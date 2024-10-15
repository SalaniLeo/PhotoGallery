import { writable } from 'svelte/store';

export const rootData = writable()
export const showCreatePost = writable(false);
export const isUserLogged = writable(false)
export const throwError = writable()
export const errorCode = writable()