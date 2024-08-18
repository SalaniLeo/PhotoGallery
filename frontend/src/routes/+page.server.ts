import type { PageServerLoad } from './$types';
import { GET_POSTS_URL, BACKEND_PORT, BACKEND_IP, DELETE_POST, UPLOAD_POST, BACKEND_ADDR, FLASK_SERVER_ADDR } from '$env/static/private';
import { env } from '$env/dynamic/private';

export const load: PageServerLoad = async ( { url } ) => {
    try {
        const address = `http://${env.FLASK_SERVER_ADDR}`;
        const response = await fetch(address + GET_POSTS_URL);

        if (!response.ok) {
            throw new Error(`Failed to fetch posts: ${response.statusText}`);
        }

        const posts: Array<[string, string, boolean]> = await response.json();

        return {
            addresses: { 
                url: BACKEND_IP,
                address: address,
                ip: url.origin,
                delete: DELETE_POST,
                upload: UPLOAD_POST,
                get_posts: GET_POSTS_URL
            },
            posts
        };
    } catch (error) {
        console.error('Error loading posts:', error);
        throw error; // Rethrow or handle as needed
    }
};