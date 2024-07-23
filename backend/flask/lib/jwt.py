import jwt, os, requests
from dotenv import load_dotenv

load_dotenv()
check_admin_url = os.environ.get('CHECK_ADMIN_URL')

def generate_token(firstname, email):
    json = {'name': firstname, 'email': email}
    response = requests.post(check_admin_url, json = json)

    if response.status_code == 200:
        try:
            data = response.json()
            is_admin = data.get('response')
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return {'status': 'error', 'message': 'Failed to parse response'}
    else:
        return {'status': 'error', 'message': f'Response status: {response.status_code}'}

    return jwt.encode({"name": firstname, "email": email, 'admin': is_admin}, os.environ.get('ACCESS_TOKEN_SECRET'), algorithm="HS256")

def validate_token(token, algorithms):
    try:
        decoded = jwt.decode(token, os.environ.get('ACCESS_TOKEN_SECRET'), algorithms="HS256")
        name = decoded.get("name")
        email = decoded.get('email')
        admin = decoded.get("admin")
        return {'username': name, 'email': email, 'admin': admin}
    except:
        return {}