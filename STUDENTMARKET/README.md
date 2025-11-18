# StudentMarket

A Flask-based marketplace web application for students to buy and sell items.

## Features

- **User Authentication**: Register, login, logout with Flask-Login
- **User Profiles**: Name, email, date of birth, description, email verification status, admin status
- **Ad Management**: Create, edit, delete, and browse ads
- **Categories**: Books, Electronics, Scripts, Clothes, Furniture, Sports & Outdoors, Other
- **Markdown Support**: Rich text descriptions with automatic HTML conversion
- **Search & Filter**: Search ads by keywords and filter by category
- **Responsive Design**: Bootstrap 5 for mobile-friendly interface
- **MongoDB Backend**: NoSQL database for flexible data storage
- **Rate Limiting**: Protection against abuse
- **Security**: CSRF protection, secure sessions, input sanitization

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: MongoDB with PyMongo
- **Authentication**: Flask-Login & Flask-Principal
- **Forms**: Flask-WTF & WTForms
- **Frontend**: Bootstrap 5 & Bootstrap Icons
- **Markdown**: Python-Markdown & Bleach for sanitization
- **Email**: Flask-Mail (for future email verification)

## Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB 4.0 or higher (running locally or remotely)

### Steps

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and configure your settings:
     - `SECRET_KEY`: Change to a random secret key
     - `MONGODB_URI`: Your MongoDB connection string
     - `MONGODB_DB`: Your database name
     - `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`: Initial admin user (optional)

5. **Start MongoDB** (if running locally):
   ```bash
   sudo systemctl start mongod
   # or
   mongod
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Access the application**:
   - Open your browser and go to: `http://localhost:5000`

## Usage

### For Users

1. **Register**: Create an account with your name, email, and password
2. **Browse Ads**: View all available ads or filter by category
3. **Post Ad**: Create a new ad with title, description (Markdown supported), and category
4. **Manage Your Ads**: Edit or delete your own ads
5. **Contact Sellers**: Use email links to contact sellers

### For Admins

- Admins can edit/delete any ads
- Admin status is set via database or initial configuration

## Project Structure

```
STUDENTMARKET/
├── app/
│   ├── __init__.py           # App factory and configuration
│   ├── models.py             # User and Ad models
│   ├── auth/                 # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py         # Login, register, profile routes
│   │   └── forms.py          # Auth forms
│   ├── ads/                  # Ads blueprint
│   │   ├── __init__.py
│   │   ├── routes.py         # CRUD routes for ads
│   │   └── forms.py          # Ad forms
│   ├── main/                 # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py         # Home and about pages
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── ads/
│   │   ├── main/
│   │   └── errors/
│   └── static/               # Static files (CSS, JS, images)
├── app.py                    # Application entry point
├── config.py                 # Configuration classes
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Models

### User Model
- `name`: User's full name
- `email`: User's email (unique)
- `password_hash`: Hashed password
- `is_email_verified`: Email verification status
- `is_admin`: Admin privilege flag
- `dob`: Date of birth (optional)
- `description`: User bio/description (optional)
- `created_at`: Account creation timestamp

### Ad Model
- `title`: Ad title
- `description`: Ad description (Markdown format)
- `description_html`: Rendered HTML from Markdown
- `category`: Category (books, electronics, scripts, clothes, etc.)
- `created_by`: User ID of creator
- `created_at`: Ad creation timestamp

## Configuration

Key configuration options in `config.py`:

- `SECRET_KEY`: Flask secret key for sessions
- `MONGO_URI`: MongoDB connection URI
- `MONGO_DBNAME`: MongoDB database name
- `ITEMS_PER_PAGE`: Number of ads per page (default: 12)
- Email settings for Flask-Mail (for future features)

## Security Features

- Password hashing with Werkzeug
- CSRF protection on all forms
- Input sanitization for HTML content
- Rate limiting on requests
- Secure session cookies
- XSS protection via content sanitization

## Future Enhancements

- Email verification system
- Image uploads for ads
- User messaging system
- Favorite/bookmark ads
- Advanced search filters
- Admin dashboard
- Price field for ads
- Location-based filtering

## License

This project is created for educational purposes.

## Contributing

Feel free to fork and submit pull requests!
