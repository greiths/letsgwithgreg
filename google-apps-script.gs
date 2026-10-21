/**
 * Policy Simulator -> Google Sheet
 * 1. Create a Google Sheet. Extensions > Apps Script. Paste this whole file. Save.
 * 2. Change TOKEN below (same value as SHEET_TOKEN in index.html).
 * 3. Deploy > New deployment > type: Web app
 *      Execute as: Me   |   Who has access: Anyone
 *    Authorize, then copy the Web app URL into SHEET_URL in index.html.
 */
const TOKEN = "change-me-123";
const SHEET_NAME = "Simulations";

const COLUMNS = [
  ["savedAt","Saved at"],["client","Client"],["age","Age"],["gender","Gender"],["smoker","Smoker class"],["datePrepared","Date prepared"],["plan","Plan"],
  ["sfwaCoverage","SFWA coverage"],["sfwaPremium","SFWA annual premium"],["yearsToPay","Years to pay"],
  ["sfwaTotalPremium","SFWA total premium"],["cancerBooster","Cancer booster"],["guaranteedCash","Guaranteed cash benefit"],
  ["hibCI","HIB (CI)"],["postHosp","Post hospitalization"],["homeRecovery","Home recovery"],["palliative","Palliative"],
  ["hibPerDay","HIB per day"],["livingBenefit30","Living benefit 30th yr"],["livingBenefit40","Living benefit 40th yr"],
  ["assureCoverage","LifeAssure coverage"],["assurePremium","LifeAssure annual premium"],["assureTotalTo70","LifeAssure total to age 70"],["combinedAnnual","Combined annual premium"],
  ["advisor","Advisor"],["mobile","Mobile"],["email","Email"]
];

function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  if (data.token !== TOKEN) return ContentService.createTextOutput("unauthorized");
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(COLUMNS.map(c => c[1]));
    sh.getRange(1, 1, 1, COLUMNS.length).setFontWeight("bold");
    sh.setFrozenRows(1);
  }
  const row = COLUMNS.map(c => c[0] === "savedAt" ? new Date(data.savedAt) : (data[c[0]] ?? ""));
  sh.appendRow(row);
  return ContentService.createTextOutput("ok");
}

// Open the Web app URL in a browser to test: it should say "Policy simulator endpoint OK".
function doGet() {
  return ContentService.createTextOutput("Policy simulator endpoint OK");
}
