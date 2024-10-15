from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from config import load_config
from connect import connect
from analytics import Analytics
import random, string, os, time, json
import jwt, os
from endpoints import *
from pprint import pprint

keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}

app = Flask(__name__, static_folder=os.environ.get('POST_STORAGE_LOCATION'))
CORS(app)
config = load_config()
load_dotenv()
bcrypt = Bcrypt(app)

like_prefix = '8!MBdp'
reaction_prefix = '6t$siV'

key_string = os.getenv("ENCRYPTION_KEY")
key = generate_key(key_string)
valid_key = os.environ.get("API_KEY_UNCRYPTED")

def verify_api_key():
    api_key = request.headers.get('x-api-key')
    if decrypt_string(key, api_key) != valid_key or not api_key:
        return jsonify({"error": "Unauthorized: Invalid API key"}), 401

@app.before_request
def before_request_func():
    if request.path in PROTECTED_ENDPOINTS:
        return verify_api_key()

@app.route(os.environ.get('TOTAL_POSTS'), methods=['GET'])
def total_posts():
    response = Database.get_total_posts()
    return jsonify(response)

@app.route(os.environ.get('MOST_VIEWED'), methods=['GET'])
def most_viewed():
    response = Database.get_top_posts(order_by='views_count')
    return jsonify(response)

@app.route(os.environ.get('MOST_LIKED'), methods=['GET'])
def most_liked():
    response = Database.get_top_posts(order_by='like_count')
    return jsonify(response)


@app.route('/api/post/<string:post_id>/view', methods=['POST'])
def view_post(post_id):
    response = Analytics.view_post(request.json.get('user_id'), post_id, request.json.get('firstname'), request.json.get('lastname'))
    return jsonify(response)

@app.route(os.environ.get('UPLOAD_POST'), methods=['POST'])
def upload_post():
    file = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')

    randomized_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    file.save(f"{os.environ.get('POST_STORAGE_LOCATION')}/{randomized_name}.jpg")
    
    response = Database.upload_post(title, description, randomized_name)
    return jsonify(response)

@app.route(os.environ.get('GET_NEW_ACCESSTOKEN'), methods=['POST'])
def new_access_token():
    response = JWT.new_access_token(request.json.get('refreshToken'))
    return jsonify(response)

@app.route(os.environ.get('CHECK_ADMIN_URL'), methods=['POST'])
def check_admin():
    response = Database.check_admin(request.json.get('email'))
    return jsonify(response)

@app.route(os.environ.get('GET_POSTS_URL'), methods=['GET'])
def get_posts():
    response = Database.get_posts()
    return jsonify(response)

@app.route(os.environ.get('GET_LATEST_POST_URL'), methods=['GET'])
def get_latest_post():
    response = Database.get_latest_post()
    return jsonify(response)

@app.route(os.environ.get('DELETE_POST'), methods=['POST'])
def delete_post():
    response = Database.delete_post(request.json.get('title'), request.json.get('description'), request.json.get('path'), request.json.get('time'))
    if response.get('response') == True:
        try:
            os.remove(f"{os.environ.get('POST_STORAGE_LOCATION')}/{request.json['path']}.jpg")
        except:
            print('Could not delete file')
    return jsonify(response)

@app.route(os.environ.get('LOGIN_URL'), methods=['POST'])
def login():
    response = Database.log_in(request.json.get('email'), request.json.get('password'))
    return jsonify(response)

@app.route(os.environ.get('REGISTER_URL'), methods=['POST'])
def register():
    response = Database.register_user(request.json.get('firstname'), request.json.get('lastname'), request.json.get('email'), request.json.get('password'))
    return jsonify(response)

@app.route(os.environ.get('CHECK_PASSWORD'), methods=['POST'])
def view_password():
    response = Database.verify_password(request.json.get('email'), request.json.get('password'))
    return jsonify(response)

@app.route(os.environ.get('EDIT_PROFILE'), methods=['POST'])
def edit_profile():
    response = Database.edit_profile(
        request.json.get('firstname'),
        request.json.get('lastname'),
        request.json.get('email'),
        request.json.get('password'),
        request.json.get('user_id'),
        request.json.get('pfp')
    )
    return jsonify(response)

@app.route(os.environ.get('VALIDATE_URL'), methods=['POST'])
def authenticate():
    token_content = JWT.validate_token(request.json.get('accessToken'), algorithms=["HS256"])
    response_data = {
        "response": "Ok",
        "status": 200,
        "user": token_content
    }
    return jsonify(response_data), 200

@app.route(os.environ.get('USER_POST_INFO'), methods=['POST'])
def get_user_post_info():
    response = Database.get_user_post_info(request.json.get('user_id'))
    return jsonify(response)

@app.route(os.environ.get('LIKE_POST'), methods=['POST'])
def like_post():
    response = Database.like_post(request.json.get('user_id'), request.json.get('post_id'))
    return jsonify(response)

@app.route(os.environ.get('UNLIKE_POST'), methods=['POST'])
def unlike_post():
    response = Database.unlike_post(request.json.get('user_id'), request.json.get('post_id'))
    return jsonify(response)

@app.route(os.environ.get('USER_REACTIONS'), methods=['POST'])
def user_reactions():
    response = Database.user_reactions(request.json.get('user_id'), request.json.get('post_id'))
    return jsonify(response)

@app.route(os.environ.get('POSTS_REACTIONS'), methods=['POST'])
def posts_reactions():
    response = Database.posts_reactions()
    return jsonify(response)

@app.route(os.environ.get('ADD_REACTION'), methods=['POST'])
def react_post():
    response = Database.add_reaction(request.json.get('user_id'), request.json.get('post_id'), request.json.get('emoji'))
    return jsonify(response)

@app.route(os.environ.get('REM_REACTION'), methods=['POST'])
def unreact_post():
    response = Database.remove_reaction(request.json.get('user_id'), request.json.get('emoji'))
    return jsonify(response)

@app.route(os.environ.get('EDIT_POST'), methods=['POST'])
def edit_post():
    response = Database.edit_post(request.json.get('post_id'), request.json.get('title'), request.json.get('description'))
    return jsonify(response)

@app.route(os.environ.get('DELETE_ACCOUNT'), methods=['POST'])
def delete_account():
    response = Database.delete_account(request.json.get('user_id'))
    return jsonify(response)

class Database:
    @staticmethod
    def get_total_posts():
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM posts")
            row = cur.fetchone()
            response_data = {
                "response": True,
                "status": 200,
                "number": row
            }
        except Exception as e:
            response_data = False
        finally:
            cur.close()
            conn.close()
        return response_data

    @staticmethod
    def get_top_posts(order_by='views_count'):
        try:
            conn = connect(config)
            cur = conn.cursor(cursor_factory=RealDictCursor)  
            query = f"SELECT * FROM posts ORDER BY {order_by} DESC LIMIT 10;"
            cur.execute(query)
            top_posts = cur.fetchmany(10)
            
            response_data = {
                "response": True,
                "status": 200,
                "top_posts": top_posts
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
    def delete_account(user_id):
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            response_data = {
                "response": True,
                "status": 200
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
    def check_admin(email):
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("SELECT * FROM admins WHERE email = %s", (email,))
            row = cur.fetchone()
            response_data = True if row else False
        except Exception as e:
            response_data = False
        finally:
            cur.close()
            conn.close()
        return response_data

    @staticmethod
    def verify_password(email, password):
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            if row:
                firstname, lastname, email, stored_password, date, pfp, user_id = row
                if bcrypt.check_password_hash(stored_password, password):
                    response_data = {
                        "response": "Ok",
                        "password": password,
                        "status": 200,
                    }
                else:
                    response_data = {
                        "response": "Wrong password",
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
    def get_user_post_info(user_id):
        likes = []
        reactions = []
        try:
            conn = connect(config)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("SELECT * FROM likes WHERE user_id = %s", (user_id,))
            likes = cur.fetchall()
            query = "SELECT * FROM posts WHERE reactions::jsonb @> %s"
            json_param = json.dumps([{"user_id": user_id}])
            cur.execute(query, (json_param,))
            reactions = cur.fetchall() 

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()

        data = {
            'likes': likes,
            'reactions': reactions
        }
        return data


    @staticmethod
    def get_posts():
        try:
            conn = connect(config)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM posts ORDER BY time DESC LIMIT 10")            
            rows = cur.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            rows = []
        finally:
            cur.close()
            conn.close()
        return rows

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
                "postData": {
                  "name": title,
                  "description": description,
                  "filename": filename,
                  "post_id": post_id
                },
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
    def edit_post(post_id, title, description):
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("""
                UPDATE posts 
                SET name = %s, description = %s 
                WHERE id = %s
            """, (title, description, post_id))
            conn.commit()

            response_data = {
                "response": "Ok",
                "status": 200,
            }

        except Exception as e:
            conn.rollback()
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
    def like_post(user_id, post_id):
        try:
            like_id = f'{like_prefix}{user_id}{post_id}'

            conn = connect(config)
            cur = conn.cursor()
            cur.execute("INSERT INTO likes (like_id, user_id, post_id) VALUES (%s, %s, %s)", (like_id, user_id, post_id))
            cur.execute("UPDATE posts SET like_count = like_count + 1 WHERE id = %s ", (post_id,))
            conn.commit()

            response_data = {
                "response": "Ok",
                "status": 200,
            }

        except Exception as e:
            conn.rollback()
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
    def add_reaction(user_id, post_id, reaction_emoji):
        try:
            reaction_data = { "emoji": reaction_emoji, "user_id": user_id }

            reaction_data_json = json.dumps(reaction_data)

            conn = connect(config)
            cur = conn.cursor()
            update_query = """
                UPDATE posts
                SET reactions = reactions || %s::jsonb
                WHERE id = %s;
            """

            cur.execute(update_query, (reaction_data_json, post_id))
            conn.commit()

            response_data = {
                "response": "Ok",
                "status": 200,
            }

        except Exception as e:
            conn.rollback()
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
    
    def remove_reaction(user_id, emoji):
        try:
            update_query = """
                UPDATE posts
                SET reactions = COALESCE(
                    (
                        SELECT jsonb_agg(reaction)
                        FROM jsonb_array_elements(reactions) AS reaction
                        WHERE NOT (reaction->>'user_id' = %s::text AND reaction->>'emoji' = %s)
                    ),
                    '[]'::jsonb
                );
            """
            conn = connect(config)
            cur = conn.cursor()
            cur.execute(update_query, (user_id, emoji))
            conn.commit()

            response_data = {
                "response": "Ok",
                "status": 200,
            }

        except Exception as e:
            conn.rollback()
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
    def unlike_post(user_id, post_id):
        try:
            like_id = f'{like_prefix}{user_id}{post_id}'

            conn = connect(config)
            cur = conn.cursor()
            cur.execute("DELETE FROM likes WHERE like_id = %s", (like_id,))
            cur.execute("UPDATE posts SET like_count = like_count - 1 WHERE id = %s ", (post_id,))
            conn.commit()
            response_data = {
                "response": "Ok",
                "status": 200,
            }

        except Exception as e:
            conn.rollback()
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
        try:
            conn = connect(config)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            
            if row:
                firstname, lastname, email, stored_password, date, pfp, user_id = row
                if bcrypt.check_password_hash(stored_password, password):
                    tokens = JWT.generate_token(firstname, lastname, email, user_id, pfp)
                    response_data = {
                        "response": "Ok",
                        "status": 200,
                        "user": {
                            "accessToken": tokens['accessToken'],
                            "refreshToken": tokens['refreshToken']
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

            response_data = {
                "response": "User registered successfully",
                "status": 200,
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

    @staticmethod
    def edit_profile(firstname, lastname, email, password, user_id, pfp):
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            conn = connect(config)
            cur = conn.cursor()
            cur.execute("""
                UPDATE users 
                SET username = %s, lastname = %s, email = %s, password = %s
                WHERE id = %s
            """, (firstname, lastname, email, hashed_password, user_id))
            conn.commit()

            tokens = JWT.generate_token(firstname, lastname, email, user_id, pfp)
            response_data = {
                "response": "Ok",
                "status": 200,
                "user": {
                    "accessToken": tokens['accessToken'],
                    "refreshToken": tokens['refreshToken']
                }
            }
        except Exception as e:
            conn.rollback()
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

def run():
    app.run(debug=True, host="0.0.0.0")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class JWT:
    def new_access_token(token):
        try:
            decoded = jwt.decode(token, os.environ.get('REFRESH_TOKEN_SECRET'), algorithms="HS256")
            firstname = decoded.get("firstname")
            lastname = decoded.get('lastname')
            email = decoded.get('email')
            admin = decoded.get("admin")
            user_id = decoded.get('user_id')
            pfp = decoded.get('pfp')
            accessToken = jwt.encode({"firstname": firstname, "lastname": lastname, "email": email, 'admin': admin, "user_id": user_id, "pfp": pfp}, os.environ.get('ACCESS_TOKEN_SECRET'), algorithm="HS256")
            return { 'accessToken': accessToken }
        except(jwt.DecodeError):
            return { 'Refresh token not valid: ': jwt.DecodeError}

    def generate_token(firstname, lastname, email, user_id, pfp):
        is_admin = Database.check_admin(email)

        accessToken = jwt.encode({"firstname": firstname, "lastname": lastname, "email": email, 'admin': is_admin, "user_id": user_id, "pfp": pfp}, os.environ.get('ACCESS_TOKEN_SECRET'), algorithm="HS256")
        refreshToken = jwt.encode({"firstname": firstname, "lastname": lastname, "email": email, 'admin': is_admin, "user_id": user_id, "pfp": pfp}, os.environ.get('REFRESH_TOKEN_SECRET'), algorithm="HS256")

        return {
            'accessToken': accessToken,
            'refreshToken': refreshToken
        }

    def validate_token(token, algorithms):
        try:
            decoded = jwt.decode(token, os.environ.get('ACCESS_TOKEN_SECRET'), algorithms="HS256")
            firstname = decoded.get("firstname")
            lastname = decoded.get('lastname')
            email = decoded.get('email')
            admin = decoded.get("admin")
            user_id = decoded.get('user_id')
            pfp = decoded.get('pfp')
            return {
                'firstname': firstname, 
                'lastname': lastname,
                'email': email, 
                'admin': admin,
                'user_id': user_id,
                'pfp': pfp
                }
        except:
            return {}