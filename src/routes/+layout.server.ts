/** @type {import('./$types').PageServerLoad} */
export function load({ cookies }) {
    
    const token = cookies.get('token');
    const display_name = cookies.get('display_name');

    return {
        hasToken: !!token,
        display_name
    }

}
