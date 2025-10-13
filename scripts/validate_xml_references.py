#!/usr/bin/env python3
"""
XML Reference Validation Script
Checks for common XML reference issues in the module
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def validate_xml_references():
    """Validate XML references in the module"""
    
    print("🔍 XML Reference Validation")
    print("=" * 40)
    
    base_dir = Path(__file__).parent.parent
    
    # Files to check
    xml_files = [
        'views/menu_views.xml',
        'views/agent_views.xml',
        'views/agreement_views.xml',
        'data/agent_data.xml'
    ]
    
    # Collect all defined IDs
    defined_ids = set()
    referenced_ids = set()
    
    for xml_file in xml_files:
        file_path = base_dir / xml_file
        if not file_path.exists():
            print(f"❌ File not found: {xml_file}")
            continue
            
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find all records with id attributes (definitions)
            for record in root.findall('.//record[@id]'):
                record_id = record.get('id')
                defined_ids.add(record_id)
                print(f"✅ Defined: {record_id} in {xml_file}")
            
            # Find all menuitem with id attributes (definitions)
            for menuitem in root.findall('.//menuitem[@id]'):
                menuitem_id = menuitem.get('id')
                defined_ids.add(menuitem_id)
                print(f"✅ Defined: {menuitem_id} in {xml_file}")
            
            # Find all references (ref attributes)
            for element in root.findall('.//*[@ref]'):
                ref_value = element.get('ref')
                if not ref_value.startswith('property_management_lite.'):
                    # Add module prefix for internal references
                    ref_value = f"property_management_lite.{ref_value}"
                referenced_ids.add(ref_value.replace('property_management_lite.', ''))
                print(f"🔗 Referenced: {ref_value} in {xml_file}")
                
        except ET.ParseError as e:
            print(f"❌ XML Parse Error in {xml_file}: {e}")
        except Exception as e:
            print(f"❌ Error processing {xml_file}: {e}")
    
    print("\n" + "=" * 40)
    print("📊 Validation Summary")
    print("=" * 40)
    
    # Check for missing references
    missing_refs = referenced_ids - defined_ids
    if missing_refs:
        print("❌ Missing Definitions:")
        for ref in missing_refs:
            print(f"   - {ref}")
    else:
        print("✅ All references have definitions")
    
    # Check for unused definitions
    unused_defs = defined_ids - referenced_ids
    if unused_defs:
        print("\n📝 Unused Definitions (may be used elsewhere):")
        for unused in unused_defs:
            print(f"   - {unused}")
    
    print(f"\n📈 Statistics:")
    print(f"   - Definitions found: {len(defined_ids)}")
    print(f"   - References found: {len(referenced_ids)}")
    print(f"   - Missing references: {len(missing_refs)}")
    
    if not missing_refs:
        print("\n🎉 XML validation passed! No missing references found.")
        return True
    else:
        print(f"\n⚠️  XML validation failed! {len(missing_refs)} missing references.")
        return False

if __name__ == "__main__":
    validate_xml_references()