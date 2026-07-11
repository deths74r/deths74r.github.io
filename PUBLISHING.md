# Publishing Guide

How to write and publish a new essay on **edwardjedmonds.com**.

The whole flow is: **write Markdown → preview → set `draft: false` → commit → push.**
GitHub builds and deploys the site automatically; your essay is live in ~1–2 minutes.

---

## One-time setup

Hugo lives in `~/go/bin`. Add it to your PATH once (fish shell) so you can just type `hugo`:

```fish
fish_add_path ~/go/bin
```

If you skip this, use the full path `~/go/bin/hugo` wherever `hugo` appears below.

---

## The steps

### 1. Create the file

```fish
hugo new content essays/your-essay-slug.md
```

**The filename becomes the URL.** `essays/lipid-peroxidation-revisited.md` →
`edwardjedmonds.com/essays/lipid-peroxidation-revisited/`. Use lowercase words separated by
hyphens, and make it descriptive — the slug matters for SEO.

This scaffolds a ready-to-write essay — front matter (with `draft: true`) plus a light body
skeleton (intro, sections, a footnote example). Just fill it in.

**Writing a math-heavy essay?** Use the math template instead — it adds `math: true`, `toc: true`,
and example equations:

```fish
hugo new content essays/your-essay-slug.md --kind math-essay
```

(The templates live in `archetypes/` — `essays.md` is the default; `math-essay.md` is the variant.)

### 2. Fill in the front matter

The block between the two `---` lines at the top of the file:

```yaml
---
title: "The Title of Your Essay"
subtitle: "An optional one-line deck shown under the title"
date: 2026-07-10
description: "One or two sentences summarizing the essay. Write this well — it's your Google result snippet, your social-card text, and your search/list blurb."
tags: ["lipids", "metabolism", "history of science"]
toc: true
math: false
draft: true
---
```

| Field | What it does |
|---|---|
| `title` | The headline — H1, browser tab, and the generated social card. |
| `subtitle` | Optional deck under the title. Delete the line if you don't want one. |
| `date` | Publish date (`YYYY-MM-DD`). Controls ordering (newest first). |
| `description` | **Write this well.** Used for the Google snippet, the social share card, and the on-site search/list blurb. ~1–2 sentences. |
| `tags` | Topic tags in `[ ]`. Helps grouping and SEO. |
| `toc` | `true` adds a table of contents — use it for long, multi-section essays. |
| `math` | `true` only if you use LaTeX math (loads the math renderer for that page). |
| `draft` | `true` hides it from the built site. **Set to `false` to publish.** |

### 3. Write the essay

Below the closing `---`, write in Markdown:

- Headings: `## Section`, `### Subsection`
- Emphasis: `**bold**`, `*italic*`
- Lists: `- item` or `1. item`
- Blockquote: `> quoted text`
- Link: `[text](https://example.com)`
- Link to another essay: `[text]({{< relref "essays/other-slug" >}})`
- Footnote: `...a claim.[^1]` then, on its own line, `[^1]: The source.`
- Table: standard Markdown pipes (`| col | col |`).
- Math (needs `math: true`): inline `\( E = mc^2 \)`, block `$$ ... $$`
- Figure: put the image in `static/figures/`, then
  `{{< figure src="/figures/name.png" class="numbered" caption="Your caption." >}}`
  (`class="numbered"` auto-labels it "Figure 1.", "Figure 2.", …)

### 4. Preview locally

```fish
hugo server -D
```

Open **http://localhost:1313** — the `-D` flag shows drafts. Edits reload live. Check that it
reads well, links work, and images load. Stop the server with `Ctrl-C`.

> On-site search does **not** run under `hugo server` (the index is built at deploy time). To
> preview search too, use the full build command in `README.md`.

### 5. Publish

1. Set `draft: false` in the front matter (or delete the `draft:` line).
2. Commit and push:

```fish
git add -A
git commit -m "New essay: The Title of Your Essay"
git push
```

That's it. GitHub Actions builds the site, generates the social card, updates the search
index, and deploys. **Live at edwardjedmonds.com in ~1–2 minutes.**

Watch the deploy at <https://github.com/deths74r/deths74r.github.io/actions>.

---

## What happens automatically

When you publish, the essay automatically gets:

- A place on the homepage and the `/essays/` list (ordered by date)
- A generated 1200×630 social share card with its title
- Full SEO: meta description, Open Graph / Twitter tags, JSON-LD structured data
- An entry in the sitemap (`/sitemap.xml`) and the RSS feed (`/index.xml`)
- Inclusion in the on-site search index

Writing the Markdown is the whole job — no extra wiring.

---

## Editing or revising a published essay

Same flow: edit the file, commit, push. If it's a substantial revision and you want the page
to show a "Last revised" line, add a `lastmod` field to the front matter:

```yaml
lastmod: 2026-08-01
```

---

## Optional: nudge Google to index it sooner

After publishing an important essay, go to Google Search Console → **URL Inspection**, paste the
new URL, and click **Request indexing**. Otherwise Google will find it on its own via the sitemap,
usually within days.

---

## Quick reference

```fish
hugo new content essays/my-essay.md          # 1. create
# 2–3. edit content/essays/my-essay.md: fill front matter, write the essay
hugo server -D                               # 4. preview at http://localhost:1313
# 5. set draft: false, then:
git add -A && git commit -m "New essay: ..." && git push
```

---

*Note: `essays/` is the active section. `concepts/` and `notes/` exist in the repo but are
currently unlinked and hidden from search — say the word if you want to start using them.*
