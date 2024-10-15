from config import load_config
from dotenv import load_dotenv
from connect import connect
from connect import get_db_connection
import json

config = load_config()
load_dotenv()

class Analytics:
    @staticmethod
    def view_post(user_id, post_id, firstname, lastname):
        conn = None
        cur = None
        try:
            conn = connect(config)
            cur = conn.cursor()

            cur.execute("SELECT views, views_count FROM posts WHERE id = %s;", (post_id,))
            post = cur.fetchone()

            if post is None:
                cur.close()
                conn.close()
                return 404

            views = post[0] 
            views_count = post[1]

            if views is None:
                views = {}

            if views_count is None:
                views_count = 0

            views_count += 1

            if user_id is not None:
                if str(user_id) in views:
                    views[str(user_id)]['count'] += 1
                else:
                    views[str(user_id)] = {
                        'firstname': firstname,
                        'lastname': lastname,
                        'count': 1
                    }

            cur.execute(
                "UPDATE posts SET views = %s, views_count = %s WHERE id = %s;",
                [json.dumps(views), views_count, post_id]
            )

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
            if cur:
                cur.close()
            if conn:
                conn.close()

        return response_data
