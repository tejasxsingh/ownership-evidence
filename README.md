# Ownership Evidence

A working browser-based business evidence investigator by Tejas. Built for a payments onboarding analyst who must connect company names to source evidence, inspect disclosed relationships, and record unresolved ownership questions.

## Run

No build or API key is required. Serve `dist` over HTTP:

```sh
python3 -m http.server 4176 --directory dist
```

Open http://localhost:4176. Do not open index.html directly from the filesystem because module loading requires HTTP.

Run automated checks with Node 20+:

```sh
npm test
```

## What works

- Microsoft FY2025 and Alphabet FY2023 subsidiary-table snapshots, with links to original SEC exhibits.
- A trained lexical entity matcher ranks name variations against case entities; inference happens in the browser.
- Text-based PDF, HTML table and TXT import, plus pasted text. Documents stay in the tab.
- Narrow, explicit ownership-statement extraction with source excerpts, line/page references and analyst review.
- Ownership-path arithmetic when a document explicitly supplies percentages. Conflicting claims block affected paths; cycles terminate; distinct paths are not summed.
- Accept, exclude and reset relationship review. Analyst notes and downloadable self-contained HTML case briefs.
- A labeled fictional chain demonstrates 80% × 60% = 48% and conflicting evidence.
- Keyboard controls, responsive layout and two optional WebMCP tools.

## ML, honestly

`ml/train.py` trains logistic regression on six lexical comparison features and exports the exact coefficients used by the browser. 3,840 generated training pairs and 960 validation pairs use disjoint generated base names, but share generation patterns. The threshold is selected on validation data, so reported validation performance is not an independent test result. The model card records the measured result and limitations. This is a name-variant ranker, not a legal identity resolver. Names alone cannot distinguish all businesses, aliases, jurisdictions or legal forms. No score is a verified identity probability. No LLM is used, and document extraction is deterministic.

Reproduce in an isolated Python environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r ml/requirements.txt
python ml/train.py
npm test
```

## Evidence and scope

Microsoft source: https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-ex21.htm (as of 2025-06-30).

Alphabet source: https://www.sec.gov/Archives/edgar/data/1652044/000165204424000022/googexhibit2101q42023.htm (as of 2023-12-31).

Bundled data is a normalized transcription of table facts, not the complete exhibits. Dates are explicit historical snapshots, not claims of freshness. Significant-subsidiary lists may omit entities. They do not establish immediate-parent relationships, percentages or ultimate human owners. Real companies are public-record subjects, not asserted customers. Aster Pay and the Northstar case are fictional.

Trulioo publicly describes source-linked ownership research and entity resolution at https://www.trulioo.com/solutions/business-verification/ubo-discovery. This independent project explores part of that problem. It has no affiliation, internal data, proprietary rules or claimed access to their roadmap.

## Import limits

PDF.js is bundled under its license in `dist/vendor`. Text PDFs only, up to 10 MB / 60 pages. No OCR. The parser supports whole-line `Company A owns 80% of Company B.` / `holds` statements, and two-column pipe-delimited subsidiary tables (HTML rows are converted to that form). Complex prose, wrapped sentences, multilingual filings, tables with extra columns and scanned documents may yield no candidates. The document remains available for manual review. The app does not claim universal document understanding. An uploaded `As of YYYY-MM-DD` date is an unverified claim in the input.

## Persistence and security

This is a deployable portfolio workbench, not a production compliance service. Changes are held in memory and lost on reload or closing the tab. Export first. No login, database, analytics, third-party LLM calls or paid services. Files are processed locally; original-source links open the SEC. HTML input is parsed as data and escaped for rendering, not injected as executable HTML. PDF evaluation is disabled. Do not use it as the sole basis for onboarding, adverse action or a completed KYB/UBO determination.

## Deploy anywhere

Publish the contents of `dist` as a static website. For another host, select the `dist` folder as the publish directory with no build command; no backend or secret is necessary. Keep `.mjs`, `.js` and `.json` MIME types supported. A custom domain is optional and managed at your hosting provider.

## Source map

- `dist/app.js`: case state, UI, file processing and case export.
- `dist/core.js`: matching features, inference, extraction, conflict handling and graph arithmetic.
- `dist/data.js`: dated public facts and fictional example.
- `ml/train.py`: reproducible training and model export.
- `dist/model-card.json`: evaluation and model limitations.
- `tests/core.test.js`: calculation, parsing, matching and escaping tests.
- `DEMO_GUIDE.md`: walkthrough and questions Tejas should be ready to answer.

## GitHub Pages deployment

The included `.github/workflows/pages.yml` runs the tests, then publishes only `dist`.

1. Create a GitHub repository named `ownership-evidence` and upload this project, keeping the directory structure and hidden `.github` folder.
2. In the repository, open Settings → Pages. Set Source to **GitHub Actions**.
3. Push to `main`, or select Actions → Test and deploy Ownership Evidence → Run workflow.
4. The successful deployment shows the live URL under the `github-pages` environment.

No API keys, paid model service, or backend configuration are needed. Relative asset paths support GitHub project URLs. The source ZIP should be extracted before upload; committing a ZIP alone will not deploy the application.

See https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages for the hosting workflow.
