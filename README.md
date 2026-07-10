# edwardjedmonds.com

The public archive — evergreen essays and reference articles on physiology, nutrition
science, lipid metabolism, and pathology. Built with [Hugo](https://gohugo.io) and deployed
to GitHub Pages. The newsletter (Buttondown) is the separate, subscriber-facing channel.

## Writing workflow

```
read papers → take notes → write Markdown → commit → auto-publish
```

Everything lives in this repo as portable Markdown. There is no external theme — all
layouts and styles are in `layouts/` and `assets/`, so nothing can rot or go unmaintained.

## Local preview

Requires **Hugo extended ≥ 0.164** (`hugo version` should say `+extended`).

```sh
hugo server -D      # live preview at http://localhost:1313 (-D shows drafts)
```

## Creating content

```sh
hugo new content essays/my-new-essay.md       # long-form essay
hugo new content concepts/oxidative-stress.md # short reference article
hugo new content notes/reading-2026-07.md     # short research note
```

New files start with `draft: true`. Set it to `false` (or delete the line) to publish.

### Front matter options

| Field         | Purpose                                                        |
|---------------|----------------------------------------------------------------|
| `title`       | Article title                                                  |
| `date`        | Publish date (controls ordering)                               |
| `description` | One–two sentences; used for SEO, social cards, and list blurbs |
| `tags`        | Topic tags for clustering, e.g. `["lipids", "history of science"]` |
| `math: true`  | Load KaTeX on this page (only when you use math)               |
| `toc: true`   | Show a table of contents (good for long essays)                |
| `draft: true` | Hide from the built site until ready                           |

### Formatting cheatsheet

- **Footnotes:** `some claim.[^1]` … then `[^1]: the citation.`
- **Math:** inline `\( E = mc^2 \)`, display `$$ ... $$` (needs `math: true`).
- **Figures:** drop images in `static/figures/`, then
  `{{</* figure src="/figures/x.svg" class="numbered" caption="..." */>}}`
  (`class="numbered"` auto-numbers the caption "Figure 1.", "Figure 2.", …).
- **Cross-links:** `[lipid peroxidation]({{</* relref "concepts/lipid-peroxidation" */>}})`.

## Structure

```
content/essays/     long-form essays
content/concepts/   short reference articles (SEO-facing)
content/notes/      short research notes
static/figures/     images and diagrams
layouts/            HTML templates (the "theme")
assets/css/         styles
```

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds with Hugo and
publishes to GitHub Pages. One-time setup: **Settings → Pages → Source → GitHub Actions**.

## Custom domain (later)

When you're ready to point `edwardjedmonds.com` here:

1. Add a `CNAME` file at the repo root containing `edwardjedmonds.com`.
2. Change `baseURL` in `hugo.toml` to `https://edwardjedmonds.com/`.
3. At your DNS registrar, add the four GitHub Pages `A` records (apex) — and a `www` CNAME to
   `edwardedmonds.github.io` if you want `www`.
4. In **Settings → Pages**, set the custom domain and enable "Enforce HTTPS".

## Known dependency: KaTeX

Math is rendered by KaTeX loaded from a CDN, and only on pages that set `math: true`. For a
fully offline-durable archive you can self-host KaTeX by vendoring its CSS/JS/fonts into
`static/` and updating `layouts/partials/head.html`. Everything else has zero runtime
dependencies.
