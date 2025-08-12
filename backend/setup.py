#!/usr/bin/env python3

import os
import subprocess
from dotenv import load_dotenv
import mysql.connector

print("Setting up Inventory Management System...")

# Install Python dependencies
print("\nInstalling Python dependencies...")
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Load environment variables
load_dotenv()

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    print("\nCreating database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_db")
    cursor.execute("USE inventory_db")
    
    # Read and execute SQL schema
    print("\nCreating tables...")
    with open('database.sql', 'r') as f:
        sql = f.read()
        # Split SQL into individual statements
        statements = sql.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement.strip())
    
    conn.commit()
    print("\nSetup complete!")
    print("You can now run the application using: python app.py")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'conn' in locals():
        conn.close()
