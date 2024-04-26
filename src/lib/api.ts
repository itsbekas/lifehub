const BASE_URL = 'http://localhost:8000/api/v0'

export async function fetch_api(path: string, init?: RequestInit | undefined): Promise<Response> {
    return await fetch(BASE_URL + path, init);
}
