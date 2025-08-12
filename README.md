# Inventory Management System

A full-stack web application for managing inventory items with CRUD operations and search functionality.

## Features

- Add new inventory items with name, quantity, and description
- Update existing items' quantities
- Delete items from inventory
- Search items by name
- Real-time inventory list display
- Clean and user-friendly interface

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (AJAX)
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Environment Management**: python-dotenv

## Project Structure

```
.
├── frontend/
│   └── frontend.html
├── backend/
│   ├── app.py
│   ├── database.sql
│   ├── requirements.txt
│   ├── setup.py
│   └── .env
└── README.md
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Configure Environment**:
   - Copy `backend/.env.example` to `backend/.env`
   - Update database credentials in `.env` file

3. **Setup Database**:
   ```bash
   cd backend
   python setup.py
   ```

4. **Run the Application**:
   ```bash
   cd backend
   python app.py
   ```
   - Open `frontend/frontend.html` in your browser
   - The backend API will be running on `http://localhost:8080`

## API Endpoints

- `GET /items` - Get all inventory items
- `POST /items` - Add new item
- `PUT /items/<id>` - Update item quantity
- `DELETE /items/<id>` - Delete item
- `GET /items/search?q=<query>` - Search items by name

## Security Features

- Input validation
- SQL injection prevention
- Error logging
- Environment-based configuration

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for learning and reference
