"""
Database Management Tools for Smart Library
Backup, restore, and migrate data between demo and production
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

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

def backup_database(supabase, backup_file=None):
    """Backup all data from database"""
    if not backup_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"data/backup_{timestamp}.json"
    
    print(f"Creating backup: {backup_file}")
    
    try:
        # Create backup directory
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        
        # Get all data
        employees = supabase.table('employees').select('*').execute()
        books = supabase.table('books').select('*').execute()
        transactions = supabase.table('transactions').select('*').execute()
        
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'employees': employees.data,
            'books': books.data,
            'transactions': transactions.data
        }
        
        # Save to file
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✅ Backup created: {backup_file}")
        print(f"  - Employees: {len(employees.data)}")
        print(f"  - Books: {len(books.data)}")
        print(f"  - Transactions: {len(transactions.data)}")
        
        return backup_file
        
    except Exception as e:
        print(f"❌ ERROR creating backup: {str(e)}")
        return None

def restore_database(supabase, backup_file, clear_existing=True):
    """Restore data from backup file"""
    print(f"Restoring from backup: {backup_file}")
    
    if not os.path.exists(backup_file):
        print(f"❌ ERROR: Backup file not found: {backup_file}")
        return False
    
    try:
        # Load backup data
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        print(f"Backup timestamp: {backup_data.get('timestamp', 'Unknown')}")
        
        if clear_existing:
            print("Clearing existing data...")
            # Clear in reverse order due to foreign key constraints
            supabase.table('transactions').delete().neq('id', 0).execute()
            supabase.table('books').delete().neq('id', 0).execute()
            supabase.table('employees').delete().neq('id', 0).execute()
            print("✓ Existing data cleared")
        
        # Restore employees
        if backup_data.get('employees'):
            employees = backup_data['employees']
            # Remove id field to let database auto-generate
            for emp in employees:
                emp.pop('id', None)
                emp.pop('created_at', None)
                emp.pop('updated_at', None)
            
            supabase.table('employees').insert(employees).execute()
            print(f"✓ Restored {len(employees)} employees")
        
        # Restore books
        if backup_data.get('books'):
            books = backup_data['books']
            # Remove id field to let database auto-generate
            for book in books:
                book.pop('id', None)
                book.pop('created_at', None)
                book.pop('updated_at', None)
            
            supabase.table('books').insert(books).execute()
            print(f"✓ Restored {len(books)} books")
        
        # Note: Transactions are not restored as they reference old IDs
        print("⚠️  Transactions not restored (would need ID mapping)")
        
        print("✅ Database restored successfully")
        return True
        
    except Exception as e:
        print(f"❌ ERROR restoring database: {str(e)}")
        return False

def clear_all_data(supabase):
    """Clear all data from database"""
    print("⚠️  WARNING: This will delete ALL data from the database!")
    confirm = input("Type 'DELETE ALL' to confirm: ")
    
    if confirm != 'DELETE ALL':
        print("Operation cancelled")
        return False
    
    try:
        print("Clearing all data...")
        # Clear in reverse order due to foreign key constraints
        supabase.table('transactions').delete().neq('id', 0).execute()
        supabase.table('books').delete().neq('id', 0).execute()
        supabase.table('employees').delete().neq('id', 0).execute()
        
        print("✅ All data cleared")
        return True
        
    except Exception as e:
        print(f"❌ ERROR clearing data: {str(e)}")
        return False

def show_database_stats(supabase):
    """Show current database statistics"""
    try:
        employees = supabase.table('employees').select('*').execute()
        books = supabase.table('books').select('*').execute()
        transactions = supabase.table('transactions').select('*').execute()
        
        print("Current Database Statistics:")
        print("=" * 30)
        print(f"Employees: {len(employees.data)}")
        print(f"Books: {len(books.data)}")
        print(f"Transactions: {len(transactions.data)}")
        
        # Book status breakdown
        available = len([b for b in books.data if b['status'] == 'available'])
        unavailable = len([b for b in books.data if b['status'] == 'unavailable'])
        print(f"  - Available books: {available}")
        print(f"  - Unavailable books: {unavailable}")
        
        # Department breakdown
        departments = {}
        for emp in employees.data:
            dept = emp['department']
            departments[dept] = departments.get(dept, 0) + 1
        
        print("Department breakdown:")
        for dept, count in departments.items():
            print(f"  - {dept}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR getting stats: {str(e)}")
        return False

def list_backups():
    """List available backup files"""
    backup_dir = 'data'
    if not os.path.exists(backup_dir):
        print("No backup directory found")
        return []
    
    backup_files = []
    for file in os.listdir(backup_dir):
        if file.startswith('backup_') and file.endswith('.json'):
            file_path = os.path.join(backup_dir, file)
            backup_files.append(file_path)
    
    if backup_files:
        print("Available backups:")
        for i, backup in enumerate(backup_files, 1):
            print(f"{i}. {backup}")
    else:
        print("No backup files found")
    
    return backup_files

def main():
    print("Smart Library Database Manager")
    print("=" * 50)
    
    # Connect to database
    supabase = connect_to_database()
    if not supabase:
        return
    
    while True:
        print("\nOptions:")
        print("1. Show database statistics")
        print("2. Create backup")
        print("3. Restore from backup")
        print("4. List backups")
        print("5. Clear all data")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            show_database_stats(supabase)
        
        elif choice == '2':
            backup_file = backup_database(supabase)
            if backup_file:
                print(f"Backup saved to: {backup_file}")
        
        elif choice == '3':
            backups = list_backups()
            if backups:
                try:
                    index = int(input("Enter backup number: ")) - 1
                    if 0 <= index < len(backups):
                        restore_database(supabase, backups[index])
                    else:
                        print("Invalid backup number")
                except ValueError:
                    print("Invalid input")
            else:
                backup_file = input("Enter backup file path: ").strip()
                if backup_file:
                    restore_database(supabase, backup_file)
        
        elif choice == '4':
            list_backups()
        
        elif choice == '5':
            clear_all_data(supabase)
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
