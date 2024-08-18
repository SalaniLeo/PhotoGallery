import { writable } from 'svelte/store';

export const showCreatePost = writable(false);
export const postTitle = writable();
export const postDescription = writable();
export const refreshPosts = writable(false)
export const isUserLogged = writable(false)
export const uploadAddress = writable()