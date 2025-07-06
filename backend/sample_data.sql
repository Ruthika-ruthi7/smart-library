-- Sample data for Smart Library

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
('emma_taylor', '1994-07-12', 'Emma Taylor', 'Engineering');

-- Insert sample books
INSERT INTO books (title, author, isbn, status) VALUES
('Clean Code', 'Robert C. Martin', '978-0132350884', 'available'),
('The Pragmatic Programmer', 'David Thomas', '978-0201616224', 'available'),
('Design Patterns', 'Gang of Four', '978-0201633612', 'available'),
('JavaScript: The Good Parts', 'Douglas Crockford', '978-0596517748', 'available'),
('Python Crash Course', 'Eric Matthes', '978-1593276034', 'available'),
('You Don''t Know JS', 'Kyle Simpson', '978-1491924464', 'available'),
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

-- Create admin user (for admin dashboard access)
INSERT INTO employees (username, dob, name, department) VALUES
('admin', '1980-01-01', 'System Administrator', 'IT');
