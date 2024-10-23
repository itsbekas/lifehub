import { env } from '$env/dynamic/private'

export const api_url = (path: string) => {
    const BACKEND_URL = env.BACKEND_URL;
    return `http://${BACKEND_URL}:8000/api/v0${path}`;
}
