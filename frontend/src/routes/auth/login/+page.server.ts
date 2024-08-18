import { LOGIN_URL, BACKEND_IP, GET_LATEST_POST_URL} from '$env/static/private';
import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

const address = `http://${env.FLASK_SERVER_ADDR}`;

export async function load({ cookies, params }) {
    const latest_post_data = await fetch(`${address}${GET_LATEST_POST_URL}`)
    let latest_post = await latest_post_data.json();

    return {
        latest_post: latest_post,
        address: BACKEND_IP
    }
}

export const actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData();
        const email = data.get('email');
        const password = data.get('password');

        if (!email || !password) {
            return fail(403, {
                error: "Please fill up each field",
                state: "var(--font-primary-color)"
            });
        }

        const response = await fetch(`${address}${LOGIN_URL}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: email,
              password: password
            })
          });

        const json = await response.json();

        if (json['status'] === 200) {
            cookies.set('accessToken', json.user.token, { path: '/', secure: false, maxAge: 24 * 60 * 60 * 30 } );
            throw redirect(303, '/');
        } else {
            console.log(json)
            return fail(json['status'], {
                error: json['response'],
                state: "var(--font-error-color)"
            });
        }
    }
};