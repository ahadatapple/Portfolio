# Ahad Rahman · Portfolio

Personal site for an ECE student at Rice University: three engineering case studies, two short project cards, and a résumé. Static HTML from Astro, no client framework, no tracking.

**Every page scores 100 on Lighthouse** for performance, accessibility, best practices and SEO, on mobile and desktop, with zero layout shift. Each page is about 7 KB over the wire, with all CSS inlined and two small inline scripts.

## Run it locally

Requires Node 22 or later.

```sh
npm install
npm run dev        # http://localhost:4321, with hot reload
npm run build      # checks, type checks, builds to dist/, adds the security policy
npm run preview    # serves dist/ exactly as it will deploy
```

Link previews and the sitemap use https://ahadatapple.dev (set in `astro.config.mjs`). To build for a different address:

```sh
SITE_URL=https://example.com npm run build
```

## Architecture

```
src/
  content/projects/*.mdx    case studies; frontmatter feeds the home page
  content.config.ts         schema every case study must satisfy
  data/site.ts              profile, short cards, skills, experience
  components/Flow.astro     architecture diagrams as HTML, not images
  layouts/Base.astro        <head>: meta, Open Graph, theme bootstrap
  pages/
    index.astro             home
    projects/[slug].astro   one page per case study
    og/[slug].png.ts        link-preview images, rendered at build
    apple-touch-icon.png.ts
    robots.txt.ts
    404.astro
scripts/
  check-content.mjs         fails the build on [FILL], TODO or filler text
  csp.mjs                   hashes inline code into a per-page security policy
analysis/gomoku/measure.py  reproducible win-rate measurement for one case study
```

### Why each choice

**Astro, static output.** The site is a set of documents, read once. Astro renders them to HTML at build time and ships no runtime, so there is nothing to hydrate and nothing to slow a phone down. A Next.js export would carry a React runtime on every page for no interactivity in return.

**MDX with a typed schema.** Each case study is a file in Git. The schema requires a one-line result, role, dates and stack, so a project without a measurable result fails the build instead of shipping vague.

**Diagrams as HTML, not Mermaid or images.** Mermaid needs a large client script and shifts layout while it renders. `Flow.astro` draws boxes and arrows with an ordered list and CSS: sharp at any size, themed in light and dark, and read by screen readers as a sequence of steps.

**System fonts on the page, Inter only in preview images.** No web font means no font download and no text reflow. The preview images embed Inter at build time, where it costs visitors nothing.

**Link previews rendered at build.** `og/[slug].png.ts` uses Satori and resvg to draw a 1200 × 630 PNG for the home page and each case study from the same frontmatter the page uses. A changed result updates its preview automatically.

**Theme without a flash.** A tiny inline script in `<head>` applies a saved light or dark choice before first paint. The first visit follows the OS setting.

**Security policy from the build output.** Astro's built-in policy missed the inline theme scripts and component styles. `scripts/csp.mjs` runs after the build, hashes every inline `<script>` and `<style>` in each page, and writes a `Content-Security-Policy` meta tag that allows exactly those blocks. It fails the build if an inline `style=""` attribute appears, since the policy would block it.

**Guards in the build.** `npm run build` fails if unfinished copy, a type error, a schema violation or an unhashable inline style would ship.

## Editing

| To change | Edit |
| --- | --- |
| Name, hero line, links, skills, experience | `src/data/site.ts` |
| A case study | `src/content/projects/<slug>.mdx` |
| Add a case study | New `.mdx` file with the same frontmatter; `order` sets its position |
| Résumé | Replace `public/resume.pdf` or `public/resume-ee.pdf` |
| Preview image design | `src/pages/og/[slug].png.ts` |
| Colours, type, spacing | `src/styles/global.css` |

A diagram inside any `.mdx` file:

```mdx
import Flow from '../../components/Flow.astro';

<Flow
  caption="What the picture shows"
  stages={[
    { nodes: [{ title: 'First step', detail: 'small note' }] },
    { nodes: [{ title: 'Option A' }, { title: 'Option B' }], edge: 'arrow label' },
    { nodes: [{ title: 'Result', accent: true }] },
  ]}
/>
```

## Deploying

Configs for three hosts are included. Pick one; [DEPLOY.md](DEPLOY.md) has the full pre-launch checklist.

| Host | Config | Custom headers |
| --- | --- | --- |
| Cloudflare Pages | `public/_headers` | Yes |
| Vercel | `vercel.json` | Yes |
| GitHub Pages | `.github/workflows/deploy-pages.yml` | No; the in-page security policy still applies |

## CI

`.github/workflows/ci.yml` runs on every push and pull request: content check, type check and build; a link check across the built site; and Lighthouse CI, which fails below 100 in any category or above zero layout shift.
