"""
MySQL Database Adapter for Smart Library
Handles MySQL database connections and operations
"""

import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MySQLAdapter:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                database=os.getenv('MYSQL_DATABASE', 'smart_library'),
                user=os.getenv('MYSQL_USERNAME', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                port=os.getenv('MYSQL_PORT', 3306)
            )
            
            if self.connection.is_connected():
                print(f"✓ Connected to MySQL database: {os.getenv('MYSQL_DATABASE', 'smart_library')}")
                return True
        except Error as e:
            print(f"❌ MySQL connection failed: {e}")
            return False
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute SQL query"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
                
        except Error as e:
            print(f"❌ Query execution failed: {e}")
            return None if fetch else False
    
    def login_employee(self, username, dob):
        """Authenticate employee login"""
        query = "SELECT * FROM employees WHERE username = %s AND dob = %s"
        result = self.execute_query(query, (username, dob), fetch=True)
        return result[0] if result else None
    
    def get_all_books(self):
        """Get all books"""
        query = "SELECT * FROM books ORDER BY title"
        return self.execute_query(query, fetch=True) or []
    
    def get_book_by_id(self, book_id):
        """Get book by ID"""
        query = "SELECT * FROM books WHERE id = %s"
        result = self.execute_query(query, (book_id,), fetch=True)
        return result[0] if result else None
    
    def take_book(self, employee_id, book_id):
        """Mark book as taken"""
        try:
            # Update book status
            update_query = "UPDATE books SET status = 'unavailable' WHERE id = %s AND status = 'available'"
            if not self.execute_query(update_query, (book_id,)):
                return False
            
            # Create transaction
            insert_query = """
                INSERT INTO transactions (employee_id, book_id, taken_at, status) 
                VALUES (%s, %s, %s, 'taken')
            """
            return self.execute_query(insert_query, (employee_id, book_id, datetime.now()))
            
        except Exception as e:
            print(f"❌ Take book failed: {e}")
            return False
    
    def get_admin_stats(self):
        """Get admin dashboard statistics"""
        try:
            # Total books taken
            total_taken_query = "SELECT COUNT(*) as count FROM transactions WHERE status = 'taken'"
            total_taken = self.execute_query(total_taken_query, fetch=True)[0]['count']
            
            # Employees with books
            employees_query = "SELECT COUNT(DISTINCT employee_id) as count FROM transactions WHERE status = 'taken'"
            employees_with_books = self.execute_query(employees_query, fetch=True)[0]['count']
            
            # Department stats
            dept_query = """
                SELECT e.department, COUNT(e.id) as total_employees, 
                       COUNT(t.id) as books_taken
                FROM employees e
                LEFT JOIN transactions t ON e.id = t.employee_id AND t.status = 'taken'
                GROUP BY e.department
            """
            dept_stats = self.execute_query(dept_query, fetch=True)
            
            # Book status
            book_status_query = """
                SELECT status, COUNT(*) as count 
                FROM books 
                GROUP BY status
            """
            book_status = self.execute_query(book_status_query, fetch=True)
            
            # Format department stats
            department_stats = {}
            for dept in dept_stats:
                department_stats[dept['department']] = {
                    'total_employees': dept['total_employees'],
                    'books_taken': dept['books_taken']
                }
            
            # Format book status
            book_status_dict = {'available': 0, 'unavailable': 0, 'total': 0}
            for status in book_status:
                book_status_dict[status['status']] = status['count']
                book_status_dict['total'] += status['count']
            
            return {
                'total_books_taken': total_taken,
                'employees_with_books': employees_with_books,
                'department_stats': department_stats,
                'book_status': book_status_dict
            }
            
        except Exception as e:
            print(f"❌ Get admin stats failed: {e}")
            return None
    
    def get_all_employees(self):
        """Get all employees"""
        query = "SELECT * FROM employees ORDER BY name"
        return self.execute_query(query, fetch=True) or []
    
    def create_employee(self, employee_data):
        """Create new employee"""
        query = """
            INSERT INTO employees (username, dob, name, department) 
            VALUES (%(username)s, %(dob)s, %(name)s, %(department)s)
        """
        return self.execute_query(query, employee_data)
    
    def update_employee(self, employee_id, employee_data):
        """Update employee"""
        query = """
            UPDATE employees 
            SET username = %(username)s, dob = %(dob)s, name = %(name)s, department = %(department)s
            WHERE id = %s
        """
        params = list(employee_data.values()) + [employee_id]
        return self.execute_query(query, params)
    
    def delete_employee(self, employee_id):
        """Delete employee"""
        query = "DELETE FROM employees WHERE id = %s"
        return self.execute_query(query, (employee_id,))
    
    def create_book(self, book_data):
        """Create new book"""
        query = """
            INSERT INTO books (title, author, isbn, status) 
            VALUES (%(title)s, %(author)s, %(isbn)s, %(status)s)
        """
        return self.execute_query(query, book_data)
    
    def update_book(self, book_id, book_data):
        """Update book"""
        query = """
            UPDATE books 
            SET title = %(title)s, author = %(author)s, isbn = %(isbn)s, status = %(status)s
            WHERE id = %s
        """
        params = list(book_data.values()) + [book_id]
        return self.execute_query(query, params)
    
    def delete_book(self, book_id):
        """Delete book"""
        query = "DELETE FROM books WHERE id = %s"
        return self.execute_query(query, (book_id,))
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ MySQL connection closed")

# Global MySQL adapter instance
mysql_db = None

def get_mysql_adapter():
    """Get MySQL adapter instance"""
    global mysql_db
    if mysql_db is None:
        mysql_db = MySQLAdapter()
    return mysql_db
