import { error, type Handle, type RequestEvent } from "@sveltejs/kit";
import { currentTheme } from "$lib/theme";
import { env } from "$env/dynamic/private";

const csrf = (
    event: RequestEvent,
    allowedOrigins: string[] | any,
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

export const handle: Handle = async ({ event, resolve }) => {
    csrf(event, [env.ORIGIN]);

    let cookieTheme = event.cookies.get("theme");
    currentTheme.set(cookieTheme)

    if (!cookieTheme) {
        cookieTheme = "dark";
        event.cookies.set("theme", cookieTheme, { path: '/', sameSite: true, maxAge: 2592000, secure: false, httpOnly: false });
    }

    const response = await resolve(event, {
        transformPageChunk: ({ html }) => {
            return html.replace('data-theme=""', `data-theme="${cookieTheme}"`);
        }
    });

    return response;
};
