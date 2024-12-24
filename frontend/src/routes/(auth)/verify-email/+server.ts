import { redirect } from '@sveltejs/kit';
import { api_url } from '$lib/api';

/** @type {import('./$types').RequestHandler} */
export async function GET({ url }) {
  const token: string | null = url.searchParams.get('token');

  if (!token) {
    redirect(302, '/');
  }

  const response = await fetch(api_url(`/user/verify-email`), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ token })
  });

  if (response.status === 200) {
    redirect(302, '/login');
  } else {
    redirect(302, '/');
  }
}
