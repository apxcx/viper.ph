import type { APIRoute } from 'astro';

export const prerender = false;

const json = (body: Record<string, unknown>, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

const text = (value: unknown) => (typeof value === 'string' ? value.trim() : '');

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const payload = await request.json();
    const formKind = payload?.formKind === 'partnership' ? 'partnership' : 'contact';
    const firstName = text(payload?.firstName);
    const lastName = text(payload?.lastName);
    const email = text(payload?.email).toLowerCase();
    const phone = text(payload?.phone);
    const companyName = text(payload?.companyName);
    const companyWebsite = text(payload?.companyWebsite);
    const message = text(payload?.message);
    const botcheck = text(payload?.botcheck);
    const collaborationTypes = Array.isArray(payload?.collaborationTypes)
      ? payload.collaborationTypes.filter((item: unknown): item is string => typeof item === 'string').map((item: string) => item.trim()).filter(Boolean)
      : [];

    if (botcheck) return json({ ok: true, message: 'Thanks — your message has been received.' });
    if (!firstName || !lastName || !email || !/^\S+@\S+\.\S+$/.test(email) || !phone || !companyName || !message) {
      return json({ ok: false, message: 'Please complete all required fields.' }, 400);
    }
    if (formKind === 'partnership' && collaborationTypes.length === 0) {
      return json({ ok: false, message: 'Please choose at least one collaboration type.' }, 400);
    }

    const env = (locals as { runtime?: { env?: Record<string, string | undefined> } }).runtime?.env ?? {};
    const accessKey = env.WEB3FORMS_ACCESS_KEY;
    if (!accessKey) return json({ ok: false, message: 'Form delivery is not configured yet.' }, 503);

    const outbound: Record<string, unknown> = {
      access_key: accessKey,
      subject: formKind === 'partnership' ? 'Viper.ph Partnership Inquiry' : 'Viper.ph Contact Form Message',
      from_name: `${firstName} ${lastName}`,
      name: `${firstName} ${lastName}`,
      email,
      phone,
      company: companyName,
      website: companyWebsite,
      message,
      form_type: formKind,
    };
    if (formKind === 'partnership') outbound.collaboration_type = collaborationTypes.join(', ');

    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(outbound),
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok || result?.success !== true) {
      console.error('Web3Forms inquiry failed', response.status, result?.message ?? 'unknown error');
      return json({ ok: false, message: 'We could not send your message. Please try again.' }, 502);
    }
    return json({ ok: true, message: 'Your message has been received. We will be in touch soon.' });
  } catch {
    return json({ ok: false, message: 'Something went wrong. Please try again.' }, 400);
  }
};
