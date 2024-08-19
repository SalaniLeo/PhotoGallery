import { env } from '$env/dynamic/private';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals, url, request, cookies }) => {
	const accessToken = cookies.get('accessToken');
	
	if (accessToken != null) {
        const address = `http://${env.FLASK_SERVER_ADDR}`;
		try {
			const response = await fetch(address + env.VALIDATE_URL, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					accessToken
				})
			});
	
			if (response.status === 200) {
				cookies.set("loggedIn", 'true', { secure: false, path: '/' })
	
				const data = await response.json();
				const username = data['user']['username'];
				const admin = data['user']['admin'];
				const loggedIn = true
	
				return {
					user: {
						loggedIn: loggedIn,
						name: username,
						admin: admin
					}
				};
			}
		} catch(error) {
			console.error('Could not connect to backend:', error)
			throw error;
		}
	}

	// @ts-ignore
	let loggedIn = cookies.get("loggedIn",{ path: '/' })
	if (loggedIn == null) {
		cookies.set('loggedIn', 'false', { secure: false, path: '/' })
	}

	return {
		user: {
			loggedIn: false
		}
	};

}

