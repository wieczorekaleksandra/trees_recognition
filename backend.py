import os
import base64
import sqlite3
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from PIL import Image
from model_usage import process_image

app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'your_secret_key' 
jwt = JWTManager(app)

DATABASE = 'flowers.db'
PLANTS_DIR = 'plants'  

def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=10)
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
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        # This handles cases where the email already exists in the database
        return jsonify({"error": "User already exists"}), 400
    except Exception as e:
        # General error handling (e.g., for database lock or connection issues)
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure the connection is closed regardless of success or failure
        if conn:
            conn.close()



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

        # Decode the image from Base64
        image_byte = base64.b64decode(data['image'])
        image_final = Image.open(BytesIO(image_byte))

        # Process the image to recognize the plant
        recognized = process_image(image_final)  # Expected to return a list of results

        if not recognized or not isinstance(recognized, list):
            return jsonify({"error": "Recognition failed or unexpected format"}), 400

        results = []  # Prepare a list to store results for each recognized plant

        for item in recognized:
            if len(item) < 3:
                continue  # Skip if the item does not have enough data
            
            plant_id = item[2]  # Assuming the plant ID is at index 2
            image_path = os.path.join(PLANTS_DIR, f"{plant_id}.jpg")

            # Encode the image as Base64 if the file exists
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            else:
                image_base64 = None  # No image found for this plant ID

            # Append the result
            results.append({
                "plant_name": item[1],  # Include the recognized data
                "image_base64": image_base64  # Add the Base64 encoded image
            })

        if not results:
            return jsonify({"error": "No valid plants recognized or images found"}), 404

        print(f"User: {current_user} - Recognized: {recognized}")
        return jsonify({"results": results}), 200  # Return all results as a JSON array

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/plants', methods=['GET'])
def get_all_plants():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, scientific_name, code FROM plants')
        plants = cursor.fetchall()
        conn.close()

        result = []
        for plant in plants:
            plant_dict = {
                "id": plant["id"],
                "scientific_name": plant["scientific_name"],
                "code": plant["code"]
            }

            # Find the image file
            image_path = os.path.join(PLANTS_DIR, f"{plant['code']}.jpg")
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    plant_dict["image"] = base64.b64encode(img_file.read()).decode('utf-8')
            else:
                plant_dict["image"] = None  # No image available

            result.append(plant_dict)

        return jsonify({"plants": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
