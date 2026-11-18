# LERSAIS-Website
This is the repo for LERSAIS Lab, University of Pittsburgh, maintained by Ph.D. student Peilin He.

## Preview locally

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. The root and `index.html` redirect to `research.html`, the combined lab homepage. Research contains the lab introduction, research areas, news and events, community, and education overview. The site is static HTML/CSS/JavaScript; no Node packages, framework, or backend are required. All content and links work without JavaScript; search, filters, the mobile menu, and the photo viewer are progressive enhancements.

## Edit and build

- `scripts/build_site.py`: page templates, shared navigation/footer, and research/education copy.
- `data/people.json`: member biographies, portraits, roles, and original profile links. Portraits are cropped to circles; the optional `image_style` zooms or re-centers one that needs it.
- `data/news.json`: news stories and past conferences, with dates, local images, and original source links.
- `data/grants.json`: selected James Joshi awards transcribed from his public CV or NSF award records (linked per grant with `source_url`), including funding, periods, roles, source URL, and the review date. Review status labels when refreshing this file; the Machine Unlearning award retains the CV's NCE note without assuming an extension end date.
- `data/image-sizes.json`: original image dimensions; update these when adding or replacing photos. Image frames outside People preserve proportions and do not upscale small source images.
- `css/site.css`: shared responsive design and accessibility styles.
- `js/site.js`: local search, filters, navigation, and gallery interactions.

After editing templates or content, run:

```sh
python3 scripts/build_site.py
```

This regenerates seven content pages, redirects from `index.html` to `research.html` and from `publications.html` to `grants.html`, the shared header/footer fragments, and `data/search-index.json`. The homepage redirect preserves query strings and anchor links when JavaScript is enabled; a meta refresh and a visible link provide a fallback. Commit the generated files too; any static host can serve them directly. Use a local HTTP server to preview keyword search, since browsers restrict fetching JSON from `file://` URLs.

Research and education summaries use existing lab information. Member biographies and student status are maintained in `data/people.json`. Conference records and screenshots use their official year-specific websites. Google Scholar links remain in People; Grants contains James Joshi's active/recent awards and selected past grants. Grant amounts and periods follow his CV or the linked NSF award record. Submitted or under-review proposals are not listed as awarded grants.
