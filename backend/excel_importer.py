"""
Excel Data Importer for Smart Library
Imports employee and book data from Excel files into Supabase database
"""

import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

# Load environment variables
load_dotenv()

def connect_to_database():
    """Connect to Supabase database"""
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ ERROR: Supabase credentials not found in .env file")
        return None
    
    if SUPABASE_KEY == 'your_supabase_anon_key_here':
        print("❌ ERROR: Please replace 'your_supabase_anon_key_here' with your actual Supabase anon key")
        return None
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✓ Connected to Supabase: {SUPABASE_URL}")
        return supabase
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to database: {str(e)}")
        return None

def read_excel_file(file_path, sheet_name=None):
    """Read Excel file and return DataFrame"""
    try:
        if not os.path.exists(file_path):
            print(f"❌ ERROR: File not found: {file_path}")
            return None
        
        # Read Excel file
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"✓ Read Excel file: {file_path} (Sheet: {sheet_name})")
        else:
            df = pd.read_excel(file_path)
            print(f"✓ Read Excel file: {file_path}")
        
        print(f"  - Rows: {len(df)}")
        print(f"  - Columns: {list(df.columns)}")
        return df
        
    except Exception as e:
        print(f"❌ ERROR: Failed to read Excel file: {str(e)}")
        return None

def validate_employee_data(df):
    """Validate employee data format"""
    print("\nValidating employee data...")
    
    required_columns = ['username', 'name', 'department', 'dob']
    optional_columns = ['email', 'phone', 'employee_id']
    
    # Check for required columns (case-insensitive)
    df_columns_lower = [col.lower().strip() for col in df.columns]
    missing_columns = []
    
    for req_col in required_columns:
        if req_col not in df_columns_lower:
            # Try common variations
            variations = {
                'username': ['user_name', 'login', 'userid', 'user_id'],
                'name': ['full_name', 'employee_name', 'emp_name'],
                'department': ['dept', 'division', 'team'],
                'dob': ['date_of_birth', 'birth_date', 'birthdate', 'date_birth']
            }
            
            found = False
            if req_col in variations:
                for var in variations[req_col]:
                    if var in df_columns_lower:
                        found = True
                        break
            
            if not found:
                missing_columns.append(req_col)
    
    if missing_columns:
        print(f"❌ Missing required columns: {missing_columns}")
        print("Required columns: username, name, department, dob")
        print("Your columns:", list(df.columns))
        return False
    
    print("✓ All required columns found")
    return True

def validate_book_data(df):
    """Validate book data format"""
    print("\nValidating book data...")
    
    required_columns = ['title']
    optional_columns = ['author', 'isbn', 'status', 'category', 'publisher']
    
    # Check for required columns (case-insensitive)
    df_columns_lower = [col.lower().strip() for col in df.columns]
    
    if 'title' not in df_columns_lower:
        # Try common variations
        variations = ['book_title', 'book_name', 'name']
        found = False
        for var in variations:
            if var in df_columns_lower:
                found = True
                break
        
        if not found:
            print("❌ Missing required column: title")
            print("Your columns:", list(df.columns))
            return False
    
    print("✓ Required columns found")
    return True

def normalize_column_names(df, data_type):
    """Normalize column names to match database schema"""
    column_mapping = {}
    
    if data_type == 'employees':
        mapping = {
            'user_name': 'username',
            'login': 'username',
            'userid': 'username',
            'user_id': 'username',
            'full_name': 'name',
            'employee_name': 'name',
            'emp_name': 'name',
            'dept': 'department',
            'division': 'department',
            'team': 'department',
            'date_of_birth': 'dob',
            'birth_date': 'dob',
            'birthdate': 'dob',
            'date_birth': 'dob'
        }
    else:  # books
        mapping = {
            'book_title': 'title',
            'book_name': 'title',
            'name': 'title',
            'book_author': 'author',
            'writer': 'author'
        }
    
    # Create mapping for actual columns
    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in mapping:
            column_mapping[col] = mapping[col_lower]
        else:
            column_mapping[col] = col_lower
    
    # Rename columns
    df_renamed = df.rename(columns=column_mapping)
    return df_renamed

def process_employee_data(df):
    """Process and clean employee data"""
    print("\nProcessing employee data...")
    
    # Normalize column names
    df = normalize_column_names(df, 'employees')
    
    # Clean and validate data
    processed_data = []
    
    for index, row in df.iterrows():
        try:
            # Extract required fields
            username = str(row.get('username', '')).strip()
            name = str(row.get('name', '')).strip()
            department = str(row.get('department', '')).strip()
            dob = row.get('dob')
            
            # Skip empty rows
            if not username or not name:
                print(f"⚠️  Skipping row {index + 1}: Missing username or name")
                continue
            
            # Process date of birth
            if pd.isna(dob):
                print(f"⚠️  Skipping row {index + 1}: Missing date of birth")
                continue
            
            # Convert date to string format
            if isinstance(dob, datetime):
                dob_str = dob.strftime('%Y-%m-%d')
            elif isinstance(dob, str):
                # Try to parse different date formats
                try:
                    parsed_date = pd.to_datetime(dob)
                    dob_str = parsed_date.strftime('%Y-%m-%d')
                except:
                    print(f"⚠️  Skipping row {index + 1}: Invalid date format: {dob}")
                    continue
            else:
                print(f"⚠️  Skipping row {index + 1}: Invalid date type: {type(dob)}")
                continue
            
            employee_data = {
                'username': username,
                'name': name,
                'department': department,
                'dob': dob_str
            }
            
            processed_data.append(employee_data)
            
        except Exception as e:
            print(f"⚠️  Error processing row {index + 1}: {str(e)}")
            continue
    
    print(f"✓ Processed {len(processed_data)} employee records")
    return processed_data

def process_book_data(df):
    """Process and clean book data"""
    print("\nProcessing book data...")
    
    # Normalize column names
    df = normalize_column_names(df, 'books')
    
    # Clean and validate data
    processed_data = []
    
    for index, row in df.iterrows():
        try:
            # Extract required fields
            title = str(row.get('title', '')).strip()
            
            # Skip empty rows
            if not title:
                print(f"⚠️  Skipping row {index + 1}: Missing title")
                continue
            
            book_data = {
                'title': title,
                'author': str(row.get('author', '')).strip() or None,
                'isbn': str(row.get('isbn', '')).strip() or None,
                'status': str(row.get('status', 'available')).strip().lower()
            }
            
            # Validate status
            if book_data['status'] not in ['available', 'unavailable']:
                book_data['status'] = 'available'
            
            processed_data.append(book_data)
            
        except Exception as e:
            print(f"⚠️  Error processing row {index + 1}: {str(e)}")
            continue
    
    print(f"✓ Processed {len(processed_data)} book records")
    return processed_data

def import_employees(supabase, employee_data, clear_existing=False):
    """Import employee data to database"""
    print(f"\nImporting {len(employee_data)} employees...")
    
    try:
        if clear_existing:
            print("Clearing existing employee data...")
            supabase.table('employees').delete().neq('id', 0).execute()
            print("✓ Existing employee data cleared")
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(employee_data), batch_size):
            batch = employee_data[i:i + batch_size]
            response = supabase.table('employees').insert(batch).execute()
            print(f"✓ Imported batch {i//batch_size + 1}: {len(batch)} employees")
        
        print(f"✅ Successfully imported {len(employee_data)} employees")
        return True
        
    except Exception as e:
        print(f"❌ ERROR importing employees: {str(e)}")
        return False

def import_books(supabase, book_data, clear_existing=False):
    """Import book data to database"""
    print(f"\nImporting {len(book_data)} books...")
    
    try:
        if clear_existing:
            print("Clearing existing book data...")
            supabase.table('books').delete().neq('id', 0).execute()
            print("✓ Existing book data cleared")
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(book_data), batch_size):
            batch = book_data[i:i + batch_size]
            response = supabase.table('books').insert(batch).execute()
            print(f"✓ Imported batch {i//batch_size + 1}: {len(batch)} books")
        
        print(f"✅ Successfully imported {len(book_data)} books")
        return True
        
    except Exception as e:
        print(f"❌ ERROR importing books: {str(e)}")
        return False

def main():
    print("Smart Library Excel Importer")
    print("=" * 50)
    
    # Connect to database
    supabase = connect_to_database()
    if not supabase:
        return
    
    print("\nUsage:")
    print("1. Place your Excel file in the 'data' folder")
    print("2. Run this script and follow the prompts")
    print("\nSupported formats:")
    print("- Employees: username, name, department, dob")
    print("- Books: title, author (optional), isbn (optional), status (optional)")
    
    # Get file path
    file_path = input("\nEnter Excel file path (or press Enter for data/library_data.xlsx): ").strip()
    if not file_path:
        file_path = "data/library_data.xlsx"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("Please place your Excel file in the specified location.")
        return
    
    # Get sheet names
    try:
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        print(f"\nAvailable sheets: {sheet_names}")
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return
    
    # Import employees
    if len(sheet_names) > 1:
        emp_sheet = input(f"Enter employee sheet name (or press Enter for '{sheet_names[0]}'): ").strip()
        if not emp_sheet:
            emp_sheet = sheet_names[0]
    else:
        emp_sheet = sheet_names[0]
    
    # Read and process employee data
    emp_df = read_excel_file(file_path, emp_sheet)
    if emp_df is not None and validate_employee_data(emp_df):
        emp_data = process_employee_data(emp_df)
        if emp_data:
            clear_emp = input("Clear existing employee data? (y/N): ").strip().lower() == 'y'
            import_employees(supabase, emp_data, clear_emp)
    
    # Import books (if separate sheet)
    if len(sheet_names) > 1:
        book_sheet = input(f"Enter book sheet name (or press Enter to skip): ").strip()
        if book_sheet and book_sheet in sheet_names:
            book_df = read_excel_file(file_path, book_sheet)
            if book_df is not None and validate_book_data(book_df):
                book_data = process_book_data(book_df)
                if book_data:
                    clear_books = input("Clear existing book data? (y/N): ").strip().lower() == 'y'
                    import_books(supabase, book_data, clear_books)
    
    print("\n" + "=" * 50)
    print("Import completed!")

if __name__ == "__main__":
    main()
