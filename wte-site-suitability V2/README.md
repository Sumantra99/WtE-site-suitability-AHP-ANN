# Waste-to-Energy Site Suitability Explorer

By Sumantra Chaudhuri · Environmental engineering research portfolio

A complete, no-build interactive website and reproducible Python analysis based on **Development of Location Suitability Index for Waste-to-Energy plant by MCDM & ANN techniques**. Uses the supplied report's four candidate sites and ten factors. Includes real source tables, original documents, actual computed results, tests, and a new optional neural-network surrogate experiment. No empty placeholder datasets or mock model artifacts are included.

## Open immediately — no coding required
Double-click `index.html`. The explorer works offline without Python, npm, API keys, a backend, or a CDN. Edit weights and Q values, compare rankings, reset to the report, and export the current scenario as CSV.

## Upload to GitHub — easiest route
1. Sign in and open https://github.com/new .
2. Set repository name to `wte-site-suitability`, choose Public if the report can be shared, and create the repository. You may initialize with a README to make the Upload files button visible.
3. Extract the supplied ZIP on your computer. Open the extracted project folder.
4. In the repository choose **Add file → Upload files** (an empty repository also offers **uploading an existing file**).
5. Drag the CONTENTS of the project folder into the upload area, including the subfolders. Do not upload only the ZIP, and do not wrap everything in an extra project folder. `index.html` and `README.md` must be at repository root. Hidden `.github` and `.gitignore` may need "show hidden files" on your computer; the website still works without the optional test workflow.
6. Click **Commit changes**. The repository page is your shareable project link; copy its address from your browser.
7. Enable the website: **Settings → Pages → Source: Deploy from a branch → main → /(root) → Save**. GitHub will display the real website URL after deployment. If your default branch has another name, select that branch instead.

GitHub's instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

No live repository URL is claimed in this package: publication happens in your own GitHub account. Review source-document sharing rights before making the repository public.

## What is included
- `index.html`, `style.css`, `app.js`, `web-data.js`: offline-capable interactive website, with live scoring, input validation, ranking bars and CSV download.
- `data/`: transcribed factor weights, raw case-study measurements, published Q values, original reported scores, and available randomized ANN rows.
- `analysis.py`: weighted SI recomputation, AHP eigenvector/CR audit, published-row metrics, optional 10–5–1 surrogate and linear baseline.
- `results/`: generated ranking CSV, audit JSON, new ANN test predictions and comparison chart from an actual execution.
- `tests/test_analysis.py`: executable numerical checks.
- `.github/workflows/tests.yml`: automated Python checks on push and pull request.
- `reports/`: original PDF report and PowerPoint.
- `docs/METHODOLOGY.md`: source tables, formulae, discrepancies and limits.

## Scientific caution
The report identifies A3 as best. Recomputing Table 8 using Table 4 also ranks A3 first, and numerical SI values match those printed in the report to rounding precision. Both versions are exposed. Geological-fault raw measurements and raw-to-Q transformations are unresolved. No missing measurements are invented. The website uses normalized Q directly, not a fabricated raw-data conversion. Read the methodology audit before using or presenting the results.

The ANN is a new synthetic surrogate experiment, NOT the recovered MATLAB model or independent validation. A weighted linear target does not require a neural network; the included linear baseline makes that explicit.

## Run the Python analysis (optional)
Requires Python 3.10 or later. Open a terminal inside this folder:

```sh
python -m venv .venv
```

Windows activation:
```powershell
.venv\Scripts\activate
```
macOS/Linux activation:
```sh
source .venv/bin/activate
```
Then:
```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python analysis.py
python analysis.py --train-ann
```

`analysis.py` writes ranking, audit and comparison chart to `results/`. `--train-ann` additionally runs the new synthetic experiment and saves held-out test predictions. Training may vary slightly by numerical-library version.

## Edit data
Factor order must remain DR,CV,GF,DW,LN,ES,HD,LC,DD,AI. Python reads CSV files in `data/`. The offline website uses the same baseline values embedded in `web-data.js`; if permanently replacing baseline data, update that file as well. Browser edits are temporary and do not change the repository; export a CSV to retain your scenario.

## Troubleshooting
- Website shows a repository README instead of the explorer: verify root `index.html` and Pages branch/folder settings.
- Downloaded ZIP opens as a file list: extract it before opening `index.html`.
- Inputs are rejected: all weights must be nonnegative, total weight must exceed zero, and every Q must lie within [0.1,0.9].
- Python says numpy is missing: activate the virtual environment and install requirements.
- Automated checks are absent: the optional hidden `.github/workflows/tests.yml` folder was probably omitted during browser upload. Upload it or use Git.

## Optional Git upload
After creating an empty repository on GitHub, run inside this folder:
```sh
git init
git add .
git commit -m "Add WtE suitability research project"
git branch -M main
```
Then copy and run the `git remote add origin ...` command shown by GitHub for YOUR repository, followed by `git push -u origin main`. Your GitHub authentication is handled locally; do not put tokens in project files.

## Attribution and permissions
Original research attribution is retained. No blanket open-source license is assigned automatically to the author's report, presentation, or externally sourced case-study data. Review rights and select a code/data license before authorizing redistribution. This project is educational research software, not a statutory site-selection assessment.
