import { redirect } from '@sveltejs/kit';

// @ts-ignore
export const load: LayoutServerLoad = async ({ cookies }) => {
    if(!cookies.get('accessToken') && !cookies.get('refreshToken')) {
        throw redirect(303, '/auth/login');
    }
}