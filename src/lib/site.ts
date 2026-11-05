export type Locale = 'en' | 'ja';
export const origin = 'https://kiss.i-pp.co.jp';
export const repository = 'https://github.com/i-pp/project-kiss-website';

export const navigation = [
  { path: '', en: 'Home', ja: 'ホーム' },
  { path: 'philosophy/', en: 'Philosophy', ja: '理念' },
  { path: 'products/', en: 'Products', ja: 'プロダクト' },
  { path: 'products/aceis/', en: 'AceIS', ja: 'AceIS' },
  { path: 'roadmap/', en: 'Roadmap', ja: 'ロードマップ' },
  { path: 'docs/', en: 'Docs', ja: 'ドキュメント' },
  { path: 'contributing/', en: 'Contributing', ja: '参加する' },
] as const;

export function href(locale: Locale, path = ''): string {
  return `${locale === 'ja' ? '/ja/' : '/'}${path}`;
}

export function pagePath(pathname: string): string {
  return pathname.replace(/^\/ja(?:\/|$)/, '/').replace(/^\//, '');
}
