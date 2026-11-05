import { href, navigation, origin } from '../lib/site';

export function GET() {
  const urls = (['en', 'ja'] as const).flatMap(locale =>
    navigation.map(page => `<url><loc>${origin}${href(locale, page.path)}</loc></url>`),
  );
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.join('')}</urlset>`, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
