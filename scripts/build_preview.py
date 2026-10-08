"""Build a no-install preview and GitHub Pages assets from verified synthetic data."""

import shutil
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    source = root / "app/static"
    target = root / "docs/demo"
    target.mkdir(parents=True, exist_ok=True)
    html = (
        (source / "index.html")
        .read_text()
        .replace('data-preview="false"', 'data-preview="true"')
        .replace("/static/", "")
    )
    (target / "index.html").write_text(html)
    for name in ["style.css", "app.js", "demo-data.js"]:
        shutil.copy2(source / name, target / name)
    (root / "docs/.nojekyll").touch()
    bundled = html.replace(
        '<link rel="stylesheet" href="style.css">',
        "<style>" + (source / "style.css").read_text() + "</style>",
    )
    bundled = bundled.replace(
        '<script src="demo-data.js"></script>',
        "<script>" + (source / "demo-data.js").read_text().replace("</script", "<\\/script") + "</script>",
    )
    bundled = bundled.replace(
        '<script src="app.js"></script>',
        "<script>" + (source / "app.js").read_text().replace("</script", "<\\/script") + "</script>",
    )
    (root / "OPEN_DEMO.html").write_text(bundled)
    (root / "docs/index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=demo/"><title>Hotel guest experience demo</title></head><body><a href="demo/">Open interactive synthetic demo</a></body></html>'
    )
    print("Built browser-only demo and docs/demo/ Pages preview")


if __name__ == "__main__":
    main()
