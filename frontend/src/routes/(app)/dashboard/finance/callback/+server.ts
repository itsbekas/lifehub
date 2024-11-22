import { api_url } from "@/lib/api";
import { redirect } from "@sveltejs/kit";

import type { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ fetch, url }) => {

    const ref = url.searchParams.get('ref');
    const error = url.searchParams.get('error');

    if (!ref) {
        return new Response('Invalid request', { status: 400 });
    }

    if (error) {
        return redirect(301, `/dashboard/finance?error=${error}`);
    }

    await fetch(api_url(`/finance/bank/callback?ref=${ref}`), {
        method: 'POST',
    });

    throw redirect(301, `/dashboard/finance`);
}