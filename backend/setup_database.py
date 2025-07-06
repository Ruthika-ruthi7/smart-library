"""
Database setup script for Smart Library
Run this script to create tables and insert sample data
"""

from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def setup_database():
    """Setup database tables and insert sample data"""
    
    # Get Supabase credentials
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
        return False
    
    try:
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("Setting up Smart Library database...")
        
        # Read and execute schema
        with open('database_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        print("Creating tables...")
        # Note: For Supabase, you'll need to run the SQL manually in the SQL editor
        # This script is for reference and local testing
        
        print("Database setup instructions:")
        print("1. Go to your Supabase project dashboard")
        print("2. Navigate to the SQL Editor")
        print("3. Copy and paste the contents of 'database_schema.sql'")
        print("4. Execute the schema creation script")
        print("5. Copy and paste the contents of 'sample_data.sql'")
        print("6. Execute the sample data script")
        print("7. Update your .env file with your Supabase credentials")
        
        return True
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()
