const puppeteer = require('playwright');
(async () => {
  const browser = await puppeteer.chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));
  await page.goto('file:///Users/fox/Documents/PROJECTS/LokumAI/LokumAI_Graphify.html');
  await page.waitForTimeout(2000);
  await browser.close();
})();
