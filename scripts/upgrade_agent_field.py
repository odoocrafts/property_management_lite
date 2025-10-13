#!/usr/bin/env python3
"""
Upgrade script to add agent field to existing agreements
Run this after updating the module with the new agent field
"""

import sys
import os

# Add the Odoo directory to the Python path if needed
# odoo_path = '/path/to/your/odoo'
# sys.path.append(odoo_path)

def upgrade_agreements_with_agents():
    """
    Script to help assign agents to existing agreements
    This can be run manually or integrated into module upgrade
    """
    
    print("Agent Field Addition - Upgrade Guide")
    print("=" * 50)
    print()
    
    print("✅ Changes Applied:")
    print("   - Added 'agent_id' field to property.agreement model")
    print("   - Updated agreement form view to include agent selection")
    print("   - Updated list view to display agent information")
    print("   - Added agent search and group by functionality")
    print("   - Created agent categories and sample agents")
    print("   - Added agent management menu")
    print()
    
    print("📋 Post-Upgrade Steps:")
    print("1. Update the module in Odoo:")
    print("   - Go to Apps → Property Management Lite → Upgrade")
    print()
    print("2. Create Agent Categories (if not automatically created):")
    print("   - Go to Contacts → Configuration → Contact Tags")
    print("   - Create tags: 'Property Agent', 'Rental Agent', 'Sales Agent'")
    print()
    print("3. Set up Agents:")
    print("   - Go to Property Management → Tenant Management → Agents")
    print("   - Create or update existing contacts as agents")
    print("   - Assign appropriate categories to agent contacts")
    print()
    print("4. Assign Agents to Existing Agreements:")
    print("   - Go to Property Management → Tenant Management → Agreements")
    print("   - Edit existing agreements to assign appropriate agents")
    print("   - Use bulk edit functionality if available")
    print()
    
    print("🔍 Agent Selection Criteria:")
    print("   - Contacts with 'Property Agent', 'Rental Agent', or 'Sales Agent' categories")
    print("   - Contacts with 'agent' in their job title/function")
    print("   - Individual contacts only (not companies)")
    print()
    
    print("📊 New Features Available:")
    print("   - Agent field in agreement forms")
    print("   - Agent column in agreement lists")
    print("   - Group agreements by agent")
    print("   - Search agreements by agent")
    print("   - Agent performance tracking capabilities")
    print()
    
    print("🎯 Benefits:")
    print("   - Track which agent handled each agreement")
    print("   - Generate agent performance reports")
    print("   - Commission calculation based on agent assignments")
    print("   - Better accountability and customer service")
    print()
    
    print("⚠️  Important Notes:")
    print("   - Existing agreements will have empty agent field initially")
    print("   - Agent field is optional - agreements can exist without agents")
    print("   - Agent tracking is now available for new agreements")
    print("   - Historical data can be updated manually as needed")

if __name__ == "__main__":
    upgrade_agreements_with_agents()