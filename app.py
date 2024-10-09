from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def home():
    return "Welcome to the Petition App!"
@app.route('/petitions', methods=['GET'])
def get_petitions():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM petitions')
        petitions = cursor.fetchall()
        return jsonify(petitions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/petitions', methods=['POST'])
def add_petition():
    title = request.json.get('title')
    description = request.json.get('description')
    
    if not title or not description:
        return jsonify({'error': 'Title and description are required!'}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = db.cursor()
        cursor.execute('INSERT INTO petitions (title, description) VALUES (%s, %s)', (title, description))
        db.commit()
        return jsonify({'message': 'Petition added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
