// 180 × 180 icon for iOS home screens and some link previews. Matches favicon.svg.
import type { APIRoute } from 'astro';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';

export const GET: APIRoute = async () => {
  const bold = await readFile(join(process.cwd(), 'node_modules/@fontsource/inter/files/inter-latin-700-normal.woff'));
  const svg = await satori(
    {
      type: 'div',
      props: {
        style: {
          width: 180,
          height: 180,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#1d5fd1',
          color: '#ffffff',
          fontFamily: 'Inter',
          fontSize: 78,
          fontWeight: 700,
          letterSpacing: -2,
        },
        children: 'AR',
      },
    } as never,
    { width: 180, height: 180, fonts: [{ name: 'Inter', data: bold, weight: 700, style: 'normal' }] },
  );
  const png = new Resvg(svg).render().asPng();
  return new Response(new Uint8Array(png), { headers: { 'Content-Type': 'image/png' } });
};
