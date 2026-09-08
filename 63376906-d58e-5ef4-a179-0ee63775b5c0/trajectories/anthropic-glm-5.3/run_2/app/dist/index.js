import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { core } from './routes/core.js';
import { ops } from './routes/ops.js';
import { ledger } from './routes/ledger.js';
import { carbon } from './routes/carbon.js';
import { certs, verify } from './routes/certs.js';
import { record } from './routes/record.js';
import { commercial } from './routes/commercial.js';
import { HttpError } from './lib/http.js';
import { migrate } from './migrate.js';
import { seedAll } from './seed.js';
const app = new Hono();
const api = new Hono();
api.route('/', core);
api.route('/', ops);
api.route('/', ledger);
api.route('/', carbon);
api.route('/', certs);
api.route('/', record);
api.route('/', commercial);
api.route('/verify', verify);
// A write that arrives with no idempotency key is refused before it reaches a route,
// so a retry can never be indistinguishable from a second act.
app.use('/api/*', async (c, next) => {
    const method = c.req.method.toUpperCase();
    if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
        if (!c.req.header('idempotency-key')) {
            return c.json({ error: 'idempotency_key_required' }, 400);
        }
    }
    return next();
});
app.route('/api', api);
app.onError((err, c) => {
    if (err instanceof HttpError) {
        return c.json({ error: err.code, ...err.extra }, err.status);
    }
    console.error('unhandled', err);
    return c.json({ error: 'internal_error' }, 500);
});
// One production build served from one origin.
const here = path.dirname(fileURLToPath(import.meta.url));
const webDir = path.resolve(here, '../web');
const distDir = path.join(webDir, 'dist');
app.use('*', async (c, next) => {
    if (c.req.path.startsWith('/api'))
        return next();
    const url = new URL(c.req.url);
    let file = path.join(distDir, url.pathname === '/' ? 'index.html' : url.pathname);
    if (!file.startsWith(distDir))
        return c.text('forbidden', 403);
    if (fs.existsSync(file) && fs.statSync(file).isFile()) {
        const type = contentType(file);
        return c.body(fs.readFileSync(file), 200, { 'content-type': type, 'cache-control': file.endsWith('.html') ? 'no-cache' : 'public, max-age=3600' });
    }
    const index = path.join(distDir, 'index.html');
    if (fs.existsSync(index)) {
        return c.body(fs.readFileSync(index), 200, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-cache' });
    }
    return c.text('not found', 404);
});
function contentType(file) {
    if (file.endsWith('.html'))
        return 'text/html; charset=utf-8';
    if (file.endsWith('.js'))
        return 'text/javascript; charset=utf-8';
    if (file.endsWith('.css'))
        return 'text/css; charset=utf-8';
    if (file.endsWith('.woff2'))
        return 'font/woff2';
    if (file.endsWith('.json'))
        return 'application/json';
    if (file.endsWith('.svg'))
        return 'image/svg+xml';
    if (file.endsWith('.txt'))
        return 'text/plain; charset=utf-8';
    return 'application/octet-stream';
}
const port = Number(process.env.PORT ?? 4173);
async function main() {
    await migrate();
    const seeded = await (await import('./lib/db.js')).query(`select count(*)::int as count from sites`);
    if (!Number(seeded[0].count)) {
        await seedAll();
    }
    serve({ fetch: app.fetch, port, hostname: '0.0.0.0' }, (info) => {
        console.log(`ravel serving on 0.0.0.0:${info.port}`);
    });
}
main().catch((e) => { console.error(e); process.exit(1); });
