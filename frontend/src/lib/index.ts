import { errorCode, throwError } from "./stores"

export function showToast(message: string, code: number = 400) {
    throwError.set(message)
    errorCode.set(code)
    console.error(message);
}