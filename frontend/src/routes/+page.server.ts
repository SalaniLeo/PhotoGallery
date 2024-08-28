import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/private';

export const load: PageServerLoad = async ( { url } ) => {
    console.log(url.origin)
    try {
        const address = `http://${env.FLASK_SERVER_ADDR}`;
        const response = await fetch(address + env.GET_POSTS_URL);

        if (!response.ok) {
            throw new Error(`Failed to fetch posts: ${response.statusText}`);
        }

        const posts: Array<[string, string, boolean]> = await response.json();

        return {
            addresses: { 
                url: env.DOMAIN,
                address: address,
                ip: url.origin,
                delete: env.DELETE_POST,
                upload: env.UPLOAD_POST,
                get_posts: env.GET_POSTS_URL
            },
            posts
        };
    } catch (error) {
        console.error('Error loading posts:', error);
        throw error; // Rethrow or handle as needed
    }
};