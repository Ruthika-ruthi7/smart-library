from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import uuid
import random
from collections import defaultdict, Counter
import calendar

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:3002", "http://127.0.0.1:3002"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Import existing employee data
from worker_data.employees import EMPLOYEES

# Root endpoint for connection testing
@app.route('/', methods=['GET'])
def root():
    """Root endpoint to test backend connectivity"""
    return jsonify({
        'status': 'success',
        'message': 'Smart Library Backend is running',
        'version': '2.0',
        'features': [
            'Employee Authentication',
            'Book Management (English & Tamil)',
            'Advanced Admin Dashboard',
            'Real-time Analytics',
            'Feedback System'
        ],
        'total_books': 374,
        'total_employees': 4595
    })

# ENGLISH BOOKS COLLECTION - 113 Books to reach 213 total
BOOKS = [
    # Fiction
    {"id": "EB001", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "book_no": "EN001", "rack_no": "E1", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB002", "title": "1984", "author": "George Orwell", "genre": "Dystopian Fiction", "book_no": "EN002", "rack_no": "E1", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB003", "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "book_no": "EN003", "rack_no": "E1", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB004", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "book_no": "EN004", "rack_no": "E1", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB005", "title": "Jane Eyre", "author": "Charlotte Brontë", "genre": "Gothic Fiction", "book_no": "EN005", "rack_no": "E2", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB006", "title": "Wuthering Heights", "author": "Emily Brontë", "genre": "Gothic Fiction", "book_no": "EN006", "rack_no": "E2", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB007", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Coming-of-age Fiction", "book_no": "EN007", "rack_no": "E2", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB008", "title": "Lord of the Flies", "author": "William Golding", "genre": "Allegorical Fiction", "book_no": "EN008", "rack_no": "E2", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB009", "title": "Animal Farm", "author": "George Orwell", "genre": "Political Satire", "book_no": "EN009", "rack_no": "E2", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB010", "title": "Brave New World", "author": "Aldous Huxley", "genre": "Science Fiction", "book_no": "EN010", "rack_no": "E3", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Science Fiction & Fantasy
    {"id": "EB011", "title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction", "book_no": "EN011", "rack_no": "E3", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB012", "title": "Foundation", "author": "Isaac Asimov", "genre": "Science Fiction", "book_no": "EN012", "rack_no": "E3", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB013", "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "book_no": "EN013", "rack_no": "E3", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB014", "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "book_no": "EN014", "rack_no": "E3", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB015", "title": "Fahrenheit 451", "author": "Ray Bradbury", "genre": "Dystopian Fiction", "book_no": "EN015", "rack_no": "E4", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB016", "title": "The Martian Chronicles", "author": "Ray Bradbury", "genre": "Science Fiction", "book_no": "EN016", "rack_no": "E4", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB017", "title": "Ender's Game", "author": "Orson Scott Card", "genre": "Science Fiction", "book_no": "EN017", "rack_no": "E4", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB018", "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genre": "Science Fiction Comedy", "book_no": "EN018", "rack_no": "E4", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB019", "title": "Neuromancer", "author": "William Gibson", "genre": "Cyberpunk", "book_no": "EN019", "rack_no": "E4", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB020", "title": "The Time Machine", "author": "H.G. Wells", "genre": "Science Fiction", "book_no": "EN020", "rack_no": "E5", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Mystery & Thriller
    {"id": "EB021", "title": "The Adventures of Sherlock Holmes", "author": "Arthur Conan Doyle", "genre": "Mystery", "book_no": "EN021", "rack_no": "E5", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB022", "title": "Murder on the Orient Express", "author": "Agatha Christie", "genre": "Mystery", "book_no": "EN022", "rack_no": "E5", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB023", "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "genre": "Crime Thriller", "book_no": "EN023", "rack_no": "E5", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB024", "title": "Gone Girl", "author": "Gillian Flynn", "genre": "Psychological Thriller", "book_no": "EN024", "rack_no": "E5", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB025", "title": "The Da Vinci Code", "author": "Dan Brown", "genre": "Thriller", "book_no": "EN025", "rack_no": "E6", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Non-Fiction
    {"id": "EB026", "title": "A Brief History of Time", "author": "Stephen Hawking", "genre": "Science", "book_no": "EN026", "rack_no": "E6", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB027", "title": "Sapiens", "author": "Yuval Noah Harari", "genre": "History", "book_no": "EN027", "rack_no": "E6", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB028", "title": "Educated", "author": "Tara Westover", "genre": "Memoir", "book_no": "EN028", "rack_no": "E6", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB029", "title": "The Immortal Life of Henrietta Lacks", "author": "Rebecca Skloot", "genre": "Science", "book_no": "EN029", "rack_no": "E6", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB030", "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "genre": "Psychology", "book_no": "EN030", "rack_no": "E7", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Business & Self-Help
    {"id": "EB031", "title": "How to Win Friends and Influence People", "author": "Dale Carnegie", "genre": "Self-Help", "book_no": "EN031", "rack_no": "E7", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB032", "title": "The 7 Habits of Highly Effective People", "author": "Stephen Covey", "genre": "Self-Help", "book_no": "EN032", "rack_no": "E7", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB033", "title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "genre": "Finance", "book_no": "EN033", "rack_no": "E7", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB034", "title": "The Lean Startup", "author": "Eric Ries", "genre": "Business", "book_no": "EN034", "rack_no": "E8", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB035", "title": "Good to Great", "author": "Jim Collins", "genre": "Business", "book_no": "EN035", "rack_no": "E8", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Technology & Programming
    {"id": "EB036", "title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "book_no": "EN036", "rack_no": "E8", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB037", "title": "The Pragmatic Programmer", "author": "David Thomas", "genre": "Programming", "book_no": "EN037", "rack_no": "E8", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB038", "title": "Design Patterns", "author": "Gang of Four", "genre": "Programming", "book_no": "EN038", "rack_no": "E8", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB039", "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "genre": "Computer Science", "book_no": "EN039", "rack_no": "E9", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB040", "title": "The Art of Computer Programming", "author": "Donald Knuth", "genre": "Computer Science", "book_no": "EN040", "rack_no": "E9", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Philosophy & Religion
    {"id": "EB041", "title": "Meditations", "author": "Marcus Aurelius", "genre": "Philosophy", "book_no": "EN041", "rack_no": "E9", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB042", "title": "The Republic", "author": "Plato", "genre": "Philosophy", "book_no": "EN042", "rack_no": "E9", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB043", "title": "Nicomachean Ethics", "author": "Aristotle", "genre": "Philosophy", "book_no": "EN043", "rack_no": "E9", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB044", "title": "The Art of War", "author": "Sun Tzu", "genre": "Strategy", "book_no": "EN044", "rack_no": "E10", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB045", "title": "Man's Search for Meaning", "author": "Viktor Frankl", "genre": "Psychology", "book_no": "EN045", "rack_no": "E10", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # History & Biography
    {"id": "EB046", "title": "The Diary of a Young Girl", "author": "Anne Frank", "genre": "Biography", "book_no": "EN046", "rack_no": "E10", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB047", "title": "Long Walk to Freedom", "author": "Nelson Mandela", "genre": "Autobiography", "book_no": "EN047", "rack_no": "E10", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB048", "title": "Steve Jobs", "author": "Walter Isaacson", "genre": "Biography", "book_no": "EN048", "rack_no": "E10", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB049", "title": "The Wright Brothers", "author": "David McCullough", "genre": "Biography", "book_no": "EN049", "rack_no": "E11", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB050", "title": "Alexander Hamilton", "author": "Ron Chernow", "genre": "Biography", "book_no": "EN050", "rack_no": "E11", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Contemporary Fiction
    {"id": "EB051", "title": "The Kite Runner", "author": "Khaled Hosseini", "genre": "Fiction", "book_no": "EN051", "rack_no": "E11", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB052", "title": "Life of Pi", "author": "Yann Martel", "genre": "Adventure Fiction", "book_no": "EN052", "rack_no": "E11", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB053", "title": "The Book Thief", "author": "Markus Zusak", "genre": "Historical Fiction", "book_no": "EN053", "rack_no": "E11", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB054", "title": "The Fault in Our Stars", "author": "John Green", "genre": "Young Adult", "book_no": "EN054", "rack_no": "E12", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB055", "title": "Where the Crawdads Sing", "author": "Delia Owens", "genre": "Fiction", "book_no": "EN055", "rack_no": "E12", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Health & Fitness
    {"id": "EB056", "title": "Atomic Habits", "author": "James Clear", "genre": "Self-Help", "book_no": "EN056", "rack_no": "E12", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB057", "title": "The Power of Now", "author": "Eckhart Tolle", "genre": "Spirituality", "book_no": "EN057", "rack_no": "E12", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB058", "title": "Mindset", "author": "Carol Dweck", "genre": "Psychology", "book_no": "EN058", "rack_no": "E12", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB059", "title": "The 4-Hour Workweek", "author": "Tim Ferriss", "genre": "Productivity", "book_no": "EN059", "rack_no": "E13", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB060", "title": "Outliers", "author": "Malcolm Gladwell", "genre": "Psychology", "book_no": "EN060", "rack_no": "E13", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Engineering & Technical
    {"id": "EB061", "title": "The Design of Everyday Things", "author": "Don Norman", "genre": "Design", "book_no": "EN061", "rack_no": "E13", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB062", "title": "Structures: Or Why Things Don't Fall Down", "author": "J.E. Gordon", "genre": "Engineering", "book_no": "EN062", "rack_no": "E13", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB063", "title": "The Soul of a New Machine", "author": "Tracy Kidder", "genre": "Technology", "book_no": "EN063", "rack_no": "E13", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB064", "title": "Code: The Hidden Language", "author": "Charles Petzold", "genre": "Computer Science", "book_no": "EN064", "rack_no": "E14", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB065", "title": "The Innovator's Dilemma", "author": "Clayton Christensen", "genre": "Business", "book_no": "EN065", "rack_no": "E14", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Economics & Politics
    {"id": "EB066", "title": "Freakonomics", "author": "Steven Levitt", "genre": "Economics", "book_no": "EN066", "rack_no": "E14", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB067", "title": "The Wealth of Nations", "author": "Adam Smith", "genre": "Economics", "book_no": "EN067", "rack_no": "E14", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB068", "title": "Democracy in America", "author": "Alexis de Tocqueville", "genre": "Political Science", "book_no": "EN068", "rack_no": "E14", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB069", "title": "The Communist Manifesto", "author": "Karl Marx", "genre": "Political Theory", "book_no": "EN069", "rack_no": "E15", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB070", "title": "On Liberty", "author": "John Stuart Mill", "genre": "Political Philosophy", "book_no": "EN070", "rack_no": "E15", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Literature Classics
    {"id": "EB071", "title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "genre": "Magical Realism", "book_no": "EN071", "rack_no": "E15", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB072", "title": "Beloved", "author": "Toni Morrison", "genre": "Historical Fiction", "book_no": "EN072", "rack_no": "E15", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB073", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Coming-of-age", "book_no": "EN073", "rack_no": "E15", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB074", "title": "Moby Dick", "author": "Herman Melville", "genre": "Adventure", "book_no": "EN074", "rack_no": "E16", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB075", "title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical Fiction", "book_no": "EN075", "rack_no": "E16", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Modern Classics
    {"id": "EB076", "title": "The Handmaid's Tale", "author": "Margaret Atwood", "genre": "Dystopian Fiction", "book_no": "EN076", "rack_no": "E16", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB077", "title": "Slaughterhouse-Five", "author": "Kurt Vonnegut", "genre": "Anti-war Fiction", "book_no": "EN077", "rack_no": "E16", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB078", "title": "Catch-22", "author": "Joseph Heller", "genre": "Satire", "book_no": "EN078", "rack_no": "E16", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB079", "title": "One Flew Over the Cuckoo's Nest", "author": "Ken Kesey", "genre": "Psychological Fiction", "book_no": "EN079", "rack_no": "E17", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB080", "title": "The Bell Jar", "author": "Sylvia Plath", "genre": "Semi-autobiographical", "book_no": "EN080", "rack_no": "E17", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Adventure & Travel
    {"id": "EB081", "title": "Into the Wild", "author": "Jon Krakauer", "genre": "Adventure", "book_no": "EN081", "rack_no": "E17", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB082", "title": "Wild", "author": "Cheryl Strayed", "genre": "Memoir", "book_no": "EN082", "rack_no": "E17", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB083", "title": "A Walk in the Woods", "author": "Bill Bryson", "genre": "Travel", "book_no": "EN083", "rack_no": "E17", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB084", "title": "The Beach", "author": "Alex Garland", "genre": "Adventure Fiction", "book_no": "EN084", "rack_no": "E18", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB085", "title": "Eat, Pray, Love", "author": "Elizabeth Gilbert", "genre": "Memoir", "book_no": "EN085", "rack_no": "E18", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Horror & Supernatural
    {"id": "EB086", "title": "Dracula", "author": "Bram Stoker", "genre": "Horror", "book_no": "EN086", "rack_no": "E18", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB087", "title": "Frankenstein", "author": "Mary Shelley", "genre": "Gothic Horror", "book_no": "EN087", "rack_no": "E18", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB088", "title": "The Shining", "author": "Stephen King", "genre": "Horror", "book_no": "EN088", "rack_no": "E18", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB089", "title": "It", "author": "Stephen King", "genre": "Horror", "book_no": "EN089", "rack_no": "E19", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB090", "title": "The Exorcist", "author": "William Peter Blatty", "genre": "Horror", "book_no": "EN090", "rack_no": "E19", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Romance & Drama
    {"id": "EB091", "title": "The Notebook", "author": "Nicholas Sparks", "genre": "Romance", "book_no": "EN091", "rack_no": "E19", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB092", "title": "Me Before You", "author": "Jojo Moyes", "genre": "Romance", "book_no": "EN092", "rack_no": "E19", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB093", "title": "The Time Traveler's Wife", "author": "Audrey Niffenegger", "genre": "Romance", "book_no": "EN093", "rack_no": "E19", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB094", "title": "Outlander", "author": "Diana Gabaldon", "genre": "Historical Romance", "book_no": "EN094", "rack_no": "E20", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB095", "title": "The Bridges of Madison County", "author": "Robert James Waller", "genre": "Romance", "book_no": "EN095", "rack_no": "E20", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Children's & Young Adult
    {"id": "EB096", "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "genre": "Fantasy", "book_no": "EN096", "rack_no": "E20", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB097", "title": "The Chronicles of Narnia", "author": "C.S. Lewis", "genre": "Fantasy", "book_no": "EN097", "rack_no": "E20", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB098", "title": "Charlotte's Web", "author": "E.B. White", "genre": "Children's Literature", "book_no": "EN098", "rack_no": "E20", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB099", "title": "The Giver", "author": "Lois Lowry", "genre": "Young Adult", "book_no": "EN099", "rack_no": "E21", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB100", "title": "Wonder", "author": "R.J. Palacio", "genre": "Children's Literature", "book_no": "EN100", "rack_no": "E21", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Poetry & Arts
    {"id": "EB101", "title": "Leaves of Grass", "author": "Walt Whitman", "genre": "Poetry", "book_no": "EN101", "rack_no": "E21", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB102", "title": "The Waste Land", "author": "T.S. Eliot", "genre": "Poetry", "book_no": "EN102", "rack_no": "E21", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB103", "title": "The Road Not Taken", "author": "Robert Frost", "genre": "Poetry", "book_no": "EN103", "rack_no": "E21", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB104", "title": "Ariel", "author": "Sylvia Plath", "genre": "Poetry", "book_no": "EN104", "rack_no": "E22", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB105", "title": "Howl and Other Poems", "author": "Allen Ginsberg", "genre": "Poetry", "book_no": "EN105", "rack_no": "E22", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},

    # Sports & Health
    {"id": "EB106", "title": "Open", "author": "Andre Agassi", "genre": "Sports Biography", "book_no": "EN106", "rack_no": "E22", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB107", "title": "The Boys in the Boat", "author": "Daniel James Brown", "genre": "Sports History", "book_no": "EN107", "rack_no": "E22", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB108", "title": "Moneyball", "author": "Michael Lewis", "genre": "Sports", "book_no": "EN108", "rack_no": "E22", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB109", "title": "The Champion's Mind", "author": "Jim Afremow", "genre": "Sports Psychology", "book_no": "EN109", "rack_no": "E23", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB110", "title": "Born to Run", "author": "Christopher McDougall", "genre": "Sports", "book_no": "EN110", "rack_no": "E23", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Final Books to reach 113 English books
    {"id": "EB111", "title": "The Alchemist", "author": "Paulo Coelho", "genre": "Philosophical Fiction", "book_no": "EN111", "rack_no": "E23", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB112", "title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "genre": "Children's Literature", "book_no": "EN112", "rack_no": "E23", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB113", "title": "Siddhartha", "author": "Hermann Hesse", "genre": "Philosophical Fiction", "book_no": "EN113", "rack_no": "E23", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},

    # Additional English Books to reach 161 total
    {"id": "EB114", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Coming-of-age", "book_no": "EN114", "rack_no": "E24", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB115", "title": "Of Mice and Men", "author": "John Steinbeck", "genre": "Fiction", "book_no": "EN115", "rack_no": "E24", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB116", "title": "The Grapes of Wrath", "author": "John Steinbeck", "genre": "Historical Fiction", "book_no": "EN116", "rack_no": "E24", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB117", "title": "East of Eden", "author": "John Steinbeck", "genre": "Fiction", "book_no": "EN117", "rack_no": "E24", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB118", "title": "The Old Man and the Sea", "author": "Ernest Hemingway", "genre": "Fiction", "book_no": "EN118", "rack_no": "E25", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB119", "title": "A Farewell to Arms", "author": "Ernest Hemingway", "genre": "War Fiction", "book_no": "EN119", "rack_no": "E25", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB120", "title": "For Whom the Bell Tolls", "author": "Ernest Hemingway", "genre": "War Fiction", "book_no": "EN120", "rack_no": "E25", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB121", "title": "The Sun Also Rises", "author": "Ernest Hemingway", "genre": "Fiction", "book_no": "EN121", "rack_no": "E25", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB122", "title": "Invisible Man", "author": "Ralph Ellison", "genre": "Social Fiction", "book_no": "EN122", "rack_no": "E26", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB123", "title": "The Sound and the Fury", "author": "William Faulkner", "genre": "Southern Gothic", "book_no": "EN123", "rack_no": "E26", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB124", "title": "As I Lay Dying", "author": "William Faulkner", "genre": "Southern Gothic", "book_no": "EN124", "rack_no": "E26", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB125", "title": "Light in August", "author": "William Faulkner", "genre": "Southern Gothic", "book_no": "EN125", "rack_no": "E26", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB126", "title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "genre": "Adventure", "book_no": "EN126", "rack_no": "E27", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB127", "title": "The Adventures of Tom Sawyer", "author": "Mark Twain", "genre": "Adventure", "book_no": "EN127", "rack_no": "E27", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB128", "title": "A Connecticut Yankee in King Arthur's Court", "author": "Mark Twain", "genre": "Satire", "book_no": "EN128", "rack_no": "E27", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB129", "title": "The Prince and the Pauper", "author": "Mark Twain", "genre": "Historical Fiction", "book_no": "EN129", "rack_no": "E27", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB130", "title": "Little Women", "author": "Louisa May Alcott", "genre": "Coming-of-age", "book_no": "EN130", "rack_no": "E28", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB131", "title": "Little Men", "author": "Louisa May Alcott", "genre": "Children's Literature", "book_no": "EN131", "rack_no": "E28", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB132", "title": "Jo's Boys", "author": "Louisa May Alcott", "genre": "Children's Literature", "book_no": "EN132", "rack_no": "E28", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB133", "title": "Anne of Green Gables", "author": "L.M. Montgomery", "genre": "Children's Literature", "book_no": "EN133", "rack_no": "E28", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB134", "title": "Anne of Avonlea", "author": "L.M. Montgomery", "genre": "Children's Literature", "book_no": "EN134", "rack_no": "E29", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB135", "title": "Anne of the Island", "author": "L.M. Montgomery", "genre": "Children's Literature", "book_no": "EN135", "rack_no": "E29", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB136", "title": "The Secret Garden", "author": "Frances Hodgson Burnett", "genre": "Children's Literature", "book_no": "EN136", "rack_no": "E29", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB137", "title": "A Little Princess", "author": "Frances Hodgson Burnett", "genre": "Children's Literature", "book_no": "EN137", "rack_no": "E29", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB138", "title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "genre": "Children's Literature", "book_no": "EN138", "rack_no": "E30", "language": "English", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "EB139", "title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll", "genre": "Children's Literature", "book_no": "EN139", "rack_no": "E30", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB140", "title": "Through the Looking-Glass", "author": "Lewis Carroll", "genre": "Children's Literature", "book_no": "EN140", "rack_no": "E30", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB141", "title": "The Jungle Book", "author": "Rudyard Kipling", "genre": "Children's Literature", "book_no": "EN141", "rack_no": "E30", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB142", "title": "Just So Stories", "author": "Rudyard Kipling", "genre": "Children's Literature", "book_no": "EN142", "rack_no": "E31", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB143", "title": "Kim", "author": "Rudyard Kipling", "genre": "Adventure", "book_no": "EN143", "rack_no": "E31", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB144", "title": "The Man Who Would Be King", "author": "Rudyard Kipling", "genre": "Adventure", "book_no": "EN144", "rack_no": "E31", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB145", "title": "Treasure Island", "author": "Robert Louis Stevenson", "genre": "Adventure", "book_no": "EN145", "rack_no": "E31", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB146", "title": "Strange Case of Dr. Jekyll and Mr. Hyde", "author": "Robert Louis Stevenson", "genre": "Gothic Fiction", "book_no": "EN146", "rack_no": "E32", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB147", "title": "Kidnapped", "author": "Robert Louis Stevenson", "genre": "Adventure", "book_no": "EN147", "rack_no": "E32", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB148", "title": "The Black Arrow", "author": "Robert Louis Stevenson", "genre": "Historical Fiction", "book_no": "EN148", "rack_no": "E32", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB149", "title": "Robinson Crusoe", "author": "Daniel Defoe", "genre": "Adventure", "book_no": "EN149", "rack_no": "E32", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB150", "title": "Moll Flanders", "author": "Daniel Defoe", "genre": "Picaresque", "book_no": "EN150", "rack_no": "E33", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB151", "title": "A Journal of the Plague Year", "author": "Daniel Defoe", "genre": "Historical Fiction", "book_no": "EN151", "rack_no": "E33", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB152", "title": "Gulliver's Travels", "author": "Jonathan Swift", "genre": "Satire", "book_no": "EN152", "rack_no": "E33", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB153", "title": "A Modest Proposal", "author": "Jonathan Swift", "genre": "Satire", "book_no": "EN153", "rack_no": "E33", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB154", "title": "The Canterbury Tales", "author": "Geoffrey Chaucer", "genre": "Medieval Literature", "book_no": "EN154", "rack_no": "E34", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB155", "title": "Paradise Lost", "author": "John Milton", "genre": "Epic Poetry", "book_no": "EN155", "rack_no": "E34", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB156", "title": "Paradise Regained", "author": "John Milton", "genre": "Epic Poetry", "book_no": "EN156", "rack_no": "E34", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB157", "title": "The Pilgrim's Progress", "author": "John Bunyan", "genre": "Allegory", "book_no": "EN157", "rack_no": "E34", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB158", "title": "Don Quixote", "author": "Miguel de Cervantes", "genre": "Adventure", "book_no": "EN158", "rack_no": "E35", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "EB159", "title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "genre": "Adventure", "book_no": "EN159", "rack_no": "E35", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB160", "title": "The Three Musketeers", "author": "Alexandre Dumas", "genre": "Adventure", "book_no": "EN160", "rack_no": "E35", "language": "English", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "EB161", "title": "The Man in the Iron Mask", "author": "Alexandre Dumas", "genre": "Historical Fiction", "book_no": "EN161", "rack_no": "E35", "language": "English", "status": "available", "available_copies": 1, "times_taken": 0}
]

# COMPREHENSIVE TAMIL BOOKS COLLECTION - ALL TAMIL BOOKS
TAMIL_BOOKS = [
    # Classical Tamil Literature
    {"id": "TB001", "title": "திருக்குறள்", "author": "திருவள்ளுவர்", "genre": "தமிழ் இலக்கியம்", "book_no": "TM001", "rack_no": "T1", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB002", "title": "கம்பராமாயணம்", "author": "கம்பர்", "genre": "காவியம்", "book_no": "TM002", "rack_no": "T1", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB003", "title": "சிலப்பதிகாரம்", "author": "இளங்கோ அடிகள்", "genre": "காவியம்", "book_no": "TM003", "rack_no": "T2", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB004", "title": "மணிமேகலை", "author": "சீத்தலை சாத்தனார்", "genre": "காவியம்", "book_no": "TM004", "rack_no": "T2", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB005", "title": "நாலடியார்", "author": "பல ஆசிரியர்கள்", "genre": "நீதி நூல்", "book_no": "TM005", "rack_no": "T3", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB006", "title": "ஆத்திசூடி", "author": "ஔவையார்", "genre": "நீதி நூல்", "book_no": "TM006", "rack_no": "T3", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB007", "title": "கொன்றை வேந்தன்", "author": "ஔவையார்", "genre": "நீதி நூல்", "book_no": "TM007", "rack_no": "T3", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB008", "title": "பரிபாடல்", "author": "பல ஆசிரியர்கள்", "genre": "சங்க இலக்கியம்", "book_no": "TM008", "rack_no": "T4", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB009", "title": "அகநானூறு", "author": "பல ஆசிரியர்கள்", "genre": "சங்க இலக்கியம்", "book_no": "TM009", "rack_no": "T4", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB010", "title": "புறநானூறு", "author": "பல ஆசிரியர்கள்", "genre": "சங்க இலக்கியம்", "book_no": "TM010", "rack_no": "T4", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Modern Tamil Literature - Kalki Krishnamurthy Complete Collection
    {"id": "TB011", "title": "பொன்னியின் செல்வன் - பாகம் 1", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM011", "rack_no": "T5", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB012", "title": "பொன்னியின் செல்வன் - பாகம் 2", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM012", "rack_no": "T5", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB013", "title": "பொன்னியின் செல்வன் - பாகம் 3", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM013", "rack_no": "T5", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB014", "title": "பொன்னியின் செல்வன் - பாகம் 4", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM014", "rack_no": "T5", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB015", "title": "பொன்னியின் செல்வன் - பாகம் 5", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM015", "rack_no": "T5", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB016", "title": "சிவகாமியின் சபதம்", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM016", "rack_no": "T6", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB017", "title": "பார்த்திபன் கனவு", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM017", "rack_no": "T6", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB018", "title": "அலை ஓசை", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "நாவல்", "book_no": "TM018", "rack_no": "T6", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB019", "title": "தியாக பூமி", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "நாவல்", "book_no": "TM019", "rack_no": "T6", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB020", "title": "கல்கியின் சிறுகதைகள்", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "சிறுகதை", "book_no": "TM020", "rack_no": "T6", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Contemporary Authors - Jeyamohan Complete Collection
    {"id": "TB021", "title": "வெண்முரசு - பாகம் 1", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM021", "rack_no": "T7", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB022", "title": "வெண்முரசு - பாகம் 2", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM022", "rack_no": "T7", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB023", "title": "வெண்முரசு - பாகம் 3", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM023", "rack_no": "T7", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB024", "title": "கொற்றவை", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM024", "rack_no": "T7", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB025", "title": "ரப்பர்", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM025", "rack_no": "T7", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB026", "title": "பின் தொடர்பவன்", "author": "ஜெயமோகன்", "genre": "சிறுகதை", "book_no": "TM026", "rack_no": "T8", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB027", "title": "எழாம் உலகம்", "author": "ஜெயமோகன்", "genre": "தத்துவம்", "book_no": "TM027", "rack_no": "T8", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Poetry and Literature - Bharathiyar Complete Collection
    {"id": "TB028", "title": "குயில் பாட்டு", "author": "சுப்ரமணிய பாரதி", "genre": "கவிதை", "book_no": "TM028", "rack_no": "T9", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB029", "title": "பாஞ்சாலி சபதம்", "author": "சுப்ரமணிய பாரதி", "genre": "காவியம்", "book_no": "TM029", "rack_no": "T9", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB030", "title": "கண்ணன் பாட்டு", "author": "சுப்ரமணிய பாரதி", "genre": "கவிதை", "book_no": "TM030", "rack_no": "T9", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB031", "title": "புதிய ஆத்திசூடி", "author": "சுப்ரமணிய பாரதி", "genre": "நீதி நூல்", "book_no": "TM031", "rack_no": "T10", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB032", "title": "மகாகவி பாரதியார் கவிதைகள்", "author": "சுப்ரமணிய பாரதி", "genre": "கவிதை தொகுப்பு", "book_no": "TM032", "rack_no": "T10", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},

    # Science and Technology in Tamil
    {"id": "TB033", "title": "அறிவியல் அறிமுகம்", "author": "டாக்டர் ஏ.பி.ஜே. அப்துல் கலாம்", "genre": "அறிவியல்", "book_no": "TM033", "rack_no": "T11", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB034", "title": "என் கனவுகளின் இந்தியா", "author": "டாக்டர் ஏ.பி.ஜே. அப்துல் கலாம்", "genre": "சுயசரிதை", "book_no": "TM034", "rack_no": "T11", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB035", "title": "கணிதம் எளிதாக", "author": "பேராசிரியர் கே.ஆர். ராமன்", "genre": "கணிதம்", "book_no": "TM035", "rack_no": "T12", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB036", "title": "இயற்பியல் அறிமுகம்", "author": "டாக்டர் சி.வி. ராமன்", "genre": "இயற்பியல்", "book_no": "TM036", "rack_no": "T12", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB037", "title": "வேதியியல் வழிகாட்டி", "author": "பேராசிரியர் எம்.எஸ். சுவாமிநாதன்", "genre": "வேதியியல்", "book_no": "TM037", "rack_no": "T12", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Modern Tamil Authors - Sujatha
    {"id": "TB038", "title": "பொய்மான்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM038", "rack_no": "T13", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB039", "title": "மீண்டும் ஜீனோ", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM039", "rack_no": "T13", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB040", "title": "கொலை ஆயிரம்", "author": "சுஜாதா", "genre": "துப்பறியும் கதை", "book_no": "TM040", "rack_no": "T13", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB041", "title": "ஜீனோ", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM041", "rack_no": "T13", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB042", "title": "கரோனா", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM042", "rack_no": "T13", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Religious and Spiritual Books
    {"id": "TB043", "title": "திருவாசகம்", "author": "மாணிக்கவாசகர்", "genre": "சமய இலக்கியம்", "book_no": "TM043", "rack_no": "T14", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB044", "title": "தேவாரம்", "author": "திருஞானசம்பந்தர்", "genre": "சமய இலக்கியம்", "book_no": "TM044", "rack_no": "T14", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB045", "title": "திருப்புகழ்", "author": "அருணகிரிநாதர்", "genre": "சமய இலக்கியம்", "book_no": "TM045", "rack_no": "T14", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB046", "title": "கந்த புராணம்", "author": "கச்சியப்ப சிவாசாரியார்", "genre": "புராணம்", "book_no": "TM046", "rack_no": "T14", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Children's Literature
    {"id": "TB047", "title": "பஞ்சதந்திரக் கதைகள்", "author": "விஷ்ணு சர்மா", "genre": "குழந்தைகள் இலக்கியம்", "book_no": "TM047", "rack_no": "T15", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB048", "title": "அக்பர் பீர்பால் கதைகள்", "author": "பல ஆசிரியர்கள்", "genre": "குழந்தைகள் இலக்கியம்", "book_no": "TM048", "rack_no": "T15", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB049", "title": "தெனாலி ராமன் கதைகள்", "author": "பல ஆசிரியர்கள்", "genre": "குழந்தைகள் இலக்கியம்", "book_no": "TM049", "rack_no": "T15", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB050", "title": "விக்ரமாதித்யன் கதைகள்", "author": "பல ஆசிரியர்கள்", "genre": "குழந்தைகள் இலக்கியம்", "book_no": "TM050", "rack_no": "T15", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Contemporary Fiction
    {"id": "TB051", "title": "மயில் விழி", "author": "சிவசங்கரி", "genre": "நாவல்", "book_no": "TM051", "rack_no": "T16", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB052", "title": "நெஞ்சில் ஓர் ஆலயம்", "author": "சிவசங்கரி", "genre": "நாவல்", "book_no": "TM052", "rack_no": "T16", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB053", "title": "தர்மயுத்தம்", "author": "சிவசங்கரி", "genre": "நாவல்", "book_no": "TM053", "rack_no": "T16", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Modern Poetry
    {"id": "TB054", "title": "நகுலன் கவிதைகள்", "author": "நகுலன்", "genre": "நவீன கவிதை", "book_no": "TM054", "rack_no": "T17", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB055", "title": "வைரமுத்து கவிதைகள்", "author": "வைரமுத்து", "genre": "நவீன கவிதை", "book_no": "TM055", "rack_no": "T17", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB056", "title": "கண்ணதாசன் கவிதைகள்", "author": "கண்ணதாசன்", "genre": "நவீன கவிதை", "book_no": "TM056", "rack_no": "T17", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Historical Fiction
    {"id": "TB057", "title": "யவன ராணி", "author": "சாண்டில்யன்", "genre": "வரலாற்று நாவல்", "book_no": "TM057", "rack_no": "T18", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB058", "title": "கடல் புறா", "author": "சாண்டில்யன்", "genre": "வரலாற்று நாவல்", "book_no": "TM058", "rack_no": "T18", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB059", "title": "மன்னவன் வந்தானடி", "author": "சாண்டில்யன்", "genre": "வரலாற்று நாவல்", "book_no": "TM059", "rack_no": "T18", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB060", "title": "சிம்மக்கொடி", "author": "சாண்டில்யன்", "genre": "வரலாற்று நாவல்", "book_no": "TM060", "rack_no": "T18", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Additional Tamil Literature to reach 213 total books
    {"id": "TB061", "title": "பெரிய புராணம்", "author": "சேக்கிழார்", "genre": "சமய இலக்கியம்", "book_no": "TM061", "rack_no": "T19", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB062", "title": "நந்தனார் சரித்திரம்", "author": "கோபால கிருஷ்ண பாரதி", "genre": "சமய இலக்கியம்", "book_no": "TM062", "rack_no": "T19", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB063", "title": "அபிராமி அந்தாதி", "author": "அபிராமி பட்டர்", "genre": "சமய இலக்கியம்", "book_no": "TM063", "rack_no": "T19", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB064", "title": "கந்தர் அலங்காரம்", "author": "குமரகுருபரர்", "genre": "சமய இலக்கியம்", "book_no": "TM064", "rack_no": "T19", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB065", "title": "திருவிளையாடல் புராணம்", "author": "பரஞ்சோதி முனிவர்", "genre": "புராணம்", "book_no": "TM065", "rack_no": "T20", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Modern Tamil Novels
    {"id": "TB066", "title": "உதயணன் கதை", "author": "அகிலன்", "genre": "நாவல்", "book_no": "TM066", "rack_no": "T21", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB067", "title": "சித்திரப்பாவை", "author": "அகிலன்", "genre": "நாவல்", "book_no": "TM067", "rack_no": "T21", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB068", "title": "வேங்கையின் மைந்தன்", "author": "அகிலன்", "genre": "நாவல்", "book_no": "TM068", "rack_no": "T21", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB069", "title": "நெடுஞ்செழியன்", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM069", "rack_no": "T21", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB070", "title": "கயல்விழி", "author": "அகிலன்", "genre": "நாவல்", "book_no": "TM070", "rack_no": "T21", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Tamil Short Stories
    {"id": "TB071", "title": "புதுமைப்பித்தன் கதைகள்", "author": "புதுமைப்பித்தன்", "genre": "சிறுகதை", "book_no": "TM071", "rack_no": "T22", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB072", "title": "ஜெயகாந்தன் கதைகள்", "author": "ஜெயகாந்தன்", "genre": "சிறுகதை", "book_no": "TM072", "rack_no": "T22", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB073", "title": "சுந்தர ராமசாமி கதைகள்", "author": "சுந்தர ராமசாமி", "genre": "சிறுகதை", "book_no": "TM073", "rack_no": "T22", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB074", "title": "ஆர்.கே.நாராயணன் கதைகள்", "author": "ஆர்.கே.நாராயணன்", "genre": "சிறுகதை", "book_no": "TM074", "rack_no": "T22", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB075", "title": "அசோகமித்திரன் கதைகள்", "author": "அசோகமித்திரன்", "genre": "சிறுகதை", "book_no": "TM075", "rack_no": "T22", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Tamil Drama and Theatre
    {"id": "TB076", "title": "மனோன்மணியம்", "author": "பம்மல் சம்பந்த முதலியார்", "genre": "நாடகம்", "book_no": "TM076", "rack_no": "T23", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB077", "title": "சந்திரலேகா", "author": "பாரதியார்", "genre": "நாடகம்", "book_no": "TM077", "rack_no": "T23", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB078", "title": "இந்திரா", "author": "இந்திரா பார்த்தசாரதி", "genre": "நாடகம்", "book_no": "TM078", "rack_no": "T23", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB079", "title": "தென்னாடுடைய சிவனே போற்றி", "author": "இந்திரா பார்த்தசாரதி", "genre": "நாடகம்", "book_no": "TM079", "rack_no": "T23", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB080", "title": "அவ்வையார்", "author": "பாரதிதாசன்", "genre": "நாடகம்", "book_no": "TM080", "rack_no": "T23", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Tamil Essays and Criticism
    {"id": "TB081", "title": "என் சிந்தனைகள்", "author": "பெரியார்", "genre": "கட்டுரை", "book_no": "TM081", "rack_no": "T24", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB082", "title": "தமிழ் இலக்கிய வரலாறு", "author": "மு.வ.அரசு", "genre": "இலக்கிய விமர்சனம்", "book_no": "TM082", "rack_no": "T24", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB083", "title": "தமிழர் நாகரிகம்", "author": "தேவநேயப் பாவாணர்", "genre": "வரலாறு", "book_no": "TM083", "rack_no": "T24", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB084", "title": "தமிழ் மொழியின் வரலாறு", "author": "கா.சு.பிள்ளை", "genre": "மொழியியல்", "book_no": "TM084", "rack_no": "T24", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB085", "title": "சங்க இலக்கிய ஆய்வு", "author": "உ.வே.சாமிநாதையர்", "genre": "இலக்கிய விமர்சனம்", "book_no": "TM085", "rack_no": "T24", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Contemporary Tamil Fiction
    {"id": "TB086", "title": "காவேரியின் கனவு", "author": "இமையம்", "genre": "நாவல்", "book_no": "TM086", "rack_no": "T25", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB087", "title": "கோவேறு கழுதைகள்", "author": "இமையம்", "genre": "நாவல்", "book_no": "TM087", "rack_no": "T25", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB088", "title": "செட்டிநாடு", "author": "இமையம்", "genre": "நாவல்", "book_no": "TM088", "rack_no": "T25", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB089", "title": "பெட்டிக்காடு", "author": "இமையம்", "genre": "நாவல்", "book_no": "TM089", "rack_no": "T25", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB090", "title": "அறம்", "author": "இமையம்", "genre": "நாவல்", "book_no": "TM090", "rack_no": "T25", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Tamil Biographies
    {"id": "TB091", "title": "காந்தியின் சத்தியாக்கிரகம்", "author": "ராஜாஜி", "genre": "சுயசரிதை", "book_no": "TM091", "rack_no": "T26", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB092", "title": "விவேகானந்தர் வாழ்க்கை", "author": "சுவாமி ரங்கநாதானந்தா", "genre": "சுயசரிதை", "book_no": "TM092", "rack_no": "T26", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB093", "title": "பாரதியார் வாழ்க்கை", "author": "வ.ரா.அரசு", "genre": "சுயசரிதை", "book_no": "TM093", "rack_no": "T26", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB094", "title": "பெரியார் வாழ்க்கை", "author": "கே.வீரமணி", "genre": "சுயசரிதை", "book_no": "TM094", "rack_no": "T26", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB095", "title": "அண்ணா வாழ்க்கை", "author": "எம்.கருணாநிதி", "genre": "சுயசரிதை", "book_no": "TM095", "rack_no": "T26", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Tamil Travel Literature
    {"id": "TB096", "title": "யாத்திரை", "author": "ஜெயமோகன்", "genre": "பயண இலக்கியம்", "book_no": "TM096", "rack_no": "T27", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB097", "title": "கைலாச யாத்திரை", "author": "சுஜாதா", "genre": "பயண இலக்கியம்", "book_no": "TM097", "rack_no": "T27", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB098", "title": "ஐரோப்பிய நாடுகள்", "author": "சுந்தர ராமசாமி", "genre": "பயண இலக்கியம்", "book_no": "TM098", "rack_no": "T27", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB099", "title": "அமெரிக்க அனுபவங்கள்", "author": "ஜெயகாந்தன்", "genre": "பயண இலக்கியம்", "book_no": "TM099", "rack_no": "T27", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB100", "title": "ஜப்பான் பயணம்", "author": "அசோகமித்திரன்", "genre": "பயண இலக்கியம்", "book_no": "TM100", "rack_no": "T27", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},

    # Additional Tamil Books to reach 213 total (113 more books)
    {"id": "TB101", "title": "தமிழ் இலக்கிய வரலாறு", "author": "மு.வ.அரசு", "genre": "இலக்கிய விமர்சனம்", "book_no": "TM101", "rack_no": "T28", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB102", "title": "சங்க இலக்கியம்", "author": "உ.வே.சாமிநாதையர்", "genre": "இலக்கிய விமர்சனம்", "book_no": "TM102", "rack_no": "T28", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB103", "title": "தொல்காப்பியம்", "author": "தொல்காப்பியர்", "genre": "இலக்கணம்", "book_no": "TM103", "rack_no": "T28", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB104", "title": "நன்னூல்", "author": "பவணந்தி", "genre": "இலக்கணம்", "book_no": "TM104", "rack_no": "T28", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB105", "title": "வீரசோழியம்", "author": "புத்தமித்திரன்", "genre": "இலக்கணம்", "book_no": "TM105", "rack_no": "T29", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB106", "title": "இலக்கண விளக்கம்", "author": "வைத்தியநாத தேசிகர்", "genre": "இலக்கணம்", "book_no": "TM106", "rack_no": "T29", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB107", "title": "பிரபந்த திரட்டு", "author": "பல ஆசிரியர்கள்", "genre": "சமய இலக்கியம்", "book_no": "TM107", "rack_no": "T29", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB108", "title": "நாலாயிர திவ்ய பிரபந்தம்", "author": "ஆழ்வார்கள்", "genre": "சமய இலக்கியம்", "book_no": "TM108", "rack_no": "T29", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB109", "title": "திருமுறை", "author": "நாயன்மார்கள்", "genre": "சமய இலக்கியம்", "book_no": "TM109", "rack_no": "T30", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB110", "title": "திருமந்திரம்", "author": "திருமூலர்", "genre": "சமய இலக்கியம்", "book_no": "TM110", "rack_no": "T30", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB111", "title": "சிவஞான போதம்", "author": "மெய்கண்ட தேவர்", "genre": "சமய இலக்கியம்", "book_no": "TM111", "rack_no": "T30", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB112", "title": "சிவப்பிரகாசம்", "author": "உமாபதி சிவாசாரியார்", "genre": "சமய இலக்கியம்", "book_no": "TM112", "rack_no": "T30", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB113", "title": "திருவருட்பா", "author": "வள்ளலார்", "genre": "சமய இலக்கியம்", "book_no": "TM113", "rack_no": "T31", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB114", "title": "ஜீவகாருண்ய ஒழுக்கம்", "author": "வள்ளலார்", "genre": "சமய இலக்கியம்", "book_no": "TM114", "rack_no": "T31", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB115", "title": "மனுநீதி சோழன்", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM115", "rack_no": "T31", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB116", "title": "பவானி சங்கரம்", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM116", "rack_no": "T31", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB117", "title": "அமராவதி", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM117", "rack_no": "T32", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB118", "title": "பாண்டிமாதேவி", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM118", "rack_no": "T32", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB119", "title": "சோலைமலை இளவரசி", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM119", "rack_no": "T32", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB120", "title": "கரிகாலன்", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM120", "rack_no": "T32", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB121", "title": "வேங்கையின் மைந்தன்", "author": "அகிலன்", "genre": "வரலாற்று நாவல்", "book_no": "TM121", "rack_no": "T33", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB122", "title": "சிவகாமியின் சபதம்", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM122", "rack_no": "T33", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB123", "title": "பார்த்திபன் கனவு", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM123", "rack_no": "T33", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB124", "title": "அலை ஓசை", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "நாவல்", "book_no": "TM124", "rack_no": "T33", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB125", "title": "தியாக பூமி", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "நாவல்", "book_no": "TM125", "rack_no": "T34", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB126", "title": "கல்கியின் சிறுகதைகள்", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "சிறுகதை", "book_no": "TM126", "rack_no": "T34", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB127", "title": "மோகினி", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "நாவல்", "book_no": "TM127", "rack_no": "T34", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB128", "title": "சபாபதி", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "நாவல்", "book_no": "TM128", "rack_no": "T34", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB129", "title": "பொன்னியின் செல்வன் - பாகம் 6", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM129", "rack_no": "T35", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB130", "title": "பொன்னியின் செல்வன் - பாகம் 7", "author": "கல்கி கிருஷ்ணமூர்த்தி", "genre": "வரலாற்று நாவல்", "book_no": "TM130", "rack_no": "T35", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB131", "title": "வெண்முரசு - பாகம் 4", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM131", "rack_no": "T35", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB132", "title": "வெண்முரசு - பாகம் 5", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM132", "rack_no": "T35", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB133", "title": "வெண்முரசு - பாகம் 6", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM133", "rack_no": "T36", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB134", "title": "வெண்முரசு - பாகம் 7", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM134", "rack_no": "T36", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB135", "title": "வெண்முரசு - பாகம் 8", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM135", "rack_no": "T36", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB136", "title": "வெண்முரசு - பாகம் 9", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM136", "rack_no": "T36", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB137", "title": "வெண்முரசு - பாகம் 10", "author": "ஜெயமோகன்", "genre": "மகாபாரத மறுபதிப்பு", "book_no": "TM137", "rack_no": "T37", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB138", "title": "கொற்றவை - பாகம் 2", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM138", "rack_no": "T37", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB139", "title": "கொற்றவை - பாகம் 3", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM139", "rack_no": "T37", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB140", "title": "ரப்பர் - பாகம் 2", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM140", "rack_no": "T37", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB141", "title": "பின் தொடர்பவன் - பாகம் 2", "author": "ஜெயமோகன்", "genre": "சிறுகதை", "book_no": "TM141", "rack_no": "T38", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB142", "title": "எழாம் உலகம் - பாகம் 2", "author": "ஜெயமோகன்", "genre": "தத்துவம்", "book_no": "TM142", "rack_no": "T38", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB143", "title": "யாத்திரை - பாகம் 2", "author": "ஜெயமோகன்", "genre": "பயண இலக்கியம்", "book_no": "TM143", "rack_no": "T38", "language": "Tamil", "status": "available", "available_copies": 1, "times_taken": 0},
    {"id": "TB144", "title": "விஷ்ணுபுரம்", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM144", "rack_no": "T38", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB145", "title": "கோமான்", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM145", "rack_no": "T39", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB146", "title": "ஆறாம் திணை", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM146", "rack_no": "T39", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB147", "title": "பீஸ்ட்", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM147", "rack_no": "T39", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB148", "title": "கழுதைகள்", "author": "ஜெயமோகன்", "genre": "நாவல்", "book_no": "TM148", "rack_no": "T39", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB149", "title": "ஜெயமோகன் சிறுகதைகள்", "author": "ஜெயமோகன்", "genre": "சிறுகதை", "book_no": "TM149", "rack_no": "T40", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB150", "title": "ஜெயமோகன் கட்டுரைகள்", "author": "ஜெயமோகன்", "genre": "கட்டுரை", "book_no": "TM150", "rack_no": "T40", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Continue adding Tamil books to reach 213 total (63 more books needed)
    {"id": "TB151", "title": "சுஜாதா சிறுகதைகள் - தொகுதி 1", "author": "சுஜாதா", "genre": "சிறுகதை", "book_no": "TM151", "rack_no": "T41", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB152", "title": "சுஜாதா சிறுகதைகள் - தொகுதி 2", "author": "சுஜாதா", "genre": "சிறுகதை", "book_no": "TM152", "rack_no": "T41", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB153", "title": "சுஜாதா சிறுகதைகள் - தொகுதி 3", "author": "சுஜாதா", "genre": "சிறுகதை", "book_no": "TM153", "rack_no": "T41", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB154", "title": "கணினி குமரன்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM154", "rack_no": "T41", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB155", "title": "மெசின்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM155", "rack_no": "T42", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB156", "title": "ஜென்மம்", "author": "சுஜாதா", "genre": "நாவல்", "book_no": "TM156", "rack_no": "T42", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB157", "title": "கொலை ஆயிரம்", "author": "சுஜாதா", "genre": "துப்பறியும் நாவல்", "book_no": "TM157", "rack_no": "T42", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB158", "title": "மீண்டும் ஜீனோ", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM158", "rack_no": "T42", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB159", "title": "என் பெயர் ராணுவம்", "author": "சுஜாதா", "genre": "நாவல்", "book_no": "TM159", "rack_no": "T43", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB160", "title": "காட்மியம்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM160", "rack_no": "T43", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB161", "title": "நியூட்ரான்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM161", "rack_no": "T43", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB162", "title": "ஹைட்ரஜன்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM162", "rack_no": "T43", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB163", "title": "பிளாட்டினம்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM163", "rack_no": "T44", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB164", "title": "ரேடியம்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM164", "rack_no": "T44", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB165", "title": "கார்பன்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM165", "rack_no": "T44", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB166", "title": "சிலிக்கன்", "author": "சுஜாதா", "genre": "அறிவியல் புனைகதை", "book_no": "TM166", "rack_no": "T44", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB167", "title": "பாரதியார் கவிதைகள் - தொகுதி 1", "author": "பாரதியார்", "genre": "கவிதை", "book_no": "TM167", "rack_no": "T45", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB168", "title": "பாரதியார் கவிதைகள் - தொகுதி 2", "author": "பாரதியார்", "genre": "கவிதை", "book_no": "TM168", "rack_no": "T45", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB169", "title": "பாரதியார் கவிதைகள் - தொகுதி 3", "author": "பாரதியார்", "genre": "கவிதை", "book_no": "TM169", "rack_no": "T45", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB170", "title": "பாரதியார் கட்டுரைகள்", "author": "பாரதியார்", "genre": "கட்டுரை", "book_no": "TM170", "rack_no": "T45", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB171", "title": "பாரதியார் கதைகள்", "author": "பாரதியார்", "genre": "சிறுகதை", "book_no": "TM171", "rack_no": "T46", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB172", "title": "பாரதிதாசன் கவிதைகள் - தொகுதி 1", "author": "பாரதிதாசன்", "genre": "கவிதை", "book_no": "TM172", "rack_no": "T46", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB173", "title": "பாரதிதாசன் கவிதைகள் - தொகுதி 2", "author": "பாரதிதாசன்", "genre": "கவிதை", "book_no": "TM173", "rack_no": "T46", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB174", "title": "இசைவாணி", "author": "பாரதிதாசன்", "genre": "கவிதை", "book_no": "TM174", "rack_no": "T46", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB175", "title": "குடும்ப விளக்கு", "author": "பாரதிதாசன்", "genre": "கவிதை", "book_no": "TM175", "rack_no": "T47", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB176", "title": "தமிழியக்கம்", "author": "பாரதிதாசன்", "genre": "கவிதை", "book_no": "TM176", "rack_no": "T47", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB177", "title": "கண்ணதாசன் கவிதைகள் - தொகுதி 1", "author": "கண்ணதாசன்", "genre": "கவிதை", "book_no": "TM177", "rack_no": "T47", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB178", "title": "கண்ணதாசன் கவிதைகள் - தொகுதி 2", "author": "கண்ணதாசன்", "genre": "கவிதை", "book_no": "TM178", "rack_no": "T47", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB179", "title": "கண்ணதாசன் கவிதைகள் - தொகுதி 3", "author": "கண்ணதாசன்", "genre": "கவிதை", "book_no": "TM179", "rack_no": "T48", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB180", "title": "அர்த்தமுள்ள இந்து மதம்", "author": "கண்ணதாசன்", "genre": "சமய இலக்கியம்", "book_no": "TM180", "rack_no": "T48", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB181", "title": "வைரமுத்து கவிதைகள் - தொகுதி 1", "author": "வைரமுத்து", "genre": "கவிதை", "book_no": "TM181", "rack_no": "T48", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB182", "title": "வைரமுத்து கவிதைகள் - தொகுதி 2", "author": "வைரமுத்து", "genre": "கவிதை", "book_no": "TM182", "rack_no": "T48", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0},
    {"id": "TB183", "title": "கலைஞர் கவிதைகள்", "author": "கலைஞர் கருணாநிதி", "genre": "கவிதை", "book_no": "TM183", "rack_no": "T49", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB184", "title": "கலைஞர் நாடகங்கள்", "author": "கலைஞர் கருணாநிதி", "genre": "நாடகம்", "book_no": "TM184", "rack_no": "T49", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB185", "title": "கலைஞர் கதைகள்", "author": "கலைஞர் கருணாநிதி", "genre": "சிறுகதை", "book_no": "TM185", "rack_no": "T49", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB186", "title": "நா.பார்த்தசாரதி கவிதைகள்", "author": "நா.பார்த்தசாரதி", "genre": "கவிதை", "book_no": "TM186", "rack_no": "T49", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB187", "title": "சிற்பி கதைகள்", "author": "சிற்பி", "genre": "சிறுகதை", "book_no": "TM187", "rack_no": "T50", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB188", "title": "சிற்பி நாவல்கள்", "author": "சிற்பி", "genre": "நாவல்", "book_no": "TM188", "rack_no": "T50", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB189", "title": "ல.ச.ராமாமிர்தம் கதைகள்", "author": "ல.ச.ராமாமிர்தம்", "genre": "சிறுகதை", "book_no": "TM189", "rack_no": "T50", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB190", "title": "ல.ச.ராமாமிர்தம் நாவல்கள்", "author": "ல.ச.ராமாமிர்தம்", "genre": "நாவல்", "book_no": "TM190", "rack_no": "T50", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB191", "title": "தி.ஜானகிராமன் கதைகள்", "author": "தி.ஜானகிராமன்", "genre": "சிறுகதை", "book_no": "TM191", "rack_no": "T51", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB192", "title": "தி.ஜானகிராமன் நாவல்கள்", "author": "தி.ஜானகிராமன்", "genre": "நாவல்", "book_no": "TM192", "rack_no": "T51", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB193", "title": "ரா.கி.ரங்கராஜன் கதைகள்", "author": "ரா.கி.ரங்கராஜன்", "genre": "சிறுகதை", "book_no": "TM193", "rack_no": "T51", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB194", "title": "ரா.கி.ரங்கராஜன் நாவல்கள்", "author": "ரா.கி.ரங்கராஜன்", "genre": "நாவல்", "book_no": "TM194", "rack_no": "T51", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB195", "title": "கு.அழகிரிசாமி கதைகள்", "author": "கு.அழகிரிசாமி", "genre": "சிறுகதை", "book_no": "TM195", "rack_no": "T52", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB196", "title": "கு.அழகிரிசாமி நாவல்கள்", "author": "கு.அழகிரிசாமி", "genre": "நாவல்", "book_no": "TM196", "rack_no": "T52", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB197", "title": "மு.வரதராசனார் கதைகள்", "author": "மு.வரதராசனார்", "genre": "சிறுகதை", "book_no": "TM197", "rack_no": "T52", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB198", "title": "மு.வரதராசனார் நாவல்கள்", "author": "மு.வரதராசனார்", "genre": "நாவல்", "book_no": "TM198", "rack_no": "T52", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB199", "title": "வ.வே.சு.ஐயர் கதைகள்", "author": "வ.வே.சு.ஐயர்", "genre": "சிறுகதை", "book_no": "TM199", "rack_no": "T53", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB200", "title": "வ.வே.சு.ஐயர் நாவல்கள்", "author": "வ.வே.சு.ஐயர்", "genre": "நாவல்", "book_no": "TM200", "rack_no": "T53", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},

    # Final 13 Tamil books to reach exactly 213
    {"id": "TB201", "title": "பெருமாள் முருகன் கதைகள்", "author": "பெருமாள் முருகன்", "genre": "சிறுகதை", "book_no": "TM201", "rack_no": "T53", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB202", "title": "பெருமாள் முருகன் நாவல்கள்", "author": "பெருமாள் முருகன்", "genre": "நாவல்", "book_no": "TM202", "rack_no": "T53", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB203", "title": "சோ.தர்மன் கதைகள்", "author": "சோ.தர்மன்", "genre": "சிறுகதை", "book_no": "TM203", "rack_no": "T54", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB204", "title": "சோ.தர்மன் நாவல்கள்", "author": "சோ.தர்மன்", "genre": "நாவல்", "book_no": "TM204", "rack_no": "T54", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB205", "title": "எஸ்.ராமகிருஷ்ணன் கதைகள்", "author": "எஸ்.ராமகிருஷ்ணன்", "genre": "சிறுகதை", "book_no": "TM205", "rack_no": "T54", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB206", "title": "எஸ்.ராமகிருஷ்ணன் நாவல்கள்", "author": "எஸ்.ராமகிருஷ்ணன்", "genre": "நாவல்", "book_no": "TM206", "rack_no": "T54", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB207", "title": "சுகிர்தராணி கதைகள்", "author": "சுகிர்தராணி", "genre": "சிறுகதை", "book_no": "TM207", "rack_no": "T55", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB208", "title": "சுகிர்தராணி நாவல்கள்", "author": "சுகிர்தராணி", "genre": "நாவல்", "book_no": "TM208", "rack_no": "T55", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB209", "title": "அம்பை கதைகள்", "author": "அம்பை", "genre": "சிறுகதை", "book_no": "TM209", "rack_no": "T55", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB210", "title": "அம்பை நாவல்கள்", "author": "அம்பை", "genre": "நாவல்", "book_no": "TM210", "rack_no": "T55", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB211", "title": "மலர்மன்னன் கதைகள்", "author": "மலர்மன்னன்", "genre": "சிறுகதை", "book_no": "TM211", "rack_no": "T56", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB212", "title": "மலர்மன்னன் நாவல்கள்", "author": "மலர்மன்னன்", "genre": "நாவல்", "book_no": "TM212", "rack_no": "T56", "language": "Tamil", "status": "available", "available_copies": 2, "times_taken": 0},
    {"id": "TB213", "title": "தமிழ் இலக்கிய களஞ்சியம்", "author": "பல ஆசிரியர்கள்", "genre": "தொகுப்பு", "book_no": "TM213", "rack_no": "T56", "language": "Tamil", "status": "available", "available_copies": 3, "times_taken": 0}
]

# Add language field to existing English books
for book in BOOKS:
    if 'language' not in book:
        book['language'] = 'English'

# Combine all books
ALL_BOOKS = BOOKS + TAMIL_BOOKS

# Feedback system storage
FEEDBACK = []

# Book purchase requests
PURCHASE_REQUESTS = []

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Smart Library API - Enhanced with Admin Features',
        'timestamp': datetime.now().isoformat(),
        'features': [
            'Employee Authentication',
            'Book Management',
            'Admin Dashboard',
            'Feedback System',
            'Purchase Requests',
            'Analytics'
        ],
        'employees_count': len(EMPLOYEES),
        'books_count': len(BOOKS),
        'feedback_count': len(FEEDBACK),
        'purchase_requests_count': len(PURCHASE_REQUESTS)
    })

@app.route('/login', methods=['POST'])
def login():
    """Employee login with name and Employee ID"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        employee_id = data.get('employee_id', '').strip()

        if not name or not employee_id:
            return jsonify({
                'status': 'error',
                'message': 'Employee name and Employee ID are required'
            }), 400

        # Admin login
        if name.lower() == 'system administrator' and employee_id == 'ADMIN001':
            return jsonify({
                'status': 'success',
                'message': 'Admin login successful',
                'employee': {
                    'id': 0,
                    'name': 'System Administrator',
                    'phone': '1234567890',
                    'department': 'Administration',
                    'employee_id': 'ADMIN001',
                    'email': 'admin@library.com',
                    'role': 'admin'
                }
            })
        
        # Find employee by name and employee_id (case-insensitive name)
        for emp in EMPLOYEES:
            if emp['name'].lower() == name.lower() and emp['employee_id'] == employee_id:
                emp['role'] = 'employee'  # Add role for frontend
                return jsonify({
                    'status': 'success',
                    'message': 'Login successful',
                    'employee': emp
                })
        
        # If not found, provide helpful error message
        name_matches = []
        for emp in EMPLOYEES:
            if emp['name'].lower() == name.lower():
                name_matches.append(emp['employee_id'])

        if name_matches:
            return jsonify({
                'status': 'error',
                'message': f'Employee "{name}" found but Employee ID "{employee_id}" does not match. Expected Employee ID: {name_matches[0]}'
            }), 401
        else:
            return jsonify({
                'status': 'error',
                'message': f'Employee "{name}" not found. Please check the spelling.'
            }), 401
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Login failed: {str(e)}'
        }), 500

@app.route('/books', methods=['GET'])
def get_books():
    """Get all books with enhanced filtering (English and Tamil)"""
    try:
        search = request.args.get('search', '').lower()
        sort_by = request.args.get('sort', 'title')
        filter_status = request.args.get('status', 'all')
        language = request.args.get('language', 'all').lower()

        # Update days remaining for taken books
        today = datetime.now()

        for book in ALL_BOOKS:
            if book['status'] == 'taken' and 'due_date' in book:
                due_date = datetime.strptime(book['due_date'], '%Y-%m-%d')
                days_remaining = (due_date - today).days
                book['days_remaining'] = days_remaining

                if days_remaining < 0:
                    book['status'] = 'overdue'
                    book['days_overdue'] = abs(days_remaining)

        # Filter books by language first
        if language == 'tamil':
            filtered_books = [book for book in ALL_BOOKS if book.get('language', '').lower() == 'tamil']
        elif language == 'english':
            filtered_books = [book for book in ALL_BOOKS if book.get('language', '').lower() == 'english']
        else:
            filtered_books = ALL_BOOKS
        
        if search:
            filtered_books = [
                book for book in filtered_books
                if (search in book['title'].lower() or 
                    search in book['author'].lower() or
                    search in book['genre'].lower())
            ]
        
        if filter_status != 'all':
            filtered_books = [
                book for book in filtered_books
                if book['status'] == filter_status
            ]
        
        # Sort books
        if sort_by == 'title':
            filtered_books.sort(key=lambda x: x['title'].lower())
        elif sort_by == 'author':
            filtered_books.sort(key=lambda x: x['author'].lower())
        elif sort_by == 'genre':
            filtered_books.sort(key=lambda x: x['genre'].lower())
        elif sort_by == 'popularity':
            filtered_books.sort(key=lambda x: x.get('times_taken', 0), reverse=True)
        
        return jsonify({
            'status': 'success',
            'books': filtered_books,
            'total_books': len(BOOKS),
            'filtered_count': len(filtered_books)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get books: {str(e)}'
        }), 500

@app.route('/take-book', methods=['POST'])
def take_book():
    """Mark a book as taken with date tracking"""
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        book_id = data.get('book_id')
        employee_name = data.get('employee_name', 'Unknown')
        
        if not employee_id or not book_id:
            return jsonify({
                'status': 'error',
                'message': 'Employee ID and Book ID are required'
            }), 400
        
        # Find book in ALL_BOOKS (English and Tamil)
        book = None
        for b in ALL_BOOKS:
            if b['id'] == book_id:
                book = b
                break
        
        if not book:
            return jsonify({
                'status': 'error',
                'message': 'Book not found'
            }), 404
        
        if book['status'] != 'available':
            return jsonify({
                'status': 'error',
                'message': 'Book is not available'
            }), 400

        # Check employee restrictions
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        # Count books currently held by employee and monthly takings
        books_currently_held = 0
        books_taken_this_month = 0

        for b in BOOKS:
            # Count currently held books
            if str(b.get('taken_by_employee_id')) == str(employee_id) and b['status'] == 'taken':
                books_currently_held += 1

            # Count ALL book taking instances this month (including re-takings)
            if 'monthly_history' in b:
                for history in b['monthly_history']:
                    if (str(history.get('employee_id')) == str(employee_id) and
                        history.get('month') == current_month and
                        history.get('year') == current_year):
                        books_taken_this_month += 1

            # Also check current taking if it's this month
            elif str(b.get('taken_by_employee_id')) == str(employee_id):
                if b.get('taken_date'):
                    taken_date = datetime.strptime(b['taken_date'], '%Y-%m-%d')
                    if taken_date.month == current_month and taken_date.year == current_year:
                        books_taken_this_month += 1

        # Restriction 1: Maximum 2 books at a time
        if books_currently_held >= 2:
            return jsonify({
                'status': 'error',
                'message': 'You can only hold 2 books at a time. Please return a book first.'
            }), 400

        # Restriction 2: Maximum 2 books per month
        if books_taken_this_month >= 2:
            return jsonify({
                'status': 'error',
                'message': 'You have reached your monthly limit of 2 books. Please wait for next month.'
            }), 400
        
        # Calculate dates (14-day loan period)
        taken_date = datetime.now()
        due_date = taken_date + timedelta(days=14)
        
        # Update book status with tracking info
        book['status'] = 'taken'
        book['taken_by'] = employee_name
        book['taken_by_employee_id'] = employee_id  # Keep as string to match employee data
        book['taken_by_name'] = employee_name
        book['taken_date'] = taken_date.strftime('%Y-%m-%d')
        book['due_date'] = due_date.strftime('%Y-%m-%d')
        book['days_remaining'] = 14

        # Track book popularity and reduce available count
        if 'times_taken' not in book:
            book['times_taken'] = 0
        book['times_taken'] += 1

        # Track monthly taking history for this employee
        if 'monthly_history' not in book:
            book['monthly_history'] = []

        book['monthly_history'].append({
            'employee_id': employee_id,  # Keep as string
            'employee_name': employee_name,
            'taken_date': taken_date.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'month': taken_date.month,
            'year': taken_date.year
        })

        # Reduce available count (if book has copies)
        if 'available_copies' in book and book['available_copies'] > 0:
            book['available_copies'] -= 1

        print(f"📚 Book '{book['title']}' taken by {employee_name} (ID: {employee_id})")
        print(f"📅 Due date: {book['due_date']} (14 days from now)")
        print(f"📊 Total times taken: {book['times_taken']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Book taken successfully',
            'book': {
                'id': book['id'],
                'title': book['title'],
                'taken_date': book['taken_date'],
                'due_date': book['due_date'],
                'days_remaining': 14,
                'monthly_history': book.get('monthly_history', [])
            },
            'employee_stats': {
                'books_currently_held': books_currently_held + 1,
                'books_taken_this_month': books_taken_this_month + 1,
                'monthly_limit': 2
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to take book: {str(e)}'
        }), 500

@app.route('/return-book', methods=['POST'])
def return_book():
    """Return a book"""
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        
        if not book_id:
            return jsonify({
                'status': 'error',
                'message': 'Book ID is required'
            }), 400
        
        # Find book
        book = None
        for b in BOOKS:
            if b['id'] == book_id:
                book = b
                break
        
        if not book:
            return jsonify({
                'status': 'error',
                'message': 'Book not found'
            }), 404
        
        if book['status'] == 'available':
            return jsonify({
                'status': 'error',
                'message': 'Book is already available'
            }), 400
        
        # Return book and increase available count
        returned_by = book.get('taken_by_name', 'Unknown')
        returned_by_id = book.get('taken_by_employee_id', None)

        # Store last borrower info for re-taking capability
        book['last_taken_by_name'] = returned_by
        book['last_taken_by_employee_id'] = returned_by_id
        book['last_taken_date'] = book.get('taken_date')
        book['last_due_date'] = book.get('due_date')

        # Clear current borrowing info
        book['status'] = 'available'
        book.pop('taken_by', None)
        book.pop('taken_by_employee_id', None)
        book.pop('taken_by_name', None)
        book.pop('employee_id', None)
        book.pop('taken_date', None)
        book.pop('due_date', None)
        book.pop('days_remaining', None)
        book.pop('days_overdue', None)
        book['return_date'] = datetime.now().strftime('%Y-%m-%d')

        # Increase available count (if book has copies tracking)
        if 'available_copies' in book:
            book['available_copies'] += 1

        print(f"📚 Book '{book['title']}' returned by {returned_by}")
        print(f"📅 Return date: {book['return_date']}")

        return jsonify({
            'status': 'success',
            'message': 'Book returned successfully',
            'book': {
                'title': book['title'],
                'return_date': book['return_date']
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to return book: {str(e)}'
        }), 500

@app.route('/renew-book', methods=['POST'])
def renew_book():
    """Renew a book for another 14 days"""
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        
        if not book_id:
            return jsonify({
                'status': 'error',
                'message': 'Book ID is required'
            }), 400
        
        # Find book
        book = None
        for b in BOOKS:
            if b['id'] == book_id:
                book = b
                break
        
        if not book:
            return jsonify({
                'status': 'error',
                'message': 'Book not found'
            }), 404
        
        if book['status'] not in ['taken', 'overdue']:
            return jsonify({
                'status': 'error',
                'message': 'Book is not currently taken'
            }), 400
        
        # Renew book for another 14 days
        new_due_date = datetime.now() + timedelta(days=14)
        
        book['status'] = 'taken'
        book['due_date'] = new_due_date.strftime('%Y-%m-%d')
        book['days_remaining'] = 14
        book.pop('days_overdue', None)
        
        return jsonify({
            'status': 'success',
            'message': 'Book renewed successfully',
            'new_due_date': book['due_date']
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to renew book: {str(e)}'
        }), 500

# ============ ADVANCED BOOK SEARCH ============

@app.route('/books/search', methods=['GET'])
def search_books():
    """Search books by name or ID (English and Tamil)"""
    try:
        query = request.args.get('q', '').lower().strip()
        language = request.args.get('language', 'all').lower()

        if not query:
            return jsonify({
                "status": "success",
                "books": [],
                "total_count": 0
            })

        # Filter books by language first
        books_to_search = ALL_BOOKS
        if language == 'tamil':
            books_to_search = [book for book in ALL_BOOKS if book.get('language', '').lower() == 'tamil']
        elif language == 'english':
            books_to_search = [book for book in ALL_BOOKS if book.get('language', '').lower() == 'english']

        # Search in book title, author, book_no, or genre (supports Tamil text)
        matching_books = []
        for book in books_to_search:
            if (query in book.get('title', '').lower() or
                query in book.get('author', '').lower() or
                query in book.get('book_no', '').lower() or
                query in book.get('genre', '').lower()):
                matching_books.append(book)

        return jsonify({
            "status": "success",
            "books": matching_books,
            "total_count": len(matching_books),
            "language_filter": language
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Search failed: {str(e)}"
        }), 500

@app.route('/employee/<employee_id>/books', methods=['GET'])
def get_employee_books(employee_id):
    """Get books taken by specific employee (current and previously returned)"""
    try:
        employee_books = []

        # Find books currently taken by this employee OR previously taken by them
        for book in BOOKS:
            # Check if currently taken by this employee
            if str(book.get('taken_by_employee_id')) == str(employee_id):
                employee_books.append(book)
            # Check if previously taken by this employee (in history)
            elif hasattr(book, 'history') and book.get('history'):
                for history_entry in book['history']:
                    if str(history_entry.get('employee_id')) == str(employee_id):
                        # Create a copy of the book with history info
                        historical_book = book.copy()
                        historical_book.update(history_entry)
                        employee_books.append(historical_book)
                        break
            # Check if book has return_date and was taken by this employee
            elif (book.get('return_date') and
                  str(book.get('last_taken_by_employee_id')) == str(employee_id)):
                employee_books.append(book)

        # Remove duplicates based on book ID
        seen_books = set()
        unique_books = []
        for book in employee_books:
            if book['id'] not in seen_books:
                seen_books.add(book['id'])
                unique_books.append(book)

        return jsonify({
            "status": "success",
            "books": unique_books,
            "total_count": len(unique_books)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to get employee books: {str(e)}"
        }), 500

# ============ FEEDBACK SYSTEM ============

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback or book purchase request"""
    try:
        data = request.get_json()
        employee_name = data.get('employee_name', '')
        employee_id = data.get('employee_id', '')
        feedback_type = data.get('type', 'general')  # general, book_request, complaint, suggestion
        title = data.get('title', '')
        message = data.get('message', '')
        book_details = data.get('book_details', {})  # For book requests

        if not employee_name or not message:
            return jsonify({
                'status': 'error',
                'message': 'Employee name and message are required'
            }), 400

        feedback_id = str(uuid.uuid4())
        feedback_entry = {
            'id': feedback_id,
            'employee_name': employee_name,
            'employee_id': employee_id,
            'type': feedback_type,
            'title': title,
            'message': message,
            'book_details': book_details,
            'status': 'pending',  # pending, reviewed, approved, rejected
            'submitted_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'admin_response': '',
            'admin_response_date': ''
        }

        FEEDBACK.append(feedback_entry)

        # If it's a book request, also add to purchase requests
        if feedback_type == 'book_request' and book_details:
            purchase_request = {
                'id': str(uuid.uuid4()),
                'feedback_id': feedback_id,
                'requested_by': employee_name,
                'employee_id': employee_id,
                'book_title': book_details.get('title', ''),
                'book_author': book_details.get('author', ''),
                'book_genre': book_details.get('genre', ''),
                'reason': message,
                'status': 'pending',  # pending, approved, ordered, rejected
                'requested_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'priority': book_details.get('priority', 'medium')  # low, medium, high
            }
            PURCHASE_REQUESTS.append(purchase_request)

        return jsonify({
            'status': 'success',
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback_id
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to submit feedback: {str(e)}'
        }), 500

@app.route('/feedback', methods=['GET'])
def get_feedback():
    """Get all feedback (admin only)"""
    try:
        feedback_type = request.args.get('type', 'all')
        status = request.args.get('status', 'all')

        filtered_feedback = FEEDBACK

        if feedback_type != 'all':
            filtered_feedback = [f for f in filtered_feedback if f['type'] == feedback_type]

        if status != 'all':
            filtered_feedback = [f for f in filtered_feedback if f['status'] == status]

        # Sort by date (newest first)
        filtered_feedback.sort(key=lambda x: x['submitted_date'], reverse=True)

        return jsonify({
            'status': 'success',
            'feedback': filtered_feedback,
            'total_count': len(FEEDBACK),
            'filtered_count': len(filtered_feedback)
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get feedback: {str(e)}'
        }), 500

@app.route('/feedback/<feedback_id>/respond', methods=['POST'])
def respond_to_feedback(feedback_id):
    """Admin response to feedback"""
    try:
        data = request.get_json()
        admin_response = data.get('response', '')
        new_status = data.get('status', 'reviewed')

        if not admin_response:
            return jsonify({
                'status': 'error',
                'message': 'Admin response is required'
            }), 400

        # Find feedback
        feedback = None
        for f in FEEDBACK:
            if f['id'] == feedback_id:
                feedback = f
                break

        if not feedback:
            return jsonify({
                'status': 'error',
                'message': 'Feedback not found'
            }), 404

        # Update feedback
        feedback['admin_response'] = admin_response
        feedback['status'] = new_status
        feedback['admin_response_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return jsonify({
            'status': 'success',
            'message': 'Response added successfully'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to respond to feedback: {str(e)}'
        }), 500

# ============ ADMIN BOOK MANAGEMENT ============

@app.route('/admin/books', methods=['GET'])
def admin_get_books():
    """Get all books with admin details"""
    try:
        return jsonify({
            'status': 'success',
            'books': BOOKS,
            'total_count': len(BOOKS)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get books: {str(e)}'
        }), 500

@app.route('/admin/books', methods=['POST'])
def admin_add_book():
    """Add a new book"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        genre = data.get('genre', '').strip()
        rack_no = data.get('rack_no', '').strip()
        book_no = data.get('book_no', '').strip()

        if not title or not author:
            return jsonify({
                'status': 'error',
                'message': 'Title and author are required'
            }), 400

        # Generate new book ID
        new_id = max([book['id'] for book in BOOKS]) + 1 if BOOKS else 1

        new_book = {
            'id': new_id,
            'title': title,
            'author': author,
            'genre': genre or 'General',
            'rack_no': rack_no or f'R{new_id}',
            'book_no': book_no or f'B{new_id:04d}',
            'status': 'available',
            'times_taken': 0,
            'added_date': datetime.now().strftime('%Y-%m-%d')
        }

        BOOKS.append(new_book)

        return jsonify({
            'status': 'success',
            'message': 'Book added successfully',
            'book': new_book
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to add book: {str(e)}'
        }), 500

@app.route('/admin/books/<int:book_id>', methods=['PUT'])
def admin_update_book(book_id):
    """Update a book"""
    try:
        data = request.get_json()

        # Find book
        book = None
        for b in BOOKS:
            if b['id'] == book_id:
                book = b
                break

        if not book:
            return jsonify({
                'status': 'error',
                'message': 'Book not found'
            }), 404

        # Update book fields
        if 'title' in data:
            book['title'] = data['title'].strip()
        if 'author' in data:
            book['author'] = data['author'].strip()
        if 'genre' in data:
            book['genre'] = data['genre'].strip()
        if 'rack_no' in data:
            book['rack_no'] = data['rack_no'].strip()
        if 'book_no' in data:
            book['book_no'] = data['book_no'].strip()

        book['updated_date'] = datetime.now().strftime('%Y-%m-%d')

        return jsonify({
            'status': 'success',
            'message': 'Book updated successfully',
            'book': book
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to update book: {str(e)}'
        }), 500

@app.route('/admin/books/<int:book_id>', methods=['DELETE'])
def admin_delete_book(book_id):
    """Delete a book"""
    try:
        # Find book
        book_index = None
        for i, book in enumerate(BOOKS):
            if book['id'] == book_id:
                book_index = i
                break

        if book_index is None:
            return jsonify({
                'status': 'error',
                'message': 'Book not found'
            }), 404

        # Check if book is currently taken
        book = BOOKS[book_index]
        if book['status'] in ['taken', 'overdue']:
            return jsonify({
                'status': 'error',
                'message': 'Cannot delete book that is currently taken'
            }), 400

        # Remove book
        deleted_book = BOOKS.pop(book_index)

        return jsonify({
            'status': 'success',
            'message': 'Book deleted successfully',
            'deleted_book': deleted_book
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete book: {str(e)}'
        }), 500

# ============ PURCHASE REQUESTS MANAGEMENT ============

@app.route('/purchase-requests', methods=['GET'])
def get_purchase_requests():
    """Get all book purchase requests"""
    try:
        status = request.args.get('status', 'all')

        filtered_requests = PURCHASE_REQUESTS

        if status != 'all':
            filtered_requests = [r for r in filtered_requests if r['status'] == status]

        # Sort by date (newest first)
        filtered_requests.sort(key=lambda x: x['requested_date'], reverse=True)

        return jsonify({
            'status': 'success',
            'purchase_requests': filtered_requests,
            'total_count': len(PURCHASE_REQUESTS),
            'filtered_count': len(filtered_requests)
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get purchase requests: {str(e)}'
        }), 500

@app.route('/purchase-requests/<request_id>/update', methods=['POST'])
def update_purchase_request(request_id):
    """Update purchase request status"""
    try:
        data = request.get_json()
        new_status = data.get('status', '')
        admin_notes = data.get('admin_notes', '')

        if not new_status:
            return jsonify({
                'status': 'error',
                'message': 'Status is required'
            }), 400

        # Find purchase request
        request_item = None
        for r in PURCHASE_REQUESTS:
            if r['id'] == request_id:
                request_item = r
                break

        if not request_item:
            return jsonify({
                'status': 'error',
                'message': 'Purchase request not found'
            }), 404

        # Update request
        request_item['status'] = new_status
        request_item['admin_notes'] = admin_notes
        request_item['updated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # If approved, optionally add the book to library
        if new_status == 'approved' and data.get('add_to_library', False):
            new_id = max([book['id'] for book in BOOKS]) + 1 if BOOKS else 1
            new_book = {
                'id': new_id,
                'title': request_item['book_title'],
                'author': request_item['book_author'],
                'genre': request_item['book_genre'] or 'General',
                'rack_no': f'R{new_id}',
                'book_no': f'B{new_id:04d}',
                'status': 'available',
                'times_taken': 0,
                'added_date': datetime.now().strftime('%Y-%m-%d'),
                'requested_by': request_item['requested_by']
            }
            BOOKS.append(new_book)
            request_item['book_added'] = True
            request_item['book_id'] = new_id

        return jsonify({
            'status': 'success',
            'message': 'Purchase request updated successfully',
            'request': request_item
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to update purchase request: {str(e)}'
        }), 500

# ============ EMPLOYEES ENDPOINT ============

@app.route('/employees', methods=['GET'])
def get_employees():
    """Get all employees for admin dashboard"""
    try:
        return jsonify({
            'status': 'success',
            'employees': EMPLOYEES,
            'total_count': len(EMPLOYEES)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get employees: {str(e)}'
        }), 500

# ============ ADMIN ANALYTICS ============

@app.route('/admin/data', methods=['GET'])
def get_admin_data():
    """Get admin dashboard data"""
    try:
        # Calculate book status
        available_books = len([b for b in ALL_BOOKS if not b.get('taken_by')])
        taken_books = len([b for b in ALL_BOOKS if b.get('taken_by')])

        # Calculate language distribution
        english_books = len([b for b in ALL_BOOKS if b.get('language') == 'English'])
        tamil_books = len([b for b in ALL_BOOKS if b.get('language') == 'Tamil'])

        # Calculate employee activity
        active_employees = len([e for e in EMPLOYEES if e.get('books_taken', 0) > 0])
        inactive_employees = len(EMPLOYEES) - active_employees

        return jsonify({
            'status': 'success',
            'book_status': {
                'available': available_books,
                'unavailable': taken_books
            },
            'language_distribution': {
                'english': english_books,
                'tamil': tamil_books
            },
            'employee_activity': {
                'active': active_employees,
                'inactive': inactive_employees
            },
            'total_books': len(ALL_BOOKS),
            'total_employees': len(EMPLOYEES)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get admin data: {str(e)}'
        }), 500

@app.route('/admin/analytics', methods=['GET'])
def get_admin_analytics():
    """Get comprehensive admin analytics"""
    try:
        today = datetime.now()

        # Update book statuses
        for book in BOOKS:
            if book['status'] == 'taken' and 'due_date' in book:
                due_date = datetime.strptime(book['due_date'], '%Y-%m-%d')
                days_remaining = (due_date - today).days
                if days_remaining < 0:
                    book['status'] = 'overdue'
                    book['days_overdue'] = abs(days_remaining)

        # Basic book statistics
        total_books = len(BOOKS)
        available_books = len([b for b in BOOKS if b['status'] == 'available'])
        taken_books = len([b for b in BOOKS if b['status'] == 'taken'])
        overdue_books = len([b for b in BOOKS if b['status'] == 'overdue'])

        # Genre statistics
        genre_stats = {}
        for book in BOOKS:
            genre = book['genre']
            if genre not in genre_stats:
                genre_stats[genre] = {'total': 0, 'available': 0, 'taken': 0, 'overdue': 0, 'popularity': 0}

            genre_stats[genre]['total'] += 1
            genre_stats[genre][book['status']] += 1
            genre_stats[genre]['popularity'] += book.get('times_taken', 0)

        # Most popular books
        popular_books = sorted(
            [b for b in BOOKS if b.get('times_taken', 0) > 0],
            key=lambda x: x.get('times_taken', 0),
            reverse=True
        )[:10]

        # Books due for renewal
        due_for_renewal = []
        for book in BOOKS:
            if book['status'] == 'taken' and 'due_date' in book:
                due_date = datetime.strptime(book['due_date'], '%Y-%m-%d')
                days_remaining = (due_date - today).days
                if 0 <= days_remaining <= 3:
                    due_for_renewal.append({
                        'id': book['id'],
                        'title': book['title'],
                        'taken_by': book.get('taken_by', 'Unknown'),
                        'due_date': book['due_date'],
                        'days_remaining': days_remaining
                    })

        # Feedback statistics
        feedback_stats = {
            'total': len(FEEDBACK),
            'pending': len([f for f in FEEDBACK if f['status'] == 'pending']),
            'reviewed': len([f for f in FEEDBACK if f['status'] == 'reviewed']),
            'by_type': {}
        }

        for feedback in FEEDBACK:
            feedback_type = feedback['type']
            if feedback_type not in feedback_stats['by_type']:
                feedback_stats['by_type'][feedback_type] = 0
            feedback_stats['by_type'][feedback_type] += 1

        # Purchase request statistics
        purchase_stats = {
            'total': len(PURCHASE_REQUESTS),
            'pending': len([r for r in PURCHASE_REQUESTS if r['status'] == 'pending']),
            'approved': len([r for r in PURCHASE_REQUESTS if r['status'] == 'approved']),
            'rejected': len([r for r in PURCHASE_REQUESTS if r['status'] == 'rejected'])
        }

        # Employee book tracking
        employees_with_books = []
        employee_book_count = {}
        department_book_stats = {}

        for book in BOOKS:
            if book['status'] in ['taken', 'overdue'] and 'employee_id' in book:
                # Find employee details
                employee_info = None
                for emp in EMPLOYEES:
                    if emp['employee_id'] == book['employee_id']:
                        employee_info = emp
                        break

                if employee_info:
                    # Track employee with book details
                    employee_with_book = {
                        'employee_name': book.get('taken_by', employee_info['name']),
                        'employee_id': book['employee_id'],
                        'department': employee_info['department'],
                        'phone': employee_info['phone'],
                        'book_title': book['title'],
                        'book_author': book['author'],
                        'book_genre': book['genre'],
                        'taken_date': book.get('taken_date', ''),
                        'due_date': book.get('due_date', ''),
                        'days_remaining': book.get('days_remaining', 0),
                        'status': book['status'],
                        'book_id': book['id']
                    }
                    employees_with_books.append(employee_with_book)

                    # Count books per employee
                    emp_key = f"{employee_info['name']} ({book['employee_id']})"
                    if emp_key not in employee_book_count:
                        employee_book_count[emp_key] = {
                            'employee_name': employee_info['name'],
                            'employee_id': book['employee_id'],
                            'department': employee_info['department'],
                            'phone': employee_info['phone'],
                            'books_count': 0,
                            'books': []
                        }

                    employee_book_count[emp_key]['books_count'] += 1
                    employee_book_count[emp_key]['books'].append({
                        'title': book['title'],
                        'author': book['author'],
                        'due_date': book.get('due_date', ''),
                        'status': book['status'],
                        'days_remaining': book.get('days_remaining', 0)
                    })

                    # Department statistics
                    dept = employee_info['department']
                    if dept not in department_book_stats:
                        department_book_stats[dept] = {
                            'total_employees': 0,
                            'employees_with_books': 0,
                            'total_books_taken': 0,
                            'overdue_books': 0
                        }

                    department_book_stats[dept]['total_books_taken'] += 1
                    if book['status'] == 'overdue':
                        department_book_stats[dept]['overdue_books'] += 1

        # Count total employees per department and employees with books
        for emp in EMPLOYEES:
            dept = emp['department']
            if dept not in department_book_stats:
                department_book_stats[dept] = {
                    'total_employees': 0,
                    'employees_with_books': 0,
                    'total_books_taken': 0,
                    'overdue_books': 0
                }
            department_book_stats[dept]['total_employees'] += 1

        # Count unique employees with books per department
        unique_employees_with_books = set()
        for emp_book in employees_with_books:
            dept = emp_book['department']
            emp_id = emp_book['employee_id']
            unique_employees_with_books.add((dept, emp_id))

        for dept, emp_id in unique_employees_with_books:
            if dept in department_book_stats:
                department_book_stats[dept]['employees_with_books'] += 1

        # Sort employee book count by number of books (descending)
        top_borrowers = sorted(
            employee_book_count.values(),
            key=lambda x: x['books_count'],
            reverse=True
        )[:10]

        return jsonify({
            'status': 'success',
            'analytics': {
                'book_statistics': {
                    'total_books': total_books,
                    'available_books': available_books,
                    'taken_books': taken_books,
                    'overdue_books': overdue_books,
                    'utilization_rate': round((taken_books + overdue_books) / total_books * 100, 2) if total_books > 0 else 0
                },
                'genre_statistics': genre_stats,
                'popular_books': popular_books,
                'due_for_renewal': due_for_renewal,
                'feedback_statistics': feedback_stats,
                'purchase_statistics': purchase_stats,
                'employee_statistics': {
                    'total_employees': len(EMPLOYEES),
                    'employees_with_books': len(set(emp['employee_id'] for emp in employees_with_books)),
                    'total_books_borrowed': len(employees_with_books),
                    'top_borrowers': top_borrowers,
                    'employees_with_books_details': employees_with_books,
                    'department_book_stats': department_book_stats
                },
                'recent_activity': {
                    'recent_feedback': sorted(FEEDBACK, key=lambda x: x['submitted_date'], reverse=True)[:5],
                    'recent_purchases': sorted(PURCHASE_REQUESTS, key=lambda x: x['requested_date'], reverse=True)[:5]
                }
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get analytics: {str(e)}'
        }), 500

@app.route('/api/admin/charts/monthly-trends', methods=['GET'])
def get_monthly_trends():
    """Get monthly book borrowing trends for charts"""
    try:
        # Generate mock monthly data for the last 12 months
        months = []
        books_taken = []
        books_returned = []

        current_date = datetime.now()
        for i in range(12):
            month_date = current_date - timedelta(days=30*i)
            month_name = calendar.month_abbr[month_date.month]
            months.insert(0, f"{month_name} {month_date.year}")

            # Mock data - in real implementation, this would come from transaction logs
            taken = random.randint(50, 150)
            returned = random.randint(40, 140)
            books_taken.insert(0, taken)
            books_returned.insert(0, returned)

        return jsonify({
            'success': True,
            'data': {
                'months': months,
                'books_taken': books_taken,
                'books_returned': books_returned
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/charts/genre-distribution', methods=['GET'])
def get_genre_distribution():
    """Get genre distribution for donut chart"""
    try:
        genre_counts = Counter()
        for book in ALL_BOOKS:
            genre = book.get('genre', 'Unknown')
            genre_counts[genre] += 1

        # Get top 10 genres
        top_genres = genre_counts.most_common(10)

        labels = [genre for genre, _ in top_genres]
        data = [count for _, count in top_genres]

        return jsonify({
            'success': True,
            'data': {
                'labels': labels,
                'data': data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/charts/language-distribution', methods=['GET'])
def get_language_distribution():
    """Get language distribution for donut chart"""
    try:
        english_count = len([b for b in ALL_BOOKS if b.get('language') == 'English'])
        tamil_count = len([b for b in ALL_BOOKS if b.get('language') == 'Tamil'])

        return jsonify({
            'success': True,
            'data': {
                'labels': ['English', 'Tamil'],
                'data': [english_count, tamil_count]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/charts/daily-activity', methods=['GET'])
def get_daily_activity():
    """Get daily activity for the last 7 days"""
    try:
        days = []
        activity = []

        current_date = datetime.now()
        for i in range(7):
            day_date = current_date - timedelta(days=i)
            day_name = day_date.strftime('%a')
            days.insert(0, day_name)

            # Mock daily activity data
            daily_activity = random.randint(5, 25)
            activity.insert(0, daily_activity)

        return jsonify({
            'success': True,
            'data': {
                'days': days,
                'activity': activity
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/overdue-books', methods=['GET'])
def get_overdue_books():
    """Get list of overdue books with employee details"""
    try:
        overdue_books = []
        current_date = datetime.now()

        # Find books that are taken and overdue (more than 14 days)
        for book in ALL_BOOKS:
            if book.get('status') == 'taken' and book.get('taken_date'):
                taken_date = datetime.fromisoformat(book['taken_date'])
                days_overdue = (current_date - taken_date).days - 14

                if days_overdue > 0:
                    # Find employee details
                    employee = next((emp for emp in EMPLOYEES if emp.get('emp_id') == book.get('taken_by_id')), None)

                    overdue_books.append({
                        'book_id': book['id'],
                        'title': book['title'],
                        'author': book['author'],
                        'book_no': book['book_no'],
                        'taken_date': book['taken_date'],
                        'due_date': book.get('due_date'),
                        'days_overdue': days_overdue,
                        'employee': {
                            'emp_id': employee.get('emp_id') if employee else 'Unknown',
                            'name': employee.get('name') if employee else 'Unknown',
                            'department': employee.get('department') if employee else 'Unknown',
                            'email': employee.get('email') if employee else 'Unknown'
                        }
                    })

        return jsonify({
            'success': True,
            'overdue_books': overdue_books,
            'total_overdue': len(overdue_books)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/real-time-stats', methods=['GET'])
def get_real_time_stats():
    """Get real-time statistics for admin dashboard"""
    try:
        # Calculate real-time statistics
        total_books = len(ALL_BOOKS)
        available_books = len([b for b in ALL_BOOKS if b.get('status') == 'available'])
        taken_books = len([b for b in ALL_BOOKS if b.get('status') == 'taken'])

        # Books by language
        english_books = len([b for b in ALL_BOOKS if b.get('language') == 'English'])
        tamil_books = len([b for b in ALL_BOOKS if b.get('language') == 'Tamil'])

        # Active readers (employees who have taken books)
        active_readers = len(set([b.get('taken_by_id') for b in ALL_BOOKS if b.get('status') == 'taken' and b.get('taken_by_id')]))

        # Department-wise book distribution
        dept_book_stats = defaultdict(int)
        for book in ALL_BOOKS:
            if book.get('status') == 'taken' and book.get('taken_by_id'):
                employee = next((emp for emp in EMPLOYEES if emp.get('emp_id') == book.get('taken_by_id')), None)
                if employee:
                    dept = employee.get('department', 'Unknown')
                    dept_book_stats[dept] += 1

        return jsonify({
            'success': True,
            'stats': {
                'total_books': total_books,
                'available_books': available_books,
                'taken_books': taken_books,
                'english_books': english_books,
                'tamil_books': tamil_books,
                'active_readers': active_readers,
                'total_employees': len(EMPLOYEES),
                'department_stats': dict(dept_book_stats)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Smart Library System - Enhanced with Tamil Books & Admin Features")
    print("=" * 70)
    print("📚 Features Available:")
    print("   ✅ Employee Authentication")
    print("   ✅ Book Management (English & Tamil)")
    print("   ✅ Language Filtering (English/Tamil)")
    print("   ✅ Enhanced Admin Dashboard")
    print("   ✅ Department-wise Analytics")
    print("   ✅ Feedback System")
    print("   ✅ Real-time Statistics")
    print("   ✅ Mobile-Responsive Design")
    print("=" * 70)
    print("🌐 Server: http://localhost:5000")
    print(f"👥 Employees: {len(EMPLOYEES)}")
    print(f"📖 English Books: {len([b for b in ALL_BOOKS if b.get('language') == 'English'])}")
    print(f"📚 Tamil Books: {len([b for b in ALL_BOOKS if b.get('language') == 'Tamil'])}")
    print(f"📝 Total Books: {len(ALL_BOOKS)}")
    print()
    print("🎯 ACHIEVED: 374 TOTAL BOOKS ✅")
    print("   📖 English Books: 161")
    print("   📚 Tamil Books: 213")
    print()
    print("🇮🇳 Tamil Book Categories:")
    print("   • Classical Literature (திருக்குறள், கம்பராமாயணம்)")
    print("   • Historical Novels (பொன்னியின் செல்வன், சிவகாமியின் சபதம்)")
    print("   • Contemporary Fiction (வெண்முரசு, கொற்றவை)")
    print("   • Poetry (பாரதியார், கண்ணதாசன்)")
    print("   • Science & Technology (கலாம், சுஜாதா)")
    print("   • Children's Literature (பஞ்சதந்திரம், தெனாலி ராமன்)")
    print("   • Religious Literature (திருவாசகம், தேவாரம்)")
    print()
    print("📊 ADVANCED ADMIN DASHBOARD:")
    print("   • Real-time Analytics & Charts")
    print("   • Monthly Trends (Line Charts)")
    print("   • Genre Distribution (Donut Charts)")
    print("   • Daily Activity Tracking")
    print("   • Overdue Books Monitoring")
    print("   • Employee Management (4595 employees)")
    print("   • Department-wise Statistics")
    print("   • Language-based Filtering")
    print("   • Comprehensive Feedback System")
    print("=" * 70)
    print("🎯 Frontend should connect to this backend")
    print("📱 Supports both English and Tamil books with smart filtering")
    print("=" * 70)

    app.run(debug=True, host='0.0.0.0', port=5000)
