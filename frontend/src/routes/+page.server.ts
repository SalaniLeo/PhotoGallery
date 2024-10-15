import { env } from '$env/dynamic/private';
import { get_top_posts } from '../lib/fetcher';

const address = `http://${env.FLASK_SERVER_ADDR}`;

export async function load({ cookies, params }) {
    const latest_post_data = await fetch(`${address}${env.GET_LATEST_POST_URL}`)
    let latest_post = await latest_post_data.json();

    const most_liked_post_data = await get_top_posts(address, env.MOST_LIKED)
    let most_liked_post = await most_liked_post_data.top_posts;

    const most_viewed_post_data = await get_top_posts(address, env.MOST_VIEWED)
    let most_viewed_post = await most_viewed_post_data.top_posts;

    return {
        latest_post: latest_post,
        most_liked_post: most_liked_post,
        most_viewed_post: most_viewed_post
    }
}
