# Salim Braksa — Portfolio

Static portfolio hosted on GitHub Pages. No build step required.

## Structure

- `index.html` — published page
- `layout-draft.html` — local preview
- `assets/css/styles.css` — layout, themes, and styling
- `assets/js/theme.js` — system theme and theme controls
- `assets/js/main.js` — dynamic experience and copyright years
- `assets/images/` — app icons, video posters, and social images
- `assets/videos/` — project recordings
- `content/selected-work.json` — featured project content; descriptions support Markdown
- `scripts/sync-content.py` — synchronizes project content into both pages

## Editing

After editing project content, run `python3 scripts/sync-content.py` from this folder.
Keep page structure changes synchronized between both HTML files. Open `layout-draft.html` for a local preview.
