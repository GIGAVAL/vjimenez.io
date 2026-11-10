# vjimenez.io

Portfolio site of Valerie Jimenez, architect in New York City.

**Live:** [www.vjimenez.io](https://www.vjimenez.io), served by GitHub Pages from this repo

Architecture for regulated platforms: fourteen years and 20+ public-use facilities at $2.7B+ aggregate, with operator fluency in design and real estate finance.

## Sections

- **Infrastructure:** transit and civic work
- **Justice:** courthouses and court studies
- **Practice:** office, interiors, development and real estate analysis
- **Editorial:** conference notes and writing (PDFs in `editorial/`)
- **Repo:** software projects, such as [sheetcheck](https://gigaval.github.io/sheetcheck/demo.html) and [fire002-handover](https://github.com/GIGAVAL/fire002-handover)

## Structure

| Path | What it holds |
|---|---|
| `index.html` | The whole site: one page, inline CSS and JS |
| `projects-data.js` | Project list data used by the page |
| `images/` | Project images, grouped by project |
| `archive/` | Full portfolio PDFs |
| `editorial/` | Editorial PDFs |

No build step. Plain static files.

## Run locally

```bash
python3 -m http.server 4400
```

Then open http://localhost:4400.

## Deploy

Push to `master`. GitHub Pages rebuilds www.vjimenez.io in about a minute. The `CNAME` file sets the custom domain, and Squarespace forwards the bare vjimenez.io to www.
