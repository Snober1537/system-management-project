from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import logging
from functools import wraps

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='inventory.log'
)

app = Flask(__name__)

# Get database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'inventory_db')

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        logging.info("Database connection established successfully")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        raise

def validate_item_data(data):
    """Validate item data before processing"""
    if not isinstance(data.get('name'), str) or not data['name'].strip():
        raise ValueError("Name is required and must be a non-empty string")
    
    try:
        quantity = int(data.get('quantity', 0))
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a positive number")
    
    return True

def validate_id(id):
    """Validate that ID is a positive integer"""
    try:
        id = int(id)
        if id <= 0:
            raise ValueError
        return id
    except (ValueError, TypeError):
        raise ValueError("Invalid ID format")

@app.route('/')
def index():
    return jsonify({"message": "Inventory Management System API Running"})

@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info("Items retrieved successfully")
        return jsonify(items)
    except mysql.connector.Error as err:
        logging.error(f"Error fetching items: {err}")
        return jsonify({"error": "Failed to fetch items"}), 500

@app.route('/items', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        validate_item_data(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventory (name, quantity, description) VALUES (%s, %s, %s)",
            (data['name'], data['quantity'], data.get('description', ''))
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        logging.info(f"Item added: {data['name']}")
        return jsonify({"message": "Item added successfully"}), 201
    except ValueError as err:
        logging.error(f"Validation error: {str(err)}")
        return jsonify({"error": str(err)}), 400
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        item_id = validate_id(item_id)
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({"error": "Quantity is required"}), 400
            
        validate_item_data(data)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = %s WHERE id = %s",
            (data['quantity'], item_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        logging.info(f"Item updated: ID {item_id}")
        return jsonify({"message": "Item updated successfully"})
    except ValueError as err:
        logging.error(f"Validation error: {str(err)}")
        return jsonify({"error": str(err)}), 400
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        item_id = validate_id(item_id)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        logging.info(f"Item deleted: ID {item_id}")
        return jsonify({"message": "Item deleted successfully"})
    except ValueError as err:
        logging.error(f"Validation error: {str(err)}")
        return jsonify({"error": str(err)}), 400
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500

@app.route('/items/search', methods=['GET'])
def search_items():
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({"error": "Search query is required"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory WHERE name LIKE %s", (f"%{query}%",))
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logging.info(f"Search performed: {query}")
        return jsonify(items)
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({"error": "Database error occurred"}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logging.error(f"Application failed to start: {e}")