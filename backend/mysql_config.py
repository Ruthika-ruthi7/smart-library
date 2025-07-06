"""
MySQL Database Configuration for Smart Library
Update these settings to match your MySQL database
"""

# MySQL Database Configuration
MYSQL_CONFIG = {
    'host': 'localhost',        # Your MySQL server host
    'database': 'sl',           # Your database name (you mentioned 'sl')
    'user': 'root',             # Your MySQL username
    'password': '',             # Your MySQL password (UPDATE THIS!)
    'port': 3306,               # MySQL port (usually 3306)
    'charset': 'utf8mb4',       # Character set
    'autocommit': True
}

# Table Names in your MySQL database
MYSQL_TABLES = {
    'workers': 'worker',           # Your worker table name
    'books': 'books details'       # Your books table name (with space)
}

# Column mappings for worker table
WORKER_COLUMNS = {
    'id': 'S No',              # Primary key column
    'emp_id': 'Emp ID',        # Employee ID column
    'name': 'Name',            # Employee name column
    'department': 'Department', # Department column
    'email': 'Mail'            # Email column
}

# Column mappings for books table
BOOK_COLUMNS = {
    'id': 'S.No',              # Primary key column
    'book_no': 'Book No',      # Book number column
    'title': 'Book name',      # Book title column
    'author': 'Author',        # Author column
    'genre': 'Genre',          # Genre column
    'rack_no': 'Rack no'       # Rack number column
}

# Phone number mappings (since not in database)
EMPLOYEE_PHONES = {
    'Senthil S': '9962539968',
    'Manikandan A': '9095865808',
    'Veeramani A V': '9962572220',
    # Add more employees and their phone numbers here
    # 'Employee Name': 'Phone Number',
}

# Default phone number pattern for employees not in the mapping
DEFAULT_PHONE_PATTERN = "99{id:08d}"  # Generates phone like 9900000001, 9900000002, etc.

def get_employee_phone(name, emp_id):
    """Get phone number for employee"""
    if name in EMPLOYEE_PHONES:
        return EMPLOYEE_PHONES[name]
    else:
        # Generate phone number based on employee ID
        try:
            numeric_id = int(''.join(filter(str.isdigit, str(emp_id))))
            return f"99{numeric_id:08d}"[:10]
        except:
            return "9900000000"  # Default fallback

# Database connection test query
TEST_QUERY = "SELECT 1"

# Import settings
IMPORT_SETTINGS = {
    'batch_size': 100,          # Number of records to process at once
    'timeout': 30,              # Connection timeout in seconds
    'retry_attempts': 3,        # Number of retry attempts
    'skip_duplicates': True     # Skip duplicate records during import
}
