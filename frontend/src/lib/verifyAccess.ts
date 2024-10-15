
export async function verifyRefreshToken(
    accessToken: string | undefined,
    refreshToken: string | undefined,
    address: string,
    cookies: any,
    env: any
): Promise<string | undefined | null> {
    if (!accessToken && refreshToken) {
        const response = await fetch(address + env.GET_NEW_ACCESSTOKEN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': env.API_KEY
            },
            body: JSON.stringify({
                'refreshToken': refreshToken
            })
        });

        if (!response.ok) {
            console.error('Could not verify user');
            return null;
        } else {
            const data = await response.json();
            return data.accessToken;
        }
    }
    return accessToken;
}