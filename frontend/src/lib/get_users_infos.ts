import { showToast } from "$lib";

export async function fetch_analytics(website: any, userAgent: string, ip: any, analytics_data: { analytics_key: string; analytics_url: string; entered_url: string | undefined; }, admin: boolean) {

    const key = analytics_data.analytics_key
    const analytics_url = analytics_data.analytics_url
    const entered_url = analytics_data.entered_url

    const browser = getBrowserInfo(userAgent)
    const os = getOSInfo(userAgent)
    try{ 
        const response = await fetch(analytics_url + entered_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': key
            },
            body: JSON.stringify({
                ip, website, browser, os
            })
        })
    } catch {
        if(admin) {
            showToast('Unable to connect to analytics server', 400)
        }
    }
    // let response_data = await response.json()

}

function getBrowserInfo(userAgent: string | string[]) {
    if (userAgent.includes("Chrome") && !userAgent.includes("Edg")) {
        return "Chrome";
    } else if (userAgent.includes("Firefox")) {
        return "Firefox";
    } else if (userAgent.includes("Safari") && !userAgent.includes("Chrome")) {
        return "Safari";
    } else if (userAgent.includes("Edg")) {
        return "Edge";
    } else if (userAgent.includes("Opera") || userAgent.includes("OPR")) {
        return "Opera";
    } else {
        return "Unknown Browser";
    }
}

function getOSInfo(userAgent: string | string[]) {

    if (userAgent.includes("Win")) {
        return "Windows";
    } else if (userAgent.includes("Mac")) {
        return "macOS";
    } else if (userAgent.includes("X11") || userAgent.includes("Linux")) {
        return "Linux";
    } else if (userAgent.includes("Android")) {
        return "Android";
    } else if (userAgent.includes("iPhone") || userAgent.includes("iPad")) {
        return "iOS";
    } else {
        return "Unknown OS";
    }
}