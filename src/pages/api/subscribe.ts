import type { APIRoute } from 'astro';

export const prerender = false;

const json = (body: Record<string, unknown>, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const payload = await request.json();
    const firstName = typeof payload.firstName === 'string' ? payload.firstName.trim() : '';
    const email = typeof payload.email === 'string' ? payload.email.trim().toLowerCase() : '';

    if (!firstName || !email || !/^\S+@\S+\.\S+$/.test(email)) {
      return json({ ok: false, message: 'Please enter your first name and a valid email.' }, 400);
    }

    const env = (locals as { runtime?: { env?: Record<string, string | undefined> } }).runtime?.env ?? {};
    const token = env.MAILERLITE_API_TOKEN;
    const groupId = env.MAILERLITE_GROUP_ID;

    if (!token) {
      return json({ ok: false, message: 'Newsletter sign-up is not configured yet.' }, 503);
    }

    const subscriber: Record<string, unknown> = {
      email,
      fields: { name: firstName },
      status: 'active',
    };

    if (groupId) subscriber.groups = [groupId];

    const response = await fetch('https://connect.mailerlite.com/api/subscribers', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(subscriber),
    });

    if (!response.ok) {
      console.error('MailerLite subscription failed', response.status);
      return json({ ok: false, message: 'We could not complete your subscription. Please try again.' }, 502);
    }

    return json({ ok: true, message: 'You are on the list. Watch your inbox for the next Viper briefing.' });
  } catch {
    return json({ ok: false, message: 'Something went wrong. Please try again.' }, 400);
  }
};
