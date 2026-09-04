# LERSAIS-Website
This is the repo for LERSAIS Lab, University of Pittsburgh, maintained by Ph.D. student Peilin He.

## Preview locally

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. The site is static HTML/CSS/JavaScript; no Node packages, framework, or backend are required. All navigation and content work without JavaScript; search, filters, the mobile menu, and the photo viewer are progressive enhancements.

## Edit and build

- `scripts/build_site.py`: page templates, shared navigation/footer, and research/education copy.
- `data/people.json`: member biographies, portraits, roles, and original profile links.
- `data/news.json`: news stories and original source links/dates.
- `data/image-sizes.json`: original image dimensions; update these when adding or replacing photos. Image frames preserve proportions and do not upscale small source images.
- `css/site.css`: shared responsive design and accessibility styles.
- `js/site.js`: local search, filters, navigation, and gallery interactions.

After editing templates or content, run:

```sh
python3 scripts/build_site.py
```

This regenerates all eight HTML pages, the shared header/footer fragments, and `data/search-index.json`. Commit the generated files too; any static host can serve them directly. Use a local HTTP server to preview keyword search, since browsers restrict fetching JSON from `file://` URLs.

The redesign retains all 31 original member profiles and all six original homepage stories. Research and education summaries use existing lab information. The old publication page contained template examples; the replacement links to the researchers' existing Google Scholar profiles rather than presenting sample papers as lab output. Member biographies and dated news are retained as provided, not independently updated.
