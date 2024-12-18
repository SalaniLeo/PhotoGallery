from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from collections import OrderedDict
from config import load_config
from connect import connect
from lib.jwt import generate_token, validate_token
import random, string, os, time

keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}

app = Flask(__name__, static_folder='posts')
CORS(app)
config = load_config()
load_dotenv()
bcrypt = Bcrypt(app)

@app.route('/api/auth/isadmin', methods=['POST'])
def check_admin():
    response = Database.check_admin(request.json.get('name'), request.json.get('email'))
    return jsonify(response)

@app.route('/api/posts/all', methods=['GET'])
def get_posts():
    response = Database.get_posts()
    return jsonify(response)

@app.route('/api/posts/latest', methods=['GET'])
def get_latest_post():
    response = Database.get_latest_post()
    return jsonify(response)

@app.route('/api/posts/upload', methods=['POST'])
def upload_post():
    file = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')

    randomized_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    file.save(f'{os.path.dirname(os.path.abspath(__file__))}/posts/{randomized_name}.jpg')
    response = Database.upload_post(title, description, randomized_name)
    return jsonify(response)

@app.route('/api/posts/delete', methods=['POST'])
def delete_post():
    response = Database.delete_post(request.json.get('title'), request.json.get('description'), request.json.get('path'), request.json.get('time'))
    if response.get('response') == True:
        try:
            os.remove(f"{os.path.dirname(os.path.abspath(__file__))}/posts/{request.json.get('path')}.jpg")
        except:
            print('Could not delete file')
    return jsonify(response)

@app.route('/api/auth/login', methods=['POST'])
def login():
    response = Database.log_in(request.json.get('email'), request.json.get('password'))
    return jsonify(response)

@app.route('/api/auth/register', methods=['POST'])
def register():
    response = Database.register_user(request.json.get('firstname'), request.json.get('lastname'), request.json.get('email'), request.json.get('password'))
    return jsonify(response)

@app.route('/api/auth/authenticate', methods=['POST'])
def authenticate():
    token_content = validate_token(request.json.get('accessToken'), algorithms=["HS256"])
    response_data = {
        "response": "Ok",
        "status": 200,
        "user": token_content
    }
    return jsonify(response_data), 200

class Database:
    @staticmethod
    def check_admin(name, email):
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("SELECT * FROM admins WHERE email = %s", (email,))
            row = cur.fetchone()
            response_data = {
                "response": True if row else False,
                "status": 200 if row else 404
            }
        except Exception as e:
            response_data = {
                "response": False,
                "status": 500,
                "error": str(e)
            }
        finally:
            cur.close()
            conn.close()
        return response_data

    @staticmethod
    def get_posts():
        try:
            conn = connect(config)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM posts")
            rows = cur.fetchmany(10)
        except Exception as e:
            print(f"An error occurred: {e}")
            rows = []
        finally:
            cur.close()
            conn.close()
        rows_reversed = list(reversed(rows))
        return rows_reversed

    @staticmethod
    def get_latest_post():
        try:
            conn = connect(config)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM posts ORDER BY time DESC LIMIT 1")
            row = cur.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            row = {}
        finally:
            cur.close()
            conn.close()
        return row

    @staticmethod
    def upload_post(title, description, filename):
        try:
            conn = connect(config)
            cur = conn.cursor()
            post_id = id_generator()
            query = "INSERT INTO posts(id, name, description, source, time) VALUES (%s, %s, %s, %s, %s);"
            values = (post_id, title, description, filename, int(time.time()))
            cur.execute(query, values)
            conn.commit()
            response_data = {
                "response": True,
                "status": 200
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            response_data = {
                "response": False,
                "status": 500,
                "error": str(e)
            }
        finally:
            cur.close()
            conn.close()
        return response_data

    @staticmethod
    def delete_post(title, description, path, time):
        try:
            conn = connect(config)
            cur = conn.cursor()
            query = "DELETE FROM posts WHERE time = (%s);"
            values = ([time])
            cur.execute(query, values)
            conn.commit()
            response_data = {
                "response": True,
                "status": 200
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            response_data = {
                "response": False,
                "status": 500,
                "error": str(e)
            }
        finally:
            cur.close()
            conn.close()
        return response_data

    @staticmethod
    def log_in(email, password):
        print(request.headers.get('Host'))
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            if row:
                user_id, firstname, lastname, email, stored_password, date = row
                if bcrypt.check_password_hash(stored_password, password):
                    encoded_jwt = generate_token(firstname, email)
                    response_data = {
                        "response": "Ok",
                        "status": 200,
                        "user": {
                            "token": encoded_jwt
                        }
                    }
                else:
                    response_data = {
                        "response": "Wrong username or password",
                        "status": 401
                    }
            else:
                response_data = {
                    "response": "User not found",
                    "status": 404
                }
        except Exception as e:
            response_data = {
                "response": "Error",
                "status": 500,
                "error": str(e)
            }
        finally:
            cur.close()
            conn.close()
        return response_data

    @staticmethod
    def register_user(firstname, lastname, email, password):
        try:
            conn = connect(config)
            cur = conn.cursor()
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur.execute("INSERT INTO users (username, lastname, email, password) VALUES (%s, %s, %s, %s)", 
                        (firstname, lastname, email, hashed_password))
            conn.commit()
            encoded_jwt = generate_token(firstname, email)
            response_data = {
                "response": "User registered successfully",
                "status": 200,
                "user": {
                    "token": encoded_jwt
                }
            }
        except Exception as e:
            error_message = str(e)
            if "duplicate key" in error_message.lower():
                response_data = {
                    "response": "Email already in use",
                    "status": 409
                }
            else:
                response_data = {
                    "response": error_message,
                    "status": 500
                }
        finally:
            cur.close()
            conn.close()
        return response_data

def run():
    app.run(debug=True, host="0.0.0.0")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
