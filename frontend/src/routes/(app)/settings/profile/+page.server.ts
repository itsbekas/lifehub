import { api_url } from '$lib/api';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
  const userResponse = await fetch(api_url('/user/me'));
  const user = await userResponse.json();

  return { user };
}

/** @type {import('./$types').Actions} */
export const actions = {
  updateProfile: async ({ fetch, request }) => {
    const formData = await request.formData();

    if (formData.get('password')) {
      if (formData.get('password') !== formData.get('password_confirm')) {
        return { error: 'Passwords do not match' };
      }
    }

    console.log(formData.get('name'));
    console.log(formData.get('email'));

    const response = await fetch(api_url('/user/me'), {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: formData.get('name'),
        email: formData.get('email'),
        password: formData.get('password')
      })
    });

    const data = await response.json();
    if (!response.ok) {
      return { error: data.detail };
    }
  }
};
