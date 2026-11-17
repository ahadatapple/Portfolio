# Pre-launch checklist

Work top to bottom. Each section ends with a check you can run, so "done" means verified, not assumed.

## 1. Content is ready

- [ ] Everything under **Must do** in [CONTENT.md](CONTENT.md) is ticked, including the PI's and AscentUP's approval.
- [ ] `public/resume.pdf` and `public/resume-ee.pdf` are current. Regenerate them with `resume-source/build_resume.py` after any edit.
- [ ] `npm run build` passes locally.

## 2. Choose a host and deploy

All three serve the site for free. Cloudflare Pages is the recommended default: it applies the security and caching headers in `public/_headers` with no extra setup.

### Cloudflare Pages (recommended)

- [ ] Push the repository to GitHub.
- [ ] Cloudflare dashboard → Workers & Pages → Create → Pages → connect the repository.
- [ ] Build command `npm run build`, output directory `dist`.
- [ ] Environment variable (Production): `NODE_VERSION` = `22`. The site address, `https://ahadatapple.dev`, is already set in `astro.config.mjs`.
- [ ] Deploy. `_headers` is picked up automatically from `dist/`.

### Vercel

- [ ] Import the repository at vercel.com/new. `vercel.json` sets the framework, build command, output directory, clean URLs and headers.
- [ ] No environment variables needed: the site address is set in `astro.config.mjs`.
- [ ] Deploy.

### GitHub Pages

- [ ] Repository Settings → Pages → Source: **GitHub Actions**.
- [ ] Use a custom domain, or name the repository `ahadatapple.github.io`. Any other repository name serves the site from a sub-path (`/repo-name/`), which breaks its links.
- [ ] Push to `main`. `.github/workflows/deploy-pages.yml` builds and deploys.
- [ ] Know the trade-off: GitHub Pages ignores custom headers, so there is no HSTS, frame protection or long-term caching. The in-page Content Security Policy still applies.

**Check:** the `*.pages.dev`, `*.vercel.app` or `*.github.io` address loads, and so does `/projects/gomoku`.

## 3. Custom domain

- [x] Buy the domain: `ahadatapple.dev`, registered at Porkbun.
- [ ] **Cloudflare Pages:** a root domain like `ahadatapple.dev` only works once Cloudflare runs its DNS. In Cloudflare, Onboard a domain → `ahadatapple.dev` → Free plan, and note the two nameservers it assigns. In Porkbun, open the domain's Nameservers setting, replace Porkbun's with Cloudflare's two, and save. Wait for Cloudflare to mark the domain Active, then add it under the Pages project's Custom domains.
- [ ] **Vercel or GitHub Pages:** keep DNS at Porkbun and add the records the host's domain page shows you.
- [ ] Choose the canonical form, `ahadatapple.dev` or `www.ahadatapple.dev`, and redirect the other one to it in the host's domain settings.
- [ ] Wait for the certificate to show as active. It takes from a few minutes to an hour.
- [ ] The site's address is set to `https://ahadatapple.dev` in `astro.config.mjs`. If you choose `www` as canonical instead, change it there and redeploy.

**Check:** `http://ahadatapple.dev` redirects to `https://`, the non-canonical form redirects to the canonical one, and the browser shows a valid certificate.

## 4. Headers and caching

The rules, in `public/_headers` and `vercel.json`:

| Path | Cache-Control | Why |
| --- | --- | --- |
| HTML pages | host default: revalidate every visit | edits appear as soon as a deploy finishes |
| `/_astro/*` | 1 year, immutable | file names change when content does; currently unused, ready for future scripts |
| `/og/*` | 1 day, then serve stale for up to 7 days while refreshing | previews rarely change |
| `/favicon.svg`, `/apple-touch-icon.png` | 1 day | |
| `/resume.pdf`, `/resume-ee.pdf` | 5 minutes, must revalidate | a recruiter should never get an old résumé |

Security headers on every response: HSTS, `nosniff`, a strict referrer policy, permissions policy, `X-Frame-Options: DENY` and `frame-ancestors 'none'`. The page-level Content Security Policy comes from `scripts/csp.mjs`.

**Check:** run these against your domain and confirm each header appears.

```sh
curl -sI https://ahadatapple.dev/ | grep -iE 'strict-transport|x-frame|content-security|referrer|cache-control'
curl -sI https://ahadatapple.dev/resume.pdf | grep -i cache-control
curl -sI https://ahadatapple.dev/og/home.png | grep -iE 'content-type|cache-control'
```

Then scan with securityheaders.com. Expect an A on Cloudflare Pages or Vercel.

Leave HSTS preload alone until the domain has run on HTTPS for a few months. Preloading is hard to undo.

## 5. Link previews

- [ ] View source on the live home page: `og:image` and `twitter:image` start with `https://ahadatapple.dev/`, not `/`. 
- [ ] Open `https://ahadatapple.dev/og/home.png` and each `/og/<slug>.png`.
- [ ] **LinkedIn:** paste the home page and each case study URL into LinkedIn's Post Inspector. It also refreshes LinkedIn's cache after a change.
- [ ] **Slack:** post the URL in a private channel or a DM to yourself. Slack caches previews; add `?v=2` to a URL to see a fresh one.
- [ ] **X:** paste the URL into a new post and check the preview card before discarding the draft.
- [ ] **iMessage:** send the link to yourself.

## 6. Final checks

- [ ] `https://ahadatapple.dev/nope` shows the custom 404 page with a 404 status.
- [ ] `/sitemap-index.xml` lists all four pages under your domain, and `/robots.txt` points to it.
- [ ] Lighthouse on the live home page and one case study: 100 across the board. Host-level tools can change this, so check the live site.
- [ ] Turn off anything the host injects: Cloudflare's Web Analytics beacon, Rocket Loader and email obfuscation; Vercel's toolbar. Each adds a script the Content Security Policy will block.
- [ ] Open the site on a phone, switch the theme, and reload: the choice persists.
- [ ] Tab through the home page with a keyboard: skip link first, then a visible focus ring on each link.
- [ ] Add the URL to LinkedIn (Contact info and Featured) and your GitHub profile. Both résumés already link to it.

## 7. After launch

- [ ] Search Google for `site:ahadatapple.dev` after a week. Submit the sitemap in Google Search Console if pages are missing.
- [ ] Update the gesture page's `status` each month.
- [ ] Re-run LinkedIn's Post Inspector whenever a preview image changes.
