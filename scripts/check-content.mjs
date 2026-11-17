// Fails the build if unfinished copy would ship: [FILL] markers, TODOs or
// filler text anywhere in src/. Run with: npm run check:content
import { readdir, readFile } from 'node:fs/promises';
import { join, relative } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const banned = [/\[FILL/i, /\bTODO\b/, /\bFIXME\b/, /lorem ipsum/i];

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(path);
    else if (/\.(astro|mdx?|ts|css)$/.test(entry.name)) yield path;
  }
}

const problems = [];
for await (const file of walk(join(root, 'src'))) {
  const lines = (await readFile(file, 'utf8')).split('\n');
  lines.forEach((line, i) => {
    if (banned.some((re) => re.test(line))) problems.push(`${relative(root, file)}:${i + 1}: ${line.trim()}`);
  });
}

if (problems.length) {
  console.error('Unfinished copy found:\n' + problems.join('\n'));
  process.exit(1);
}
console.log('Content check passed: no unfinished copy in src/.');
