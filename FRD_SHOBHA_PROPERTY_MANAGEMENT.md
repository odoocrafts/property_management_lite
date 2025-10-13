# Functional Requirements Document (FRD)
## Shobha Real Estate Property Management System

**System URL:** https://erp.shobharealestate.com  
**Platform:** Odoo 18.0 Enterprise  
**Module:** Property Management Lite v18.0.1.0.0  
**Document Version:** 1.0  
**Date:** September 23, 2025  

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Functional Requirements](#functional-requirements)
4. [User Roles & Permissions](#user-roles--permissions)
5. [Business Processes](#business-processes)
6. [Integration Requirements](#integration-requirements)
7. [Reporting Requirements](#reporting-requirements)
8. [Data Management](#data-management)
9. [Security Requirements](#security-requirements)
10. [Performance Requirements](#performance-requirements)

---

## 1. Executive Summary

### 1.1 Project Overview
The Shobha Real Estate Property Management System is a comprehensive Odoo 18-based solution designed to manage the complete lifecycle of property rental operations. The system manages a portfolio of **8 properties** with **151 flats**, **627 rooms**, and **614 active tenants** across Dubai properties.

### 1.2 Business Objectives
- Streamline property rental operations for Shobha Real Estate portfolio
- Automate rent collection and financial management
- Provide real-time visibility into property performance
- Enhance tenant experience through digital services
- Ensure compliance with Dubai rental regulations

### 1.3 Key Success Metrics
- **Operational Efficiency**: 90% reduction in manual processes
- **Collection Efficiency**: 95% on-time rent collection rate
- **Tenant Satisfaction**: 85% tenant portal adoption
- **Financial Visibility**: Real-time P&L reporting per property

---

## 2. System Overview

### 2.1 System Architecture
```
Shobha Real Estate ERP (https://erp.shobharealestate.com)
├── Property Management Core
│   ├── Property Portfolio (8 Buildings)
│   ├── Flat Management (151 Units)
│   ├── Room Inventory (627 Rooms)
│   └── Tenant Database (614 Active)
├── Financial Management
│   ├── Rent Collection System
│   ├── Invoice Generation
│   ├── Expense Tracking
│   └── Landlord Payments
├── Tenant Portal
│   ├── Self-Service Features
│   ├── Payment History
│   ├── Document Management
│   └── Maintenance Requests
└── Analytics & Reporting
    ├── Financial Dashboards
    ├── Occupancy Analytics
    ├── Performance KPIs
    └── Compliance Reports
```

### 2.2 Technology Stack
- **Platform**: Odoo 18.0 Enterprise
- **Database**: PostgreSQL 15+
- **Web Server**: Nginx
- **Application Server**: Python 3.11
- **Frontend**: Odoo Web Client (Responsive)
- **Mobile Access**: Progressive Web App (PWA)

---

## 3. Functional Requirements

### 3.1 Property Management Module

#### 3.1.1 Property Portfolio Management
**REQ-PM-001**: Property Registration
- System shall maintain detailed records of all 8 Shobha properties
- Each property must include: Name, Address, Total Flats, Facilities, Contact Details
- Properties: ADCB, AL BAKER, AL DAR, B.D, DEEMA, JS, S.P, YAHYA

**REQ-PM-002**: Flat Management
- System shall manage 151 flats across all properties
- Each flat must include: Property Reference, Flat Number, Floor, Room Count, Status
- Support for flat-level utilities and maintenance tracking

**REQ-PM-003**: Room Inventory
- System shall manage 627 individual rooms with detailed specifications
- Room types: Master Room, Partition Room, Sharing Room, Maid Room, Separate Room
- Each room must track: Facilities, Rent Amount, Occupancy Status, Maintenance History

#### 3.1.2 Room Type Configuration
**REQ-PM-004**: Room Categories
- **Master Room**: AED 2,500-4,500/month (Premium private rooms)
- **Partition Room**: AED 1,800-3,000/month (Divided spaces)
- **Sharing Room**: AED 1,200-2,200/month (Shared accommodations)
- **Maid Room**: AED 800-1,500/month (Service quarters)
- **Separate Room**: AED 2,000-3,500/month (Independent units)

### 3.2 Tenant Management Module

#### 3.2.1 Tenant Registration
**REQ-TM-001**: Tenant Profiles
- System shall maintain comprehensive profiles for all 614 tenants
- Required fields: Name, Emirates ID, Passport, Visa Status, Contact Details
- Optional fields: Emergency Contact, Employer Details, References

**REQ-TM-002**: Document Management
- System shall store and manage tenant documents securely
- Document types: Emirates ID, Passport, Visa, Labor Card, Salary Certificate
- Version control and expiry date tracking for all documents

**REQ-TM-003**: Tenant Portal Access
- Each tenant shall have portal access with unique credentials
- Portal features: Payment History, Document Upload, Maintenance Requests, Agreement Details

#### 3.2.2 Agreement Management
**REQ-TM-004**: Rental Agreements
- System shall manage 614 active rental agreements
- Agreement details: Tenant, Room, Agent, Rent Amount, Deposit, Start/End Dates, Terms
- Agent assignment for tracking responsibility and performance
- Automated renewal notifications and expiry tracking

**REQ-TM-005**: Agreement Lifecycle
- Support for agreement states: Draft, Active, Expired, Terminated
- Automated agreement activation upon tenant move-in
- Exit process with deposit settlement and room handover
- Agent performance tracking and commission calculation

### 3.3 Agent Management Module

#### 3.3.1 Agent Registration
**REQ-AM-001**: Agent Profiles
- System shall maintain comprehensive profiles for property agents
- Integration with Odoo Contacts module for unified contact management
- Agent categories: Property Agent, Rental Agent, Sales Agent
- Required fields: Name, Contact Details, Job Function, Category

**REQ-AM-002**: Agent Assignment
- Agents can be assigned to rental agreements for tracking responsibility
- Support for agent performance tracking and commission calculation
- Agent-specific workflows and reporting capabilities

#### 3.3.2 Agent Performance
**REQ-AM-003**: Performance Tracking
- Track agreements handled by each agent
- Monitor agent success rates and customer satisfaction
- Generate agent performance reports and KPIs
- Commission calculation based on successful agreements

### 3.4 Financial Management Module

#### 3.3.1 Rent Collection
**REQ-FM-001**: Payment Processing
- Support multiple payment methods: Cash, Bank Transfer, Cheque, Online Payment
- Real-time payment recording and receipt generation
- Integration with UAE banking systems for transfer verification

**REQ-FM-002**: Invoice Generation
- Automated monthly invoice generation for all active agreements
- Customizable invoice templates with Shobha branding
- Integration with Odoo Accounting module for financial posting

**REQ-FM-003**: Due Management
- Automated due tracking and reminder system
- Grace period configuration (typically 5 days)
- Escalation workflow for overdue payments

#### 3.3.2 Financial Reporting
**REQ-FM-004**: Revenue Tracking
- Real-time revenue monitoring per property and room type
- Monthly, quarterly, and annual revenue reports
- Comparison analysis with previous periods

**REQ-FM-005**: Expense Management
- Property-wise expense tracking and categorization
- Approval workflow for expense authorization
- Integration with vendor management system

### 3.4 Operations Management

#### 3.4.1 Daily Operations
**REQ-OM-001**: Dashboard Analytics
- Real-time occupancy rates across all properties
- Daily collection summary and targets
- Outstanding dues and follow-up requirements
- Maintenance request status tracking

**REQ-OM-002**: Collection Workflow
- Morning due report generation
- Collection team assignment and tracking
- Evening reconciliation and deposit confirmation
- Bank deposit reconciliation

#### 3.4.2 Maintenance Management
**REQ-OM-003**: Maintenance Requests
- Tenant-initiated maintenance requests through portal
- Internal maintenance scheduling and tracking
- Vendor management and work order generation
- Cost tracking and approval workflow

---

## 4. User Roles & Permissions

### 4.1 User Hierarchy

#### 4.1.1 Property Administrator
**Permissions**: Full system access
- Property portfolio configuration
- User management and security settings
- System customization and module configuration
- Financial reporting and analytics access

#### 4.1.2 Property Manager
**Permissions**: Operational management
- Property and room management
- Tenant agreement approval
- Financial oversight and reporting
- Staff performance monitoring

#### 4.1.3 Property Officer
**Permissions**: Daily operations
- Rent collection and payment processing
- Tenant communication and support
- Maintenance request coordination
- Expense recording and submission

#### 4.1.4 Property User
**Permissions**: Data entry and basic operations
- Tenant profile updates
- Payment recording
- Document upload assistance
- Basic reporting access

#### 4.1.5 Tenant Portal User
**Permissions**: Self-service features
- Payment history viewing
- Document upload and management
- Maintenance request submission
- Agreement details access

---

## 5. Business Processes

### 5.1 Tenant Onboarding Process

#### 5.1.1 Pre-Onboarding
1. **Room Inquiry**: Tenant submits interest through website/phone
2. **Room Viewing**: Scheduled property visit and room inspection
3. **Application**: Tenant completes application form with documents
4. **Verification**: Document verification and background check
5. **Approval**: Management approval for tenancy

#### 5.1.2 Agreement Creation
1. **Room Assignment**: Available room allocation to approved tenant
2. **Agreement Generation**: Rental agreement creation with terms
3. **Deposit Collection**: Security deposit and first month rent collection
4. **Agreement Signing**: Digital or physical agreement execution
5. **Move-in**: Room handover and tenant portal activation

### 5.2 Monthly Operations Cycle

#### 5.2.1 Month-End Process
1. **Invoice Generation**: Automated invoice creation for all tenants
2. **Payment Collection**: Multi-channel payment collection
3. **Due Tracking**: Identification and follow-up of overdue accounts
4. **Reconciliation**: Bank and cash reconciliation
5. **Reporting**: Monthly financial and operational reports

#### 5.2.2 Landlord Management
1. **Rent Calculation**: Landlord share calculation per agreement
2. **Expense Deduction**: Property expense allocation
3. **Payment Processing**: Landlord payment generation and transfer
4. **Reporting**: Landlord statement and tax documentation

### 5.3 Tenant Exit Process

#### 5.3.1 Notice Period
1. **Exit Notice**: Tenant submits 30-day notice through portal
2. **Inspection Scheduling**: Pre-exit room inspection arrangement
3. **Settlement Calculation**: Final bill and deposit adjustment
4. **Documentation**: Exit documentation and clearance process

#### 5.3.2 Room Handover
1. **Final Inspection**: Room condition assessment
2. **Damage Assessment**: Repair cost calculation if applicable
3. **Deposit Settlement**: Final deposit refund processing
4. **Room Preparation**: Cleaning and preparation for next tenant

---

## 6. Integration Requirements

### 6.1 Internal Integrations

#### 6.1.1 Odoo Core Modules
- **Accounting**: Automated journal entries and financial posting
- **CRM**: Lead management and customer lifecycle
- **Sales**: Quotation generation for new tenants
- **Contacts**: Customer and vendor management
- **Website**: Public property listings and inquiry forms

#### 6.1.2 Portal Integration
- **Self-Service Portal**: Tenant access to account information
- **Document Management**: Secure document storage and retrieval
- **Payment Gateway**: Online payment processing
- **Communication**: Automated email and SMS notifications

### 6.2 External Integrations

#### 6.2.1 Banking Integration
- **UAE Banks**: Integration with major UAE banks for payment verification
- **Payment Gateways**: Integration with local payment processors
- **Bank Reconciliation**: Automated transaction matching

#### 6.2.2 Government Systems
- **Emirates ID Verification**: Real-time ID verification service
- **Visa Status Check**: MOI visa status verification
- **RERA Compliance**: Dubai rental regulation compliance

---

## 7. Reporting Requirements

### 7.1 Financial Reports

#### 7.1.1 Revenue Reports
- **Daily Collection Report**: Daily payment summary by property
- **Monthly Revenue Report**: Comprehensive monthly financial summary
- **Annual Financial Statement**: Yearly P&L and balance sheet
- **Property Performance**: Individual property profitability analysis

#### 7.1.2 Receivables Reports
- **Aging Report**: Outstanding receivables by aging buckets
- **Collection Efficiency**: Payment collection performance metrics
- **Due Forecast**: Projected collections for upcoming periods

### 7.2 Operational Reports

#### 7.2.1 Occupancy Reports
- **Occupancy Rate**: Real-time occupancy statistics by property
- **Vacancy Analysis**: Vacant room analysis with duration
- **Turnover Report**: Tenant turnover rates and trends

#### 7.2.2 Tenant Reports
- **Tenant Profile**: Comprehensive tenant information reports
- **Agreement Status**: Current agreement status and renewals
- **Tenant Communication**: Communication history and follow-ups

### 7.3 Management Reports

#### 7.3.1 Executive Dashboard
- **KPI Summary**: Key performance indicators across all metrics
- **Trend Analysis**: Historical trend analysis and forecasting
- **Exception Reports**: Alerts and notifications for critical issues

---

## 8. Data Management

### 8.1 Data Structure

#### 8.1.1 Master Data
- **Property Portfolio**: 8 properties with complete specifications
- **Room Inventory**: 627 rooms with detailed attributes
- **Tenant Database**: 614 active tenant profiles
- **Agreement Repository**: Current and historical agreements

#### 8.1.2 Transactional Data
- **Payment Records**: All payment transactions with audit trail
- **Invoice History**: Complete invoice generation and status tracking
- **Maintenance Records**: Maintenance request and completion history
- **Communication Logs**: All tenant and vendor communications

### 8.2 Data Quality

#### 8.2.1 Data Validation
- **Input Validation**: Real-time data validation during entry
- **Duplicate Detection**: Automated duplicate record prevention
- **Data Cleansing**: Regular data quality monitoring and correction

#### 8.2.2 Data Backup
- **Automated Backup**: Daily automated backup to secure location
- **Disaster Recovery**: Complete disaster recovery procedures
- **Data Retention**: Policy-compliant data retention management

---

## 9. Security Requirements

### 9.1 Access Control

#### 9.1.1 Authentication
- **Multi-Factor Authentication**: Required for administrative users
- **Password Policy**: Strong password requirements and rotation
- **Session Management**: Secure session handling and timeout

#### 9.1.2 Authorization
- **Role-Based Access**: Granular permissions based on user roles
- **Data Isolation**: Property-wise data access restrictions
- **Audit Trail**: Complete user activity logging

### 9.2 Data Protection

#### 9.2.1 Encryption
- **Data at Rest**: Database encryption for sensitive information
- **Data in Transit**: SSL/TLS encryption for all communications
- **Document Storage**: Encrypted storage for tenant documents

#### 9.2.2 Privacy Compliance
- **UAE Data Protection**: Compliance with UAE data protection laws
- **Tenant Privacy**: Secure handling of personal information
- **Document Retention**: Policy-compliant document management

---

## 10. Performance Requirements

### 10.1 System Performance

#### 10.1.1 Response Time
- **Dashboard Loading**: < 3 seconds for main dashboard
- **Report Generation**: < 10 seconds for standard reports
- **Search Operations**: < 2 seconds for tenant/property search
- **Payment Processing**: < 5 seconds for payment recording

#### 10.1.2 Scalability
- **User Concurrent**: Support for 50+ concurrent users
- **Data Volume**: Handle 10,000+ transactions per month
- **Property Growth**: Scalable to 20+ properties
- **Tenant Capacity**: Support for 2,000+ tenant records

### 10.2 System Availability

#### 10.2.1 Uptime Requirements
- **System Availability**: 99.5% uptime (excluding planned maintenance)
- **Planned Maintenance**: Maximum 4 hours per month
- **Recovery Time**: < 4 hours for system recovery

#### 10.2.2 Monitoring
- **Performance Monitoring**: Real-time system performance tracking
- **Alert System**: Automated alerts for system issues
- **Health Checks**: Regular system health assessments

---

## 11. Implementation Roadmap

### 11.1 Current Status (Completed)
✅ **Phase 1: Core System Implementation**
- Property portfolio setup (8 properties)
- Flat configuration (151 flats)
- Room inventory management (627 rooms)
- Tenant database creation (614 tenants)
- Rental agreement setup (614 active agreements)

### 11.2 Phase 2: Enhancement & Optimization
🔄 **Immediate Priorities (Q4 2025)**
- Payment gateway integration
- SMS notification system
- Advanced reporting dashboard
- Mobile app development
- Performance optimization

### 11.3 Phase 3: Advanced Features
🔮 **Future Enhancements (2026)**
- AI-powered analytics
- IoT sensor integration
- Predictive maintenance
- WhatsApp Business API integration
- Multi-language support

---

## 12. Acceptance Criteria

### 12.1 Functional Acceptance
- All 614 tenants successfully onboarded with complete profiles
- All 627 rooms properly configured and mapped to agreements
- All financial processes working end-to-end
- Tenant portal fully functional with all features
- All reports generating accurately

### 12.2 Performance Acceptance
- Dashboard loading within 3 seconds
- Payment processing within 5 seconds
- 99.5% system uptime achieved
- Support for 50+ concurrent users
- All security requirements implemented

### 12.3 User Acceptance
- 85% user satisfaction rating
- 90% tenant portal adoption
- 95% collection efficiency rate
- Successful staff training completion
- Management approval and sign-off

---

## 13. Maintenance & Support

### 13.1 Ongoing Maintenance
- Regular system updates and patches
- Database optimization and maintenance
- Security monitoring and updates
- Performance tuning and optimization
- User training and support

### 13.2 Support Structure
- **Level 1**: End-user support and basic troubleshooting
- **Level 2**: Technical support and system administration
- **Level 3**: Advanced technical support and development
- **Escalation**: Emergency support and critical issue resolution

---

**Document Prepared By**: Property Management System Team  
**Approved By**: Shobha Real Estate Management  
**Next Review Date**: December 23, 2025  

---

*This document serves as the comprehensive functional specification for the Shobha Real Estate Property Management System hosted at https://erp.shobharealestate.com*