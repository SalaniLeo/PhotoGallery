import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

const address = `http://${env.FLASK_SERVER_ADDR}`;

export async function load({ cookies, params }) {
    const latest_post_data = await fetch(`${address}${env.GET_LATEST_POST_URL}`)
    let latest_post = await latest_post_data.json();

    return {
        latest_post: latest_post,
    }
}

export const actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData();
        const email = data.get('email')
        const password = data.get('password')
        const firstname = data.get('firstname')
        const lastname = data.get('lastname')

        const response = await fetch(`${address}${env.REGISTER_URL}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': env.API_KEY
            },
            body: JSON.stringify({
                firstname,
                lastname,
                email,
                password
            })
        });

        const json = await response.json();
        if (json['status'] === 200) {
            throw redirect(303, '/auth/login');
        } else {
            return fail(json['status'], {
                error: json['response'],
                state: "var(--font-error-color)"
            });
        }
    }
};
