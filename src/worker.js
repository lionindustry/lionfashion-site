// Sends every visitor and search engine to one address (https://<HOME>, set in wrangler.jsonc "vars"):
// www., http:// and the workers.dev preview address get a permanent 301 redirect.
// Then serves the site files from public/ with browser-cache headers.
const WEEK = 'public, max-age=604800';
const MEDIA = /\.(jpg|jpeg|png|webp|svg|gif|ico|pdf|woff2?|css|js)$/i;

export default {
  async fetch(request, env) {
    const HOME = env.HOME;
    const url = new URL(request.url);
    const wrongHost = url.hostname === 'www.' + HOME || url.hostname.endsWith('.workers.dev');
    if (wrongHost || (url.hostname === HOME && url.protocol === 'http:')) {
      url.protocol = 'https:';
      url.hostname = HOME;
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    const res = await env.ASSETS.fetch(request);
    const out = new Response(res.body, res);
    if (res.ok && MEDIA.test(url.pathname)) out.headers.set('Cache-Control', WEEK);
    out.headers.set('X-Content-Type-Options', 'nosniff');
    out.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    return out;
  },
};
