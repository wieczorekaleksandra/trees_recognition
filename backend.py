import base64
import sqlite3
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from PIL import Image
from model_usage import process_image

app = Flask(__name__)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
jwt = JWTManager(app)

DATABASE = 'flowers.db'

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data['email'].strip().lower()
    password = data['password']

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "User already exists"}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data['email'].strip().lower()
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()

    if not result or not check_password_hash(result['password'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token}), 200


@app.route('/upload-image', methods=['POST'])
@jwt_required()  # Require a valid JWT for access
def upload_image():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    try:
        # Get the current user from the JWT
        current_user = get_jwt_identity()

        image_byte = base64.b64decode(data['image'])
        image_final = Image.open(BytesIO(image_byte))
        recognized = process_image(image_final)

        print(f"User: {current_user} - Recognized: {recognized}")
        return jsonify({"recognized": recognized}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
