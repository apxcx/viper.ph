import { readFileSync, createReadStream, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

/** @returns {import('astro').AstroIntegration} */
export default function r2Preview() {
  return {
    name: 'viper-r2-preview-mirrors',
    hooks: {
      'astro:server:setup': ({ server }) => {
        const mapPath = fileURLToPath(new URL('../.r2-preview-map.json', import.meta.url));
        if (!existsSync(mapPath)) return;
        const map = JSON.parse(readFileSync(mapPath, 'utf8'));
        server.middlewares.use((req, res, next) => {
          const path = (req.url ?? '').split('?')[0];
          if (!path.startsWith('/api/media/') || !['GET', 'HEAD'].includes(req.method ?? '')) return next();
          const key = path.slice('/api/media/'.length);
          const local = map[key];
          if (!local || !existsSync(local)) return next();
          /** @type {Record<string, string>} */
          const types = { jpg: 'image/jpeg', jpeg: 'image/jpeg', webp: 'image/webp', png: 'image/png', avif: 'image/avif' };
          res.setHeader('Content-Type', types[key.split('.').pop() ?? ''] ?? 'application/octet-stream');
          res.setHeader('X-Viper-Image-Source', 'development-mirror');
          if (req.method === 'HEAD') return res.end();
          createReadStream(local).on('error', () => res.destroy()).pipe(res);
        });
      },
    },
  };
}
