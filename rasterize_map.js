const { chromium } = require('playwright-core');
const fs = require('fs');

(async () => {
    let browser;
    try {
        const pw = require('playwright');
        browser = await pw.chromium.launch();
    } catch(e) {
        try {
            browser = await chromium.launch({
                executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
            });
        } catch(e2) {
            console.error("Could not launch browser:", e2);
            process.exit(1);
        }
    }
    
    // We create a very clean page
    const page = await browser.newPage();
    const svgPath = 'C:\\Users\\Nodar\\2026 antigraviti\\05-Projects\\Tsalka\\6-Sales\\6-4-Marketing\\2025PRV05TGGM-2026-FEB-5.svg';
    let svg = fs.readFileSync(svgPath, 'utf8');
    
    // Remove text overlays for the background map
    svg = svg.replace(/<text[\s\S]*?<\/text>/g, '');
    svg = svg.replace(/maskUnits="userSpaceOnUse"/g, 'maskUnits="objectBoundingBox"');
    
    // Force SVG dimensions exactly to 3000 x 4248
    svg = svg.replace(/<svg([^>]*)width="[^"]*"/, '<svg$1width="3000"');
    svg = svg.replace(/<svg([^>]*)height="[^"]*"/, '<svg$1height="4248"');
    
    const html = `<!DOCTYPE html>
    <html>
    <style>body { margin: 0; padding: 0; background: #FFF; }</style>
    <body>
        ${svg}
    </body>
    </html>`;
    
    await page.setViewportSize({ width: 3100, height: 4300 }); // Slightly larger viewport to fit SVG without scrollbars altering size
    await page.setContent(html, { waitUntil: 'networkidle' });
    
    // Give time to render
    await page.waitForTimeout(2000);
    
    // Create correct asset directory
    const outDir = 'C:\\Users\\Nodar\\2026 antigraviti\\05-Projects\\Tsalka\\6-Sales\\6-4-Marketing\\Assets';
    if(!fs.existsSync(outDir)) fs.mkdirSync(outDir, {recursive: true});
    
    const outPath = outDir + '\\masterplan_leaflet.png';
    
    // SCREENSHOT ONLY THE SVG ELEMENT TO GUARANTEE BOUNDS !
    const svgElement = page.locator('svg');
    await svgElement.screenshot({ path: outPath });
    
    console.log('Rasterized exact SVG successfully (no margins).');
    await browser.close();
})();
