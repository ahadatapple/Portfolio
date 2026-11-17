// Link-preview images, rendered once at build time: /og/home.png and one per
// case study (/og/gomoku.png and so on). 1200 × 630 PNG, the size X, LinkedIn,
// Slack and iMessage all crop well.
import type { APIRoute, GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { profile } from '../../data/site';

const W = 1200;
const H = 630;
const INK = '#1a1a18';
const MUTED = '#5c5c57';
const ACCENT = '#1d5fd1';
const BG = '#fbfbf9';
const RULE = '#e2e1dc';

interface Card {
  kicker: string;
  title: string;
  body: string;
  footer: string;
}

type Node = { type: string; props: Record<string, unknown> };
const el = (type: string, style: Record<string, unknown>, children?: unknown): Node => ({
  type,
  props: { style, children },
});

const fontDir = join(process.cwd(), 'node_modules/@fontsource/inter/files');
const fontsPromise = Promise.all([
  readFile(join(fontDir, 'inter-latin-400-normal.woff')),
  readFile(join(fontDir, 'inter-latin-600-normal.woff')),
  readFile(join(fontDir, 'inter-latin-700-normal.woff')),
]);

function layout(card: Card): Node {
  const titleSize = card.title.length > 34 ? 60 : 72;
  return el(
    'div',
    { width: W, height: H, display: 'flex', background: BG, fontFamily: 'Inter' },
    [
      el('div', { width: 18, height: H, background: ACCENT }),
      el(
        'div',
        {
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '72px 88px 64px 82px',
          width: W - 18,
        },
        [
          el('div', { display: 'flex', flexDirection: 'column' }, [
            el('div', { fontSize: 28, fontWeight: 600, color: ACCENT, letterSpacing: 0.5 }, card.kicker),
            el(
              'div',
              { fontSize: titleSize, fontWeight: 700, color: INK, lineHeight: 1.1, marginTop: 22, letterSpacing: -1 },
              card.title,
            ),
            el('div', { fontSize: 32, fontWeight: 400, color: INK, lineHeight: 1.35, marginTop: 30, maxWidth: 980 }, card.body),
          ]),
          el(
            'div',
            {
              display: 'flex',
              borderTop: `2px solid ${RULE}`,
              paddingTop: 26,
              fontSize: 24,
              fontWeight: 400,
              color: MUTED,
            },
            card.footer,
          ),
        ],
      ),
    ],
  );
}

export const getStaticPaths: GetStaticPaths = async () => {
  const footer = 'ECE, Rice University ’30 · Incoming Amazon intern, Summer 2027';
  const projects = await getCollection('projects');
  return [
    {
      params: { slug: 'home' },
      props: {
        card: {
          kicker: 'Software and ML engineering',
          title: profile.name,
          body: profile.hero,
          footer: `${footer} · Gates Scholar`,
        } satisfies Card,
      },
    },
    ...projects.map((p) => ({
      params: { slug: p.id },
      props: {
        card: {
          kicker: `${profile.name} · Case study`,
          title: p.data.title,
          body: p.data.result,
          footer,
        } satisfies Card,
      },
    })),
  ];
};

export const GET: APIRoute = async ({ props }) => {
  const [regular, semibold, bold] = await fontsPromise;
  const svg = await satori(layout(props.card as Card) as never, {
    width: W,
    height: H,
    fonts: [
      { name: 'Inter', data: regular, weight: 400, style: 'normal' },
      { name: 'Inter', data: semibold, weight: 600, style: 'normal' },
      { name: 'Inter', data: bold, weight: 700, style: 'normal' },
    ],
  });
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: W } }).render().asPng();
  return new Response(new Uint8Array(png), { headers: { 'Content-Type': 'image/png' } });
};
