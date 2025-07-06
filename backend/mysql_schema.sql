-- Smart Library MySQL Database Schema

-- Create database (run this first if database doesn't exist)
CREATE DATABASE IF NOT EXISTS smart_library;
USE smart_library;

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    dob DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create books table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    isbn VARCHAR(20),
    status VARCHAR(20) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (status IN ('available', 'unavailable'))
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    book_id INT,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned_at TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'taken',
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    CHECK (status IN ('taken', 'returned'))
);

-- Create indexes for better performance
CREATE INDEX idx_employees_username ON employees(username);
CREATE INDEX idx_employees_dob ON employees(dob);
CREATE INDEX idx_books_status ON books(status);
CREATE INDEX idx_transactions_employee_id ON transactions(employee_id);
CREATE INDEX idx_transactions_book_id ON transactions(book_id);
CREATE INDEX idx_transactions_taken_at ON transactions(taken_at);

-- Insert sample employees
INSERT INTO employees (username, dob, name, department) VALUES
('john_doe', '1990-05-15', 'John Doe', 'Engineering'),
('jane_smith', '1988-12-03', 'Jane Smith', 'Marketing'),
('mike_johnson', '1992-08-22', 'Mike Johnson', 'Engineering'),
('sarah_wilson', '1985-03-10', 'Sarah Wilson', 'HR'),
('david_brown', '1991-11-07', 'David Brown', 'Finance'),
('lisa_davis', '1989-06-18', 'Lisa Davis', 'Engineering'),
('tom_miller', '1993-01-25', 'Tom Miller', 'Marketing'),
('anna_garcia', '1987-09-14', 'Anna Garcia', 'HR'),
('chris_martinez', '1990-04-30', 'Chris Martinez', 'Finance'),
('emma_taylor', '1994-07-12', 'Emma Taylor', 'Engineering'),
('admin', '1980-01-01', 'System Administrator', 'IT');

-- Insert sample books
INSERT INTO books (title, author, isbn, status) VALUES
('Clean Code', 'Robert C. Martin', '978-0132350884', 'available'),
('The Pragmatic Programmer', 'David Thomas', '978-0201616224', 'available'),
('Design Patterns', 'Gang of Four', '978-0201633612', 'available'),
('JavaScript: The Good Parts', 'Douglas Crockford', '978-0596517748', 'available'),
('Python Crash Course', 'Eric Matthes', '978-1593276034', 'available'),
('You Don\'t Know JS', 'Kyle Simpson', '978-1491924464', 'available'),
('Eloquent JavaScript', 'Marijn Haverbeke', '978-1593279509', 'available'),
('The Clean Coder', 'Robert C. Martin', '978-0137081073', 'available'),
('Refactoring', 'Martin Fowler', '978-0201485677', 'available'),
('Code Complete', 'Steve McConnell', '978-0735619678', 'available'),
('The Mythical Man-Month', 'Frederick Brooks', '978-0201835953', 'available'),
('Cracking the Coding Interview', 'Gayle McDowell', '978-0984782857', 'available'),
('System Design Interview', 'Alex Xu', '978-1736049112', 'available'),
('Algorithms', 'Robert Sedgewick', '978-0321573513', 'available'),
('Introduction to Algorithms', 'Thomas Cormen', '978-0262033848', 'available'),
('Head First Design Patterns', 'Eric Freeman', '978-0596007126', 'available'),
('Effective Java', 'Joshua Bloch', '978-0134685991', 'available'),
('Spring in Action', 'Craig Walls', '978-1617294945', 'available'),
('React: Up & Running', 'Stoyan Stefanov', '978-1491931820', 'available'),
('Node.js in Action', 'Mike Cantelon', '978-1617290572', 'available');

-- Insert some sample transactions (some books taken)
INSERT INTO transactions (employee_id, book_id, taken_at, status) VALUES
(1, 1, '2024-01-15 10:30:00', 'taken'),
(2, 5, '2024-01-16 14:20:00', 'taken'),
(3, 8, '2024-01-17 09:15:00', 'taken'),
(4, 12, '2024-01-18 11:45:00', 'taken'),
(5, 3, '2024-01-19 16:30:00', 'taken');

-- Update book status for taken books
UPDATE books SET status = 'unavailable' WHERE id IN (1, 5, 8, 12, 3);
