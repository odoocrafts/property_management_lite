from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class PropertyOutstandingDues(models.Model):
    _name = 'property.outstanding.dues'
    _description = 'Outstanding Dues Summary'
    _order = 'total_outstanding desc, tenant_id'
    _rec_name = 'tenant_id'

    # Relations
    tenant_id = fields.Many2one('property.tenant', 'Tenant', required=True)
    room_id = fields.Many2one('property.room', 'Room', required=True)
    agreement_id = fields.Many2one('property.agreement', 'Agreement')
    
    # Outstanding Amounts
    rent_outstanding = fields.Monetary('Rent Outstanding', currency_field='currency_id')
    deposit_outstanding = fields.Monetary('Deposit Outstanding', currency_field='currency_id')
    parking_outstanding = fields.Monetary('Parking Outstanding', currency_field='currency_id')
    other_charges_outstanding = fields.Monetary('Other Charges Outstanding', currency_field='currency_id')
    total_outstanding = fields.Monetary('Total Outstanding', currency_field='currency_id', 
                                       compute='_compute_total_outstanding', store=True)
    
    # Period Information
    last_payment_date = fields.Date('Last Payment Date')
    months_overdue = fields.Integer('Months Overdue', compute='_compute_overdue_months')
    days_overdue = fields.Integer('Days Overdue', compute='_compute_overdue_days')
    
    # Status
    status = fields.Selection([
        ('current', 'Current'),
        ('overdue_30', 'Overdue (1-30 days)'),
        ('overdue_60', 'Overdue (31-60 days)'),
        ('overdue_90', 'Overdue (61-90 days)'),
        ('overdue_90plus', 'Overdue (90+ days)'),
        ('critical', 'Critical (180+ days)'),
    ], string='Status', compute='_compute_status', store=True)
    
    # Financial
    currency_id = fields.Many2one('res.currency', 'Currency', 
                                  default=lambda self: self.env.company.currency_id)
    
    # Computed Fields for Details
    next_due_date = fields.Date('Next Due Date', compute='_compute_next_due_date')
    expected_monthly_amount = fields.Monetary('Expected Monthly Amount', currency_field='currency_id',
                                            compute='_compute_expected_amount')
    
    @api.depends('rent_outstanding', 'deposit_outstanding', 'parking_outstanding', 'other_charges_outstanding')
    def _compute_total_outstanding(self):
        for record in self:
            record.total_outstanding = (record.rent_outstanding + record.deposit_outstanding + 
                                      record.parking_outstanding + record.other_charges_outstanding)
    
    @api.depends('last_payment_date')
    def _compute_overdue_months(self):
        today = fields.Date.today()
        for record in self:
            if record.last_payment_date:
                delta = relativedelta(today, record.last_payment_date)
                record.months_overdue = delta.months + (delta.years * 12)
            else:
                record.months_overdue = 0
    
    @api.depends('last_payment_date')
    def _compute_overdue_days(self):
        today = fields.Date.today()
        for record in self:
            if record.last_payment_date:
                delta = today - record.last_payment_date
                record.days_overdue = delta.days
            else:
                record.days_overdue = 0
    
    @api.depends('days_overdue', 'total_outstanding')
    def _compute_status(self):
        for record in self:
            if record.total_outstanding <= 0:
                record.status = 'current'
            elif record.days_overdue <= 30:
                record.status = 'overdue_30'
            elif record.days_overdue <= 60:
                record.status = 'overdue_60'
            elif record.days_overdue <= 90:
                record.status = 'overdue_90'
            elif record.days_overdue <= 180:
                record.status = 'overdue_90plus'
            else:
                record.status = 'critical'
    
    @api.depends('agreement_id', 'agreement_id.payment_day')
    def _compute_next_due_date(self):
        today = fields.Date.today()
        for record in self:
            if record.agreement_id and record.agreement_id.payment_day:
                # Calculate next due date based on payment day
                next_month = today.replace(day=1) + relativedelta(months=1)
                try:
                    record.next_due_date = next_month.replace(day=record.agreement_id.payment_day)
                except ValueError:
                    # Handle cases like February 30th
                    record.next_due_date = next_month.replace(day=28)
            else:
                record.next_due_date = False
    
    @api.depends('agreement_id')
    def _compute_expected_amount(self):
        for record in self:
            if record.agreement_id:
                record.expected_monthly_amount = (record.agreement_id.rent_amount + 
                                                record.agreement_id.parking_charges)
            else:
                record.expected_monthly_amount = 0
    
    @api.model
    def update_outstanding_dues(self):
        """Method to calculate and update outstanding dues for all active tenants"""
        
        # Clear existing records
        self.search([]).unlink()
        
        # Get all active tenants with current agreements
        tenants = self.env['property.tenant'].search([
            ('status', '=', 'active'),
            ('current_room_id', '!=', False),
            ('current_agreement_id', '!=', False)
        ])
        
        for tenant in tenants:
            agreement = tenant.current_agreement_id
            if not agreement or agreement.state != 'active':
                continue
            
            # Calculate outstanding amounts
            rent_outstanding = self._calculate_rent_outstanding(tenant, agreement)
            deposit_outstanding = self._calculate_deposit_outstanding(tenant, agreement)
            parking_outstanding = self._calculate_parking_outstanding(tenant, agreement)
            other_charges_outstanding = self._calculate_other_charges_outstanding(tenant, agreement)
            
            # Get last payment date
            last_collection = self.env['property.collection'].search([
                ('tenant_id', '=', tenant.id),
                ('active', '=', True)
            ], limit=1, order='date desc')
            
            last_payment_date = last_collection.date if last_collection else agreement.start_date
            
            # Create outstanding dues record only if there are outstanding amounts
            if any([rent_outstanding, deposit_outstanding, parking_outstanding, other_charges_outstanding]):
                self.create({
                    'tenant_id': tenant.id,
                    'room_id': tenant.current_room_id.id,
                    'agreement_id': agreement.id,
                    'rent_outstanding': rent_outstanding,
                    'deposit_outstanding': deposit_outstanding,
                    'parking_outstanding': parking_outstanding,
                    'other_charges_outstanding': other_charges_outstanding,
                    'last_payment_date': last_payment_date,
                })
    
    def _calculate_rent_outstanding(self, tenant, agreement):
        """Calculate outstanding rent amount"""
        today = fields.Date.today()
        start_date = agreement.start_date
        monthly_rent = agreement.rent_amount
        
        # Calculate expected rent based on months passed
        months_passed = relativedelta(today, start_date).months + (relativedelta(today, start_date).years * 12)
        if today.day >= agreement.payment_day:
            months_passed += 1  # Include current month if past due date
        
        expected_rent = monthly_rent * months_passed
        
        # Calculate total rent collected
        rent_collections = self.env['property.collection'].search([
            ('tenant_id', '=', tenant.id),
            ('collection_type', '=', 'rent'),
            ('active', '=', True)
        ])
        
        total_rent_collected = sum(rent_collections.mapped('amount_collected'))
        
        return max(0, expected_rent - total_rent_collected)
    
    def _calculate_deposit_outstanding(self, tenant, agreement):
        """Calculate outstanding deposit amount"""
        expected_deposit = agreement.deposit_amount
        
        # Calculate total deposit collected
        deposit_collections = self.env['property.collection'].search([
            ('tenant_id', '=', tenant.id),
            ('collection_type', '=', 'deposit'),
            ('active', '=', True)
        ])
        
        total_deposit_collected = sum(deposit_collections.mapped('amount_collected'))
        
        return max(0, expected_deposit - total_deposit_collected)
    
    def _calculate_parking_outstanding(self, tenant, agreement):
        """Calculate outstanding parking charges"""
        today = fields.Date.today()
        start_date = agreement.start_date
        monthly_parking = agreement.parking_charges
        
        if not monthly_parking:
            return 0
        
        # Calculate expected parking charges based on months passed
        months_passed = relativedelta(today, start_date).months + (relativedelta(today, start_date).years * 12)
        if today.day >= agreement.payment_day:
            months_passed += 1
        
        expected_parking = monthly_parking * months_passed
        
        # Calculate total parking collected
        parking_collections = self.env['property.collection'].search([
            ('tenant_id', '=', tenant.id),
            ('collection_type', 'in', ['parking_charges', 'parking_deposit']),
            ('active', '=', True)
        ])
        
        total_parking_collected = sum(parking_collections.mapped('amount_collected'))
        
        # Add expected parking deposit
        expected_parking += agreement.parking_deposit
        
        return max(0, expected_parking - total_parking_collected)
    
    def _calculate_other_charges_outstanding(self, tenant, agreement):
        """Calculate outstanding other charges"""
        # Calculate based on agreement's other charges
        total_expected = 0
        
        for charge_line in agreement.other_charges_ids.filtered('active'):
            if charge_line.frequency == 'monthly':
                today = fields.Date.today()
                start_date = charge_line.start_date or agreement.start_date
                months_passed = relativedelta(today, start_date).months + (relativedelta(today, start_date).years * 12)
                if today.day >= agreement.payment_day:
                    months_passed += 1
                total_expected += charge_line.amount * months_passed
            elif charge_line.frequency == 'one_time':
                total_expected += charge_line.amount
        
        # Calculate total other charges collected
        other_collections = self.env['property.collection'].search([
            ('tenant_id', '=', tenant.id),
            ('collection_type', '=', 'other_charges'),
            ('active', '=', True)
        ])
        
        total_other_collected = sum(other_collections.mapped('amount_collected'))
        
        return max(0, total_expected - total_other_collected)
    
    def action_view_tenant_collections(self):
        """View all collections for this tenant"""
        return {
            'name': _('Tenant Collections'),
            'view_mode': 'list,form',
            'res_model': 'property.collection',
            'type': 'ir.actions.act_window',
            'domain': [('tenant_id', '=', self.tenant_id.id), ('active', '=', True)],
            'context': {'default_tenant_id': self.tenant_id.id}
        }
    
    def action_create_collection(self):
        """Create a new collection for this tenant"""
        return {
            'name': _('Create Collection'),
            'view_mode': 'form',
            'res_model': 'property.collection',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_tenant_id': self.tenant_id.id,
                'default_room_id': self.room_id.id,
                'default_agreement_id': self.agreement_id.id,
                'default_amount_collected': self.expected_monthly_amount,
            }
        }

    @api.model
    def cron_update_outstanding_dues(self):
        """Cron job to update outstanding dues daily"""
        self.update_outstanding_dues()