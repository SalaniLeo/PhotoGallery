// @ts-nocheck
import { env } from '$env/dynamic/private';
import { getAddresses } from '$lib/consts';
import { get_posts, user_post_info, validate_access } from '$lib/fetcher';
import { verifyRefreshToken } from '$lib/verifyAccess';
import type { LayoutServerLoad } from './$types';

export const load = async ({ url, cookies, getClientAddress, request }: Parameters<LayoutServerLoad>[0]) => {
	const address = `http://${env.FLASK_SERVER_ADDR}`;
	let accessToken = cookies.get('accessToken');
	let use_analytics = env.DOMAIN != 'http://localhost' ? true : false
	const refreshToken = cookies.get('refreshToken');
	const addresses = getAddresses(env, url, address)
	let posts: Array<[string, string, boolean]> | any = await get_posts(address, env.GET_POSTS_URL)

	const newAccessToken = await verifyRefreshToken(accessToken, refreshToken, address, cookies, env);

	if (newAccessToken) {
		accessToken = newAccessToken
		cookies.set('accessToken', newAccessToken, { httpOnly: false, path: '/', maxAge: 15 });
	}

	if (accessToken && refreshToken) {
		const validated_data = await validate_access(address, env.VALIDATE_URL, accessToken, env.API_KEY);

		const user_posts_info: {likes: Array<object>, reactions: Array<object>} | any = await user_post_info(address, env.USER_POST_INFO, validated_data.user_id, env.API_KEY);

		let liked_posts = user_posts_info.likes
		let reacted_posts = user_posts_info.reactions
		
		let data = {
			addresses,
			user: {
				'loggedIn': true,
				'info': {'firstname': validated_data.firstname, 'lastname': validated_data.lastname, 'email': validated_data.email, 'user_id': validated_data.user_id, 'admin': validated_data.admin, 'pfp': validated_data.pfp},
				'liked_posts': liked_posts,
				'reacted_posts': reacted_posts
			},
			posts,
			apikey: env.API_KEY,
			analytics: {
				analytics_key: env.ANALYTICS_KEY,
				analytics_url: env.ANALYTICS_URL,
				entered_url: env.ENTERED_URL
			},
			use_analytics,
			source: url.origin, 
		};

		return data

	}

	return {
		addresses,
		user: {
			loggedIn: false
		},
		posts,
		apikey: env.API_KEY,
		use_analytics,
		source: url.origin, 
	};

}

