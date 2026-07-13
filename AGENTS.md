# English landing page playbook

## Mission

Build and maintain the English landing page for the Telegram tarot bot at `https://taro.mom/en/`. Optimize first for useful, indexable, trustworthy content, then for clicks to the bot. Search rankings and AI citations are outcomes to improve toward, never guarantees to claim.

The implementation is a static site hosted on GitHub Pages. Keep the existing Russian home page at `/`; put the English page at `en/index.html`. Do not introduce a framework, build system, backend, analytics, email capture, or another conversion path unless the user explicitly requests it.

## Sources of truth

Use these sources in this order:

1. `taro-bot-website-master-description.md` for product facts, allowed claims, tone, pricing language, features, languages, Premium details, and the disclaimer.
2. The fixed decisions and URLs in this file.
3. `index.html` for existing technical conventions and reusable site assets.
4. `images/referens.png` and `images/referens2.png` for visual direction only.

If sources conflict, preserve the higher-priority source and report the conflict. Never invent features, prices, testimonials, ratings, user counts, credentials, outcomes, contact details, or legal claims.

## Fixed decisions

- Publish the general English version at `/en/`; use `<html lang="en">`.
- Address a broad international English-speaking audience. Use clear, neutral international English. Create country-specific versions only when the user asks or when real regional differences in search demand, offer, payment, law, or terminology justify separate content.
- Use this exact destination for every conversion CTA:
  `https://t.me/taroshenka_bot?start=ref974025936`
- Preserve the entire `start=ref974025936` parameter. It is mandatory for referral attribution. Do not replace it with `https://t.me/taroshenka_bot`, a URL shortener, JavaScript redirect, or a different parameter.
- Use `@taroshenka_bot` and `https://t.me/taroshenka_bot` only for non-conversion identity references such as visible account naming or `sameAs`.
- The site URL is `https://taro.mom/`; the English canonical URL is `https://taro.mom/en/`.
- All one-page landing pages in this repository are published through GitHub Pages. Treat GitHub Pages compatibility as a release requirement.
- Do not add email capture, forms, secondary offers, or competing outbound CTAs.

## GitHub Pages deployment constraints

- Produce deployable static HTML, CSS, JavaScript, images, and metadata files. Do not depend on server-side rendering, PHP, a database, runtime environment variables, custom server headers, or server rewrite rules.
- Implement directory routes with real files: `en/index.html` must serve `/en/`. Do not assume extensionless routing or SPA fallback behavior.
- Preserve the repository's `CNAME` file and the custom domain `taro.mom`. Do not edit or remove `CNAME` unless the user explicitly requests a domain change.
- Treat deployed paths and filenames as case-sensitive. Keep URL casing identical to filesystem casing and use forward slashes in URLs.
- Prefer root-absolute public URLs such as `/images/en/...` and `/favicons/...` because the site is published at the custom-domain root. Verify every asset from the nested `/en/` route.
- Do not commit secrets, API keys, local development addresses, temporary browser profiles, QA screenshots, or generated test artifacts. Anything committed to a GitHub Pages repository must be treated as publicly accessible.
- Keep the page functional when served as plain static files. Use a local static HTTP server for verification because `file://` behavior does not accurately represent GitHub Pages paths.
- After changes to routes or public assets, verify `CNAME`, `robots.txt`, `sitemap.xml`, canonical URLs, `hreflang`, and internal links together before publishing.

## Content requirements

- Write original English copy from the master description; do not mechanically translate the Russian page.
- State the entity early and plainly: this is an AI-powered Tarot reading bot that works in Telegram.
- Use one descriptive `h1` and a logical `h2`/`h3` hierarchy. Keep all important copy visible in server-delivered HTML, not injected by JavaScript or hidden only inside tabs.
- Cover user intent with concise, factual sections: what the bot is, how it works, available reading types, AI interpretation, personalization, Premium and credits, supported languages, FAQ, disclaimer, and CTA.
- Explain Tarot readings as entertainment and self-reflection. Do not promise accurate predictions or outcomes and do not present the bot as a substitute for medical, psychological, legal, financial, or other professional help.
- Use the full disclaimer from the master description in natural English without weakening its meaning.
- Mention prices only with the approved non-specific wording from the master description unless current, channel-specific prices have been separately verified.
- Prefer concrete answer-first sentences that can stand alone when quoted. Keep the bot name, username, feature names, and URLs consistent throughout visible copy, metadata, and structured data.
- Do not keyword-stuff, create doorway copy, add generic filler, or publish claims solely for crawlers. Omit `<meta name="keywords">`; it is not part of the SEO strategy.

## Search and AI discoverability

### Page metadata

- Give `/en/` a unique, descriptive English `<title>`, meta description, `og:title`, `og:description`, `og:url`, `og:locale="en_US"`, Twitter metadata, and a representative large social image.
- Set a self-referencing canonical: `<link rel="canonical" href="https://taro.mom/en/">`.
- Add reciprocal language alternates on both `/` and `/en/`: `hreflang="ru"`, `hreflang="en"`, and `hreflang="x-default"` pointing to the general international English page at `https://taro.mom/en/`. Do not canonicalize English to Russian.
- Ensure title, visible `h1`, Open Graph title, and structured-data naming describe the same page without being exact repetitive spam.

### Crawl and discovery

- Keep navigation and the Telegram CTA as real `<a href="...">` links with descriptive anchor text.
- Update `sitemap.xml` whenever `/en/` is added or materially changed. Include only canonical, indexable URLs and use truthful `lastmod` dates; do not use fake freshness.
- Keep the sitemap declaration in `robots.txt`. Ensure `/en/`, its render-critical assets, Googlebot, Bingbot, and `OAI-SearchBot` are crawlable. An explicit `OAI-SearchBot` allow rule is acceptable for clarity. Do not change `GPTBot` training access without an explicit user decision, and do not claim that allowing any crawler guarantees inclusion or citation.
- Keep the primary content usable without client-side JavaScript. Avoid bot challenges, forced locale redirects, consent walls, or authentication on the landing page.
- After deployment, recommend submitting the sitemap and inspecting `/en/` in Google Search Console and Bing Webmaster Tools. Recommend IndexNow only when deployment support and ownership are available; never fabricate keys or verification tokens.

### Structured data and entity consistency

- Use valid JSON-LD that matches visible page content. Prefer a small connected graph using stable `@id` values for `WebSite`, `WebPage`, and `SoftwareApplication`; add `FAQPage` only when every marked-up question and answer is visibly present.
- Identify the app consistently as a Telegram-based entertainment application. Use `sameAs` for the plain bot identity URL and use the mandatory referral deep link for the visible CTA and `potentialAction.target`.
- Do not add `AggregateRating`, `Review`, authorship, organization details, prices, availability, or other properties without verifiable visible evidence.
- Do not assume structured data creates a rich result. Validate JSON-LD syntax and test applicable markup after implementation.

### Citation-friendly writing

- Make important facts easy to extract: give each section a clear heading and answer its subject in the first sentence.
- Keep facts internally consistent and distinguish free entry points from paid actions without making unsupported promises.
- Include a short FAQ based on genuine user questions, not near-duplicate keyword variations.
- Use semantic HTML landmarks and descriptive internal anchors. Avoid putting key factual text only inside images, canvas, decorative pseudo-elements, or animation.
- Do not create an `llms.txt` as a substitute for crawlability, strong content, sitemap, or robots configuration. Add one only if the user later requests it and its contents can be maintained accurately.

## Visual direction and image workflow

- Inspect both reference images before creating or selecting visuals. Preserve their shared art direction: dark navy and violet mystical interior, luminous cyan/lilac magic, warm candlelight, refined anime-inspired digital illustration, tarot cards, crystals, celestial ornament, and an elegant female reader.
- Treat the references as style guidance, not page assets to duplicate blindly. Keep character appearance, palette, lighting, line treatment, and level of detail consistent across newly generated images.
- Keep the interface sophisticated and readable rather than turning every surface into an illustration. Use dark high-contrast content panels, restrained glow, warm metallic accents, generous spacing, and typography compatible with the existing Cormorant Garamond/Inter direction.
- Preserve the original reference files. Put generated production assets under `images/en/` with short descriptive English filenames.
- For new raster artwork, use the image-generation workflow with both references supplied. Request compositions for the exact placement and aspect ratio; keep important subjects away from text-safe areas and responsive crop boundaries.
- Export production derivatives in modern compressed formats such as AVIF or WebP, with a practical fallback when needed. Do not ship the multi-megabyte references directly as page backgrounds.
- Embed meaningful images with `<img>` or `<picture>`, a real `src` fallback, explicit `width` and `height`, responsive `srcset` where useful, and concise contextual English `alt` text. Use empty `alt` only for genuinely decorative images. Do not rely on CSS background images for important indexable artwork.
- Never place AI-generated pseudo-writing on tarot cards or props where malformed text becomes a focal point. Do not add misleading seals, reviews, platform badges, or certification marks.

## UX, accessibility, and performance

- Mobile devices are the primary target. Design mobile-first, starting with the narrowest supported viewport, and enhance progressively for tablets and desktops. A desktop layout that merely shrinks is not acceptable.
- The page must remain fully usable and visually coherent at widths from 320 px upward and in both portrait and landscape orientation. No horizontal page scrolling, clipped content, overlapping sections, off-screen controls, broken grids, unreadably small text, or CTA buttons wider than their container.
- Use fluid layouts, wrapping flex/grid structures, responsive spacing and typography, and media that never exceeds its container. Do not depend on fixed pixel widths or fixed heights for text-bearing components.
- Keep the primary CTA visible early without obscuring content. Interactive targets must be comfortably touchable, separated from adjacent controls, and usable without hover. Account for mobile safe-area insets where fixed or sticky UI is used.
- Test at minimum at 320, 360, 375, 390, 414, 768, 1024, and 1440 CSS pixels, including long English headings, browser zoom, and increased text size. Treat any mobile layout breakage as a release blocker.
- Meet WCAG 2.2 AA where practical: semantic landmarks, keyboard access, visible focus, sufficient contrast, descriptive controls, reduced-motion support, and no information conveyed by color alone.
- Use progressive enhancement and minimal JavaScript. No autoplay audio, intrusive popups, fake chat notifications, countdowns, or manipulative urgency.
- Aim for good Core Web Vitals: LCP at most 2.5 s, INP at most 200 ms, and CLS at most 0.1 at the 75th percentile. Optimize the hero image, reserve media dimensions, and avoid render-blocking excess.
- Because the page lives under `/en/`, use root-absolute URLs such as `/favicons/...`, `/images/en/...`, and `/manifest.json`, or verify every relative path carefully. Do not copy root-relative assumptions from `index.html` unchanged.

## Required implementation workflow

1. Read this file and the complete master description.
2. Inspect the current root page, `robots.txt`, `sitemap.xml`, `manifest.json`, and both reference images.
3. Define the English search intent, page outline, factual claims, and image placements before coding.
4. Build `en/index.html` as semantic static HTML with responsive CSS and minimal JavaScript.
5. Generate only the images the layout actually needs; optimize them before use.
6. Add reciprocal `hreflang` links to the Russian and English pages, then update sitemap and crawler rules as needed.
7. Verify the exact referral URL in every CTA and relevant structured-data action.
8. Validate through a local static HTTP server and review the rendered page at mobile and desktop widths.
9. Confirm GitHub Pages compatibility: no server-only dependencies, no missing case-sensitive paths, no secrets, and no accidental change to `CNAME`.

## Definition of done

- `en/index.html` resolves conceptually to `https://taro.mom/en/`, is English-only except for proper names, and has a self-canonical.
- `/` and `/en/` expose reciprocal, valid `hreflang` annotations.
- The English page is reachable through a crawlable internal link, and both canonical pages are present in `sitemap.xml` with truthful metadata.
- All conversion links exactly equal `https://t.me/taroshenka_bot?start=ref974025936` and open safely with `rel="noopener noreferrer"` when using `target="_blank"`.
- Product facts and disclaimer agree with the master description; no unsupported prices, ratings, guarantees, or features appear.
- JSON-LD parses and mirrors visible content. FAQ markup, if present, matches the displayed FAQ word for word in substance.
- Important content remains available without JavaScript. Heading order, landmarks, keyboard navigation, focus, contrast, alt text, and reduced motion are checked.
- All local asset paths work from `/en/`; images have dimensions, suitable formats, useful names, and acceptable file sizes.
- Mobile layouts have been manually checked at the required viewport widths and remain intact with long content and increased text size.
- There are no broken links, console errors, horizontal mobile overflow, clipped or overlapping elements, unusable touch targets, accidental layout shifts, or obvious spelling errors.
- The site works from GitHub Pages as static files, `CNAME` still points to the intended custom domain, and no implementation depends on rewrites or backend behavior.
- Report what was verified locally and list deployment-only checks separately. Never report indexing, ranking, Core Web Vitals field data, or AI citations as achieved without external evidence.

## Current authoritative guidance

When SEO behavior may have changed, prefer current primary documentation over remembered rules:

- Google Search Central: [multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites), [helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), [crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), [image SEO](https://developers.google.com/search/docs/appearance/google-images), and [software application structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app).
- Bing: [Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) and [IndexNow guidance](https://www.bing.com/webmasters/help/indexnow-0z209wby).
- OpenAI: [publisher and developer guidance](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq) for `OAI-SearchBot` access and separate `GPTBot` training controls.

Update this playbook when those official requirements or the product source of truth materially change.
