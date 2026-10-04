# Salim Braksa — Portfolio

Astro portfolio hosted on GitHub Pages. The existing design and theme are preserved.

## Structure

- `src/pages/index.astro` — single page template
- `src/components/ProjectCard.astro` — reusable project card
- `src/styles/global.css` — layout and light/dark themes
- `content/selected-work.json` — project descriptions in Markdown, ratings, tags, and media
- `public/assets/` — images, videos, and theme scripts
- `.github/workflows/deploy.yml` — automatic GitHub Pages publishing

## Local development

Run `npm install`, then `npm run dev` and open the local URL printed in the terminal.
Edit the JSON or page components; Astro refreshes the preview automatically.
The old file-based preview and Python synchronization script are no longer needed.

## Publishing

Select **GitHub Actions** under repository Settings → Pages → Source.
Push to `main` to generate and publish the static site automatically.
`npm run build` generates `dist/`; `npm run preview` previews that output.
