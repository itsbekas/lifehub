export function load({ cookies, fetch }) {
    
    const token = cookies.get('token');
    const display_name = cookies.get('display_name');

    return {
        loggedIn: !!token,
        display_name
    }
}
