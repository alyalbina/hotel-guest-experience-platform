# Publishing on GitHub and a free demo

Repository name: **hotel-guest-experience-platform**. Repository owner selected for publication: **alyalbina**. Public name: **Hotel Guest Experience & Service Automation Platform**.

A public repository was created under `alyalbina` on 8 October 2026 (UTC). Source upload and GitHub Pages deployment are being verified separately. The publication package contains clean source and synthetic assets; the original archives, thesis PDF, credentials and operational databases are excluded.

## Publish the repository

Create a public repository under the intended personal account using the exact name above. Avoid importing the original ZIP or thesis PDF. Upload the contents of this project folder, including `.github/workflows`, `.gitignore` and `.env.example`; exclude local `.venv`, database, caches and `.env`. The supplied clean archive already excludes them.

With Git installed, the equivalent commands from the clean project folder are:

```bash
git init -b main
git add .
git commit -m "Add thesis-derived hotel service platform and synthetic demo"
git remote add origin https://github.com/alyalbina/hotel-guest-experience-platform.git
git push -u origin main
```

GitHub authentication uses your normal account flow. Do not paste account tokens into source or chat. Before pushing, run `python scripts/check_public_tree.py` and inspect `git status`. If an existing repo is supplied, fetch/read its state before adding files rather than replacing unrelated content.

## Free public preview with GitHub Pages

GitHub's [official Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) describes static hosting and free access for public repositories. It runs HTML/CSS/JS; it does not run Python, SQLite or polling bots.

After upload: repository **Settings → Pages → Deploy from a branch → main → /docs → Save**. `docs/.nojekyll` and `docs/index.html` are provided. The preview path is:

`https://alyalbina.github.io/hotel-guest-experience-platform/demo/`

This URL is a planned deployment address until Pages reports success. Confirm it loads in a signed-out browser, filters work, a preview update changes history, and refresh resets it. The README already explains this publishing boundary.

## Finish the portfolio page

Use the About description/topics in [portfolio](portfolio.md), set the website to the live preview only after it works, and pin the repository on your profile. CI is configured; inspect the first real workflow result before claiming GitHub CI passed. Avoid setting a production deployment badge or uptime figure without evidence.

Licensing the original source requires clarity about contribution rights. This clean rebuild does not bundle original code or a thesis copy, and no open-source license has been assigned on behalf of an unknown original contributor. Choose a repository license only after clarifying what you own and intend to license; public visibility alone does not make it open source.
