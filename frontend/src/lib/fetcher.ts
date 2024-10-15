// ---- WEBSITE LOAD ----
export async function validate_access(base: string, apiAddreds: string, accessToken: string, key: string) {
    try {
        const response = await fetch(base + apiAddreds, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': key
            },
            body: JSON.stringify({
                accessToken
            })
        })
        const response_data = await response.json()
        return response_data.user
    } catch (e) {
        return e
    }
}


// ---- POSTS ACTIONS ----
export async function get_posts(base: string, apiAddreds: string) {
    try {
		const response = await fetch(base + apiAddreds);
        return await response.json();
	} catch(e) {
        return e
	}
}

export async function user_post_info(base: string, apiAddreds: string, user_id: string, key: string) {
    try {
        const response = await fetch(base + apiAddreds, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': key
            },
            body: JSON.stringify({
                'user_id': user_id
            })
        });
        return await response.json();
    } catch (e) {
        return e;
    }
}

export async function get_top_posts(base: string, apiAddress: string) {
    try {
        const response = await fetch(base + apiAddress, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return await response.json();
    } catch (e) {
        return e;
    }
}
