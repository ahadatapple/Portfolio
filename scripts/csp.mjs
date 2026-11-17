// Adds a Content Security Policy to every built page. Each inline <script> and
// <style> that ships is hashed, so those exact blocks run and nothing else
// can. Runs after `astro build`, which is why the hashes always match the
// final HTML. JSON-LD blocks are data, not code, and need no hash.
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const dist = new URL('../dist/', import.meta.url).pathname;

const sha = (text) => `'sha256-${createHash('sha256').update(text, 'utf8').digest('base64')}'`;

async function* htmlFiles(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(path);
    else if (entry.name.endsWith('.html')) yield path;
  }
}

function policy(scriptHashes, styleHashes) {
  return [
    "default-src 'self'",
    `script-src 'self' ${scriptHashes.join(' ')}`.trim(),
    `style-src 'self' ${styleHashes.join(' ')}`.trim(),
    "img-src 'self' data:",
    "font-src 'self'",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'none'",
    'upgrade-insecure-requests',
  ].join('; ');
}

let pages = 0;
for await (const file of htmlFiles(dist)) {
  let html = await readFile(file, 'utf8');
  html = html.replace(/<meta http-equiv="content-security-policy"[^>]*>/gi, '');

  const scripts = [...html.matchAll(/<script(\s[^>]*)?>([\s\S]*?)<\/script>/gi)]
    .filter(([, attrs = '']) => !/\bsrc=/.test(attrs) && !/type="application\/ld\+json"/.test(attrs))
    .map(([, , body]) => sha(body));
  const styles = [...html.matchAll(/<style(\s[^>]*)?>([\s\S]*?)<\/style>/gi)].map(([, , body]) => sha(body));
  if (/\sstyle="/.test(html)) {
    throw new Error(`${file} has an inline style attribute, which the policy blocks. Use a class instead.`);
  }

  const meta = `<meta http-equiv="Content-Security-Policy" content="${policy([...new Set(scripts)], [...new Set(styles)])}">`;
  html = html.replace(/<meta charset="utf-8">/i, (m) => `${m}${meta}`);
  if (!html.includes(meta)) throw new Error(`${file}: could not place the policy after <meta charset>.`);
  await writeFile(file, html);
  pages++;
}
console.log(`Content Security Policy added to ${pages} pages.`);
