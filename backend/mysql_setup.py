"""
MySQL Database Setup and Testing Script
Run this to configure and test your MySQL connection
"""

import mysql.connector
from mysql.connector import Error
import getpass

def test_mysql_connection():
    """Test MySQL connection and show data"""
    print("🗄️ MYSQL DATABASE CONNECTION TEST")
    print("=" * 50)
    
    # Get MySQL credentials
    print("Enter your MySQL database credentials:")
    host = input("Host (default: localhost): ").strip() or 'localhost'
    database = input("Database name (default: sl): ").strip() or 'sl'
    user = input("Username (default: root): ").strip() or 'root'
    password = getpass.getpass("Password: ")
    
    config = {
        'host': host,
        'database': database,
        'user': user,
        'password': password,
        'port': 3306
    }
    
    try:
        print(f"\n🔍 Connecting to {host}:{database}...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ MySQL connection successful!")
            cursor = connection.cursor(dictionary=True)
            
            # Check worker table
            print("\n📋 Checking 'worker' table...")
            try:
                cursor.execute("SELECT COUNT(*) as count FROM worker")
                result = cursor.fetchone()
                worker_count = result['count']
                print(f"✅ Found {worker_count} workers")
                
                # Show sample workers
                cursor.execute("SELECT * FROM worker LIMIT 3")
                workers = cursor.fetchall()
                print("📊 Sample workers:")
                for worker in workers:
                    name = worker.get('Name', 'N/A')
                    dept = worker.get('Department', 'N/A')
                    emp_id = worker.get('Emp ID', 'N/A')
                    print(f"   • {name} | {dept} | {emp_id}")
                    
            except Error as e:
                print(f"❌ Worker table error: {e}")
            
            # Check books table
            print("\n📚 Checking 'books details' table...")
            try:
                cursor.execute("SELECT COUNT(*) as count FROM `books details`")
                result = cursor.fetchone()
                books_count = result['count']
                print(f"✅ Found {books_count} books")
                
                # Show sample books
                cursor.execute("SELECT * FROM `books details` LIMIT 3")
                books = cursor.fetchall()
                print("📊 Sample books:")
                for book in books:
                    title = book.get('Book name', 'N/A')
                    author = book.get('Author', 'N/A')
                    genre = book.get('Genre', 'N/A')
                    print(f"   • {title} | {author} | {genre}")
                    
            except Error as e:
                print(f"❌ Books table error: {e}")
            
            connection.close()
            
            print("\n🎉 Database test completed!")
            print("\n📋 To use this database:")
            print("1. Update mysql_backend.py with your password")
            print("2. Run: python mysql_backend.py")
            print("3. Your real data will be imported automatically")
            
            return True
            
    except Error as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Common solutions:")
        print("• Check if MySQL server is running")
        print("• Verify database name, username, and password")
        print("• Ensure database 'sl' exists")
        print("• Check if tables 'worker' and 'books details' exist")
        return False

if __name__ == "__main__":
    test_mysql_connection()
