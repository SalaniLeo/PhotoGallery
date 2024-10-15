import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

const address = `http://${env.FLASK_SERVER_ADDR}`;

export async function load({ cookies, params }) {
    const latest_post_data = await fetch(`${address}${env.GET_LATEST_POST_URL}`);
    let latest_post = await latest_post_data.json();

    return {
        latest_post: latest_post,
    };
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

        const response = await fetch(`${address}${env.LOGIN_URL}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'x-api-key': env.API_KEY
            },
            body: JSON.stringify({
              email: email,
              password: password
            })
        });

        const json = await response.json();

        if (json['status'] === 200) {
            cookies.set('accessToken', json.user.accessToken, { path: '/', maxAge: 15 * 60 }); // 15 minutes expiry
            cookies.set('refreshToken', json.user.refreshToken, { path: '/', maxAge: 24 * 60 * 60 * 7 }); // 7 days expiry
            
            throw redirect(303, '/');
        } else {
            return fail(json['status'], {
                error: json['response'],
                state: "var(--font-error-color)"
            });
        }
    }
};
