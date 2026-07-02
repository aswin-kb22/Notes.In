# 📚 Notes.in

A Flask-based web application for sharing, searching, and managing academic notes.
> 🚧 **Project Status:** Currently under development. New features and improvements are being added regularly.
## ✨ Overview
Notes.in is a web application that allows students to upload, browse, preview, search, and download academic notes. It provides secure user authentication so that users can manage only the notes they have uploaded.
This project is being developed as part of my B.Tech Computer Science coursework while exploring Flask, SQLAlchemy, and web development.
## 🚀 Current Features
### Authentication
- User Registration
- User Login
- User Logout
- Session Management
### Notes Management
- Upload Notes
- Download Notes
- Preview PDF Notes
- Edit Note Details
- Delete Uploaded Notes
- View Personal Notes
### Search
- Search by Note Title
- Search by Subject
### User Features
- User Profile
- Notes Upload Counter
- Secure Delete Account
### Security
- Only the uploader can edit a note.
- Only the uploader can delete a note.
- Protected routes using Flask sessions.
## 🛠️ Tech Stack
### Backend
- Python
- Flask
- Flask SQLAlchemy
### Database
- SQLite
### Frontend
- HTML5
- SCSS
- CSS
- JavaScript (for UI interactions)
### Version Control
- Git
- GitHub
## 📂 Project Structure
Notes.in/
│
├── main.py
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── styles.scss
│   ├── styles.css
│   └── pencil.png
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── upload.html
│   ├── mynotes.html
│   ├── profile.html
│   └── edit.html
│
├── uploads/
│
└── README.md
## ⚙️ Installation
Clone the repository
```bash
git clone https://github.com/aswin-kb22/Notes.In.git
```
Move into the project directory
```bash
cd Notes.In
```
Create a virtual environment
```bash
python -m venv .venv
```
Activate the virtual environment
### Windows
```bash
.venv\Scripts\activate
```
Install dependencies
```bash
pip install -r requirements.txt
```
Run the application
```bash
python main.py
```
Open your browser and visit
```
http://127.0.0.1:5000
```
## 🚧 Upcoming Features
- Advanced Filtering
- Dashboard
- Download Counter
- Responsive Design
- Better Search
- File Replacement
- User Statistics
- Improved UI/UX
- Admin Panel (Future)
## 🎯 Learning Objectives
This project is helping me learn:
- Flask
- SQLAlchemy ORM
- Authentication & Authorization
- File Upload Handling
- Session Management
- CRUD Operations
- Database Relationships
- Git & GitHub
- Frontend Design with SCSS
## 📄 License
This project is intended for educational purposes.
## 👨‍💻 Author
**Aswin KB**
GitHub: https://github.com/aswin-kb22
