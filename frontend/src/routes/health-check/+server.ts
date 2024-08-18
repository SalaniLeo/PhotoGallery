export async function GET({ request }) {
    return new Response(JSON.stringify({ message: 'Logged out successfully' }), {
        status: 200,
    });
}
