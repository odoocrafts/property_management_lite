#!/usr/bin/env python3
"""
Data Import Script for Shobha Property Management
==============================================

This script processes the Excel files from "shobha data import" directory
and prepares clean CSV files for importing into the Property Management system.
"""

import pandas as pd
import os
import sys
from pathlib import Path

def clean_data():
    """Clean and prepare the Excel data for import"""
    
    # File paths
    base_dir = Path(__file__).parent
    import_dir = base_dir / "shobha data import"
    output_dir = base_dir / "import_csv"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Read the main data file
    excel_file = import_dir / "import_data_template_AUG2025_Complete 2.xlsx"
    
    print(f"Reading data from: {excel_file}")
    
    # Read with proper headers (row 1 contains the actual headers)
    df = pd.read_excel(excel_file, header=1)
    
    # Clean column names
    df.columns = [
        'building_name',
        'flat_no',
        'room_no', 
        'room_type',
        'customer_name',
        'rent',
        'deposit',
        'deposit_transfer',
        'parking',
        'other_charges',
        'collected_by',
        'payment_method',
        'date'
    ]
    
    print(f"Total rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Remove empty rows
    df = df.dropna(subset=['building_name', 'customer_name'])
    print(f"Rows after removing empty: {len(df)}")
    
    # Clean and standardize data
    df['building_name'] = df['building_name'].astype(str).str.strip().str.upper()
    df['flat_no'] = pd.to_numeric(df['flat_no'], errors='coerce')
    df['customer_name'] = df['customer_name'].astype(str).str.strip().str.title()
    df['room_type'] = df['room_type'].astype(str).str.strip().str.upper()
    
    # Clean rent amounts - extract numeric values
    df['rent_clean'] = pd.to_numeric(df['rent'], errors='coerce')
    
    # Fill missing room numbers with flat numbers
    df['room_no'] = df['room_no'].fillna(df['flat_no'])
    
    # Create unique identifiers
    df['property_ref'] = df['building_name']
    df['flat_ref'] = df['building_name'] + '_' + df['flat_no'].astype(str)
    df['room_ref'] = df['flat_ref'] + '_' + df['room_no'].astype(str)
    
    print("\nData summary:")
    print(f"Unique Buildings: {df['building_name'].nunique()}")
    print(f"Unique Flats: {df['flat_ref'].nunique()}")
    print(f"Unique Rooms: {df['room_ref'].nunique()}")
    print(f"Unique Tenants: {df['customer_name'].nunique()}")
    
    # Save cleaned data
    df.to_csv(output_dir / "cleaned_data.csv", index=False)
    print(f"\nCleaned data saved to: {output_dir / 'cleaned_data.csv'}")
    
    return df

def create_properties_csv(df):
    """Create CSV for Properties (Buildings)"""
    output_dir = Path(__file__).parent / "import_csv"
    
    # Extract unique properties
    properties = df.groupby('building_name').agg({
        'flat_no': 'nunique',
        'room_ref': 'nunique',
        'customer_name': 'nunique'
    }).reset_index()
    
    properties.columns = ['name', 'total_flats', 'total_rooms', 'total_tenants']
    properties['address'] = 'Deira, Dubai, UAE'  # Default address
    properties['property_type'] = 'building'
    properties['external_id'] = 'property_' + properties['name'].str.lower()
    
    # Reorder columns for Odoo import
    properties = properties[['external_id', 'name', 'address', 'property_type', 'total_flats', 'total_rooms']]
    
    properties.to_csv(output_dir / "properties.csv", index=False)
    print(f"Properties CSV created: {len(properties)} buildings")
    return properties

def create_flats_csv(df):
    """Create CSV for Flats"""
    output_dir = Path(__file__).parent / "import_csv"
    
    # Extract unique flats
    flats = df.groupby(['building_name', 'flat_no']).agg({
        'room_ref': 'nunique',
        'customer_name': 'nunique'
    }).reset_index()
    
    flats.columns = ['property_name', 'flat_number', 'total_rooms', 'total_tenants']
    flats['name'] = 'Flat ' + flats['flat_number'].astype(str)
    flats['property_external_id'] = 'property_' + flats['property_name'].str.lower()
    flats['external_id'] = flats['property_external_id'] + '_flat_' + flats['flat_number'].astype(str)
    
    # Reorder columns
    flats = flats[['external_id', 'name', 'property_external_id', 'flat_number', 'total_rooms']]
    
    flats.to_csv(output_dir / "flats.csv", index=False)
    print(f"Flats CSV created: {len(flats)} flats")
    return flats

def create_rooms_csv(df):
    """Create CSV for Rooms"""
    output_dir = Path(__file__).parent / "import_csv"
    
    # Create rooms data
    rooms = df[['building_name', 'flat_no', 'room_no', 'room_type', 'room_ref']].drop_duplicates()
    
    rooms['name'] = 'Room ' + rooms['room_no'].astype(str)
    rooms['flat_external_id'] = 'property_' + rooms['building_name'].str.lower() + '_flat_' + rooms['flat_no'].astype(str)
    rooms['external_id'] = rooms['flat_external_id'] + '_room_' + rooms['room_no'].astype(str)
    rooms['room_type_clean'] = rooms['room_type']
    
    # Map room types to standard types
    room_type_mapping = {
        'ATTACH BAL.': 'attached_bathroom',
        'S. ATTACH': 'attached_bathroom', 
        'SHARING': 'shared',
        'MAID ROOM': 'maid_room',
        'HALL PART. BAL': 'hall_partition',
        'HALL 1ST PART.': 'hall_partition',
        'HALL 2ND PART.': 'hall_partition',
        '1ST PART.': 'partition',
        'PART. BAL.': 'partition',
        'SMALL ATTACH': 'attached_bathroom'
    }
    
    rooms['room_type_standard'] = rooms['room_type'].map(room_type_mapping).fillna('other')
    
    # Reorder columns
    rooms = rooms[['external_id', 'name', 'flat_external_id', 'room_type_standard', 'room_type']]
    
    rooms.to_csv(output_dir / "rooms.csv", index=False)
    print(f"Rooms CSV created: {len(rooms)} rooms")
    return rooms

def create_tenants_csv(df):
    """Create CSV for Tenants"""
    output_dir = Path(__file__).parent / "import_csv"
    
    # Create tenants data (one tenant can have multiple rooms)
    tenants = df[['customer_name']].drop_duplicates()
    tenants = tenants[tenants['customer_name'].notna()]
    
    tenants['name'] = tenants['customer_name']
    tenants['external_id'] = 'tenant_' + tenants['customer_name'].str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
    tenants['status'] = 'active'
    tenants['nationality'] = 'UAE'  # Default nationality
    
    # Reorder columns
    tenants = tenants[['external_id', 'name', 'status', 'nationality']]
    
    tenants.to_csv(output_dir / "tenants.csv", index=False)
    print(f"Tenants CSV created: {len(tenants)} tenants")
    return tenants

def create_agreements_csv(df):
    """Create CSV for Rental Agreements"""
    output_dir = Path(__file__).parent / "import_csv"
    
    # Create agreements for each tenant-room combination
    agreements = df[['customer_name', 'room_ref', 'rent_clean', 'deposit', 'building_name', 'flat_no', 'room_no']].copy()
    agreements = agreements[agreements['customer_name'].notna()]
    
    agreements['name'] = 'Agreement - ' + agreements['customer_name'] + ' - Room ' + agreements['room_no'].astype(str)
    agreements['tenant_external_id'] = 'tenant_' + agreements['customer_name'].str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
    agreements['room_external_id'] = 'property_' + agreements['building_name'].str.lower() + '_flat_' + agreements['flat_no'].astype(str) + '_room_' + agreements['room_no'].astype(str)
    agreements['external_id'] = agreements['tenant_external_id'] + '_' + agreements['room_external_id']
    
    agreements['rent_amount'] = agreements['rent_clean']
    agreements['state'] = 'active'
    agreements['start_date'] = '2025-08-01'  # Default start date
    agreements['end_date'] = '2026-07-31'    # Default end date (1 year)
    
    # Clean deposit amounts
    agreements['deposit_amount'] = pd.to_numeric(agreements['deposit'], errors='coerce').fillna(0)
    
    # Reorder columns
    agreements = agreements[['external_id', 'name', 'tenant_external_id', 'room_external_id', 'rent_amount', 'deposit_amount', 'state', 'start_date', 'end_date']]
    
    agreements.to_csv(output_dir / "agreements.csv", index=False)
    print(f"Agreements CSV created: {len(agreements)} agreements")
    return agreements

def main():
    """Main function to run the data import preparation"""
    print("Shobha Property Management - Data Import Preparation")
    print("=" * 55)
    
    try:
        # Clean the main data
        df = clean_data()
        
        print("\nCreating CSV files for import...")
        
        # Create individual CSV files
        create_properties_csv(df)
        create_flats_csv(df)
        create_rooms_csv(df)
        create_tenants_csv(df)
        create_agreements_csv(df)
        
        print("\n" + "=" * 55)
        print("Data preparation completed successfully!")
        print("CSV files are ready in the 'import_csv' directory")
        print("\nImport order:")
        print("1. properties.csv")
        print("2. flats.csv") 
        print("3. rooms.csv")
        print("4. tenants.csv")
        print("5. agreements.csv")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()