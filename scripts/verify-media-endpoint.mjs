import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const { GET, HEAD } = await import(new URL('../src/pages/api/media/[...key].ts', import.meta.url).href);
const posts = JSON.parse(readFileSync(new URL('../src/data/post-index.json', import.meta.url), 'utf8'));
const key = posts[0].imageKey;
const bytes = new Uint8Array([1, 2, 3, 4]);
const bucket = {
  async get() {
    return {
      body: new ReadableStream({ start(controller) { controller.enqueue(bytes); controller.close(); } }),
      httpEtag: '"test-image"',
      /** @param {Headers} headers */
      writeHttpMetadata(headers) { headers.set('Content-Type', 'application/octet-stream'); },
    };
  },
};
/**
 * @param {string} path
 * @param {{get: () => Promise<{body: ReadableStream<Uint8Array>, httpEtag: string, writeHttpMetadata: (headers: Headers) => void} | null>} | undefined} media
 * @param {string} method
 * @param {Record<string, string>} headers
 */
const context = (path, media, method = 'GET', headers = {}) => ({
  params: { key: path },
  request: new Request('https://viper.ph/api/media/' + path, { method, headers }),
  locals: { runtime: { env: { MEDIA: media } } },
});

let response = await GET(context(key, bucket));
assert.equal(response.status, 200);
assert.match(response.headers.get('Content-Type') ?? '', /^image\//);
assert.equal(response.headers.get('Cache-Control'), 'public, max-age=86400');
assert.equal(response.headers.get('ETag'), '"test-image"');
assert.deepEqual(new Uint8Array(await response.arrayBuffer()), bytes);
response = await HEAD(context(key, bucket, 'HEAD'));
assert.equal(response.status, 200);
assert.equal((await response.arrayBuffer()).byteLength, 0);
response = await GET(context(key, bucket, 'GET', { 'If-None-Match': '"test-image"' }));
assert.equal(response.status, 304);
response = await GET(context(key, undefined));
assert.equal(response.status, 503);
response = await GET(context(key, { get: async () => null }));
assert.equal(response.status, 404);
for (const invalid of ['private/example.png', '../secret', key + '/extra', 'articles/2026/10/not-imported/featured.jpg']) {
  response = await GET(context(invalid, bucket));
  assert.equal(response.status, 404);
}
console.log('Media endpoint verified: public-key allowlist, R2 body streaming, image MIME, HEAD, ETag 304, cache policy, missing/unconfigured storage handling.');
