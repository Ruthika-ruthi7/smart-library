# Smart Library Management System

A full-stack web application for library management, featuring Employee and Admin dashboards.

---

## Features

### Employee Dashboard
- **Login**: Sign in with username and date of birth.
- **Book List**: Browse available books.
- **Borrow Books**: Take books (marked as unavailable).
- **Profile**: View personal details.

### Admin Dashboard
- **Statistics**: View total books taken, active employees.
- **Trends**: Department-wise analytics with charts.
- **Book Status**: Real-time book availability.
- **Manage Data**: Full CRUD operations for employees and books.

---

## Tech Stack

**Frontend**
- React (Vite)
- React Router
- Axios
- Chart.js or Recharts
- CSS

**Backend**
- Flask (Python)
- Supabase (PostgreSQL)
- RESTful API

**Database**
- Supabase PostgreSQL  
  Tables: `employees`, `books`, `transactions`

---

## Project Structure

```
smart-library/
├── frontend/    # React application
├── backend/     # Flask API
├── docs/        # Documentation
└── README.md
```

---

## Setup

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Supabase account

### Backend
1. `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure environment: Copy `.env.example` to `.env` and add Supabase credentials
6. Run: `python app.py`

### Frontend
1. `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`

### Database
1. Create Supabase project
2. Run SQL scripts to create tables and sample data
3. Update backend `.env` with Supabase credentials

---

## API Endpoints

**Authentication**
- `POST /login` — Validate username and DOB

**Employee**
- `GET /employee/details` — Get employee info
- `GET /books` — List available books
- `POST /take-book` — Borrow a book

**Admin**
- `GET /admin/data` — Dashboard stats
- `GET /admin/crud/employees` — List employees
- `GET /admin/crud/books` — List books
- `POST /admin/crud/employees` — Add employee
- `PUT /admin/crud/employees/:id` — Edit employee
- `DELETE /admin/crud/employees/:id` — Remove employee
- `POST /admin/crud/books` — Add book
- `PUT /admin/crud/books/:id` — Edit book
- `DELETE /admin/crud/books/:id` — Remove book

---

## Quick Start

**Option 1: Startup Scripts**
- Windows: Double-click `start.bat`
- Mac/Linux: `chmod +x start.sh && ./start.sh`

**Option 2: Manual**
- See [docs/SETUP.md](docs/SETUP.md) for detailed steps

---

## Demo Credentials

**Employee**
- Username: `john_doe`
- Date of Birth: `1990-05-15`

**Admin**
- Username: `admin`
- Date of Birth: `1980-01-01`

---

## Notes

1. **Supabase Required**: Set up Supabase and database before running.
2. **Environment Variables**: Copy `backend/.env.example` to `backend/.env` and add your credentials.
3. **Install Dependencies**: Both Python and Node.js dependencies are needed.

---

## Development

Follows modern web development practices and RESTful API design.

```
smart-library/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   └── package.json
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── database_schema.sql
│   └── sample_data.sql
├── docs/
└── README.md
```

---

## License

MIT
