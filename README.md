# Health Plan Comparison – Policy Simulator

Compares **Sun Fit and Well Advantage 10 / 20** against **Sun LifeAssure**, using the formulas from the original Excel comparison sheets.

## Deploy on GitHub Pages
1. Create a repo and upload all files in this folder (`index.html`, `sw.js`, `manifest.webmanifest`, `icon.svg`).
2. Settings → Pages → Source: *Deploy from a branch* → `main` / root → Save.
3. Open the Pages URL once while online. After that it works offline, and on a phone you can "Add to Home Screen".

When you update `index.html`, also change `VERSION` in `sw.js` so devices fetch the new copy.

## Formulas (from the workbook)
| Benefit | Formula |
|---|---|
| Accidental death benefit | = coverage |
| Specific cancer booster | = coverage ÷ 2 |
| Guaranteed cash benefit | = 5% × coverage |
| HIB (critical illness) | = 0.125% × coverage |
| Home recovery benefit | = 0.0625% × coverage |
| Palliative benefit | = 10% × coverage |

Annual premiums and living benefits are entered from the official proposal.
