export function getAddresses(env: any, url: any, address: string) {
	return {
		url: env.DOMAIN,
		address: address,
		ip: url.origin,
		delete: env.DELETE_POST,
		upload: env.UPLOAD_POST,
		get_posts: env.GET_POSTS_URL,
		like: env.LIKE_POST,
		unlike: env.UNLIKE_POST,
		react: env.ADD_REACTION,
		unreact: env.REM_REACTION,
		edit_post: env.EDIT_POST,
		check_password: env.CHECK_PASSWORD,
		edit_profile: env.EDIT_PROFILE,
		delete_account: env.DELETE_ACCOUNT,
		post_views: env.POST_VIEWS
	}
}