import type { APIRoute } from 'astro';
import posts from '../../../data/post-index.json' with { type: 'json' };

export const prerender = false;
type IndexedPost = { imageKey: string; imageKeys?: string[] };
const allowedKeys = new Set(
  (posts as IndexedPost[])
    .flatMap((post) => [post.imageKey, ...(post.imageKeys ?? [])])
    .map((key) => key.split('?')[0]),
);

interface R2Image {
  body: ReadableStream<Uint8Array>;
  httpEtag: string;
  writeHttpMetadata(headers: Headers): void;
}
interface MediaBucket {
  get(key: string): Promise<R2Image | null>;
}

const imageTypes: Record<string, string> = {
  jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png',
  webp: 'image/webp', avif: 'image/avif', gif: 'image/gif',
};

const serve: APIRoute = async ({ params, request, locals }) => {
  const key = params.key ?? '';
  if (!allowedKeys.has(key)) return new Response('Image not found', { status: 404 });
  const env = (locals as { runtime?: { env?: { MEDIA?: MediaBucket } } }).runtime?.env;
  if (!env?.MEDIA) return new Response('Image storage unavailable', { status: 503 });
  try {
    const object = await env.MEDIA.get(key);
    if (!object) return new Response('Image not found', { status: 404 });
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('Content-Type', imageTypes[key.split('.').pop()?.toLowerCase() ?? ''] ?? 'application/octet-stream');
    headers.set('ETag', object.httpEtag);
    headers.set('Cache-Control', 'public, max-age=86400');
    headers.set('X-Content-Type-Options', 'nosniff');
    if (request.headers.get('If-None-Match') === object.httpEtag) {
      return new Response(null, { status: 304, headers });
    }
    return new Response(request.method === 'HEAD' ? null : object.body, { headers });
  } catch (error) {
    console.error('R2 image read failed', error instanceof Error ? error.message : 'unknown error');
    return new Response('Image storage temporarily unavailable', { status: 503 });
  }
};

export const GET = serve;
export const HEAD = serve;
