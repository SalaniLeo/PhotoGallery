import { serialize } from 'cookie';

export async function GET({ request }) {

    const accessTokenCookie = serialize('accessToken', '', {
        secure: false,
        path: '/',
        expires: new Date(0)
    });

    const refreshTokenCookie = serialize('refreshToken', '', {
        secure: false,
        path: '/',
        expires: new Date(0)
    });
    const headers = new Headers();
    headers.append('Set-Cookie', accessTokenCookie);
    headers.append('Set-Cookie', refreshTokenCookie);
    headers.append('Content-Type', 'application/json');

    return new Response(JSON.stringify({ message: 'Logged out successfully' }), {
        status: 200,
        headers: headers
    });
}
