import { error, type Handle, type RequestEvent } from "@sveltejs/kit";
import { allowedOrigins } from "$lib/config.js";
import { currentTheme } from "$lib/theme";

// CSRF Protection Middleware
const csrf = (
    event: RequestEvent,
    allowedOrigins: string[],
) => {
    const { request } = event;

    const forbidden =
        isFormContentType(request) &&
        (request.method === "POST" ||
            request.method === "PUT" ||
            request.method === "PATCH" ||
            request.method === "DELETE") &&
        !allowedOrigins.includes(request.headers.get("origin") || "");

    if (forbidden) {
        throw error(403, `Cross-site ${request.method} form submissions are forbidden`);
    }
};

// Helper Functions to Check Content-Type
function isContentType(request: Request, ...types: string[]) {
    const type = request.headers.get("content-type")?.split(";", 1)[0].trim() ?? "";
    return types.includes(type.toLowerCase());
}

function isFormContentType(request: Request) {
    return isContentType(
        request,
        "application/x-www-form-urlencoded",
        "multipart/form-data",
        "text/plain",
    );
}

// Main Handle Function
export const handle: Handle = async ({ event, resolve }) => {
    // Apply CSRF Protection
    csrf(event, allowedOrigins);

    // Determine the theme
    let cookieTheme = event.cookies.get("theme");
    currentTheme.set(cookieTheme)

    if (!cookieTheme) {
        cookieTheme = "dark";
        event.cookies.set("theme", cookieTheme, { path: '/', sameSite: true, maxAge: 2592000, secure: false, httpOnly: false });
    }

    // Modify the HTML with the current theme
    const response = await resolve(event, {
        transformPageChunk: ({ html }) => {
            return html.replace('data-theme=""', `data-theme="${cookieTheme}"`);
        }
    });

    return response;
};
