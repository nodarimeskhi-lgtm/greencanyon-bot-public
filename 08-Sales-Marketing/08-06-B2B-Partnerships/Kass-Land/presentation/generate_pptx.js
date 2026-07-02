const html2pptx = require('c:/Users/Nodar/2026 antigraviti/.agent/skills/pptx/scripts/html2pptx.js');
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

async function createPresentation() {
  const htmlPath = 'c:/Users/Nodar/2026 antigraviti/08-Sales-Marketing/08-06-B2B-Partnerships/Kass-Land/presentation/slides.html';
  const outputPath = 'c:/Users/Nodar/2026 antigraviti/08-Sales-Marketing/08-06-B2B-Partnerships/Kass-Land/Kass_Land_Partnership_Presentation.pptx';
  
  try {
    console.log('Generating presentation...');
    const pres = new pptxgen();
    pres.layout = 'LAYOUT_16x9';
    
    // The html2pptx script expects to be called for each slide if multiple slides are in one HTML?
    // Actually, looking at the code, it processes one HTML as one slide.
    // But my HTML has multiple slides? No, my HTML has multiple .slide divs.
    // Wait, the html2pptx script might not handle multiple slides in one HTML.
    // I should probably split the HTML or adjust the script.
    
    // Let's check if html2pptx handles multiple slides.
    // Based on extractSlideData, it looks for all elements on the page.
    // It doesn't seem to split by .slide class.
    
    // I will split my HTML into individual files.
    console.log('Splitting HTML into individual slides...');
    const slidesHtml = fs.readFileSync(htmlPath, 'utf8');
    const slideMatches = slidesHtml.match(/<!-- Slide \d+: .*? -->[\s\S]*?<div class="slide[\s\S]*?<\/div>/g);
    
    if (!slideMatches) {
      console.log('No individual slides found, processing entire file as one slide.');
      await html2pptx(htmlPath, pres);
    } else {
      for (let i = 0; i < slideMatches.length; i++) {
        const slideHtml = `<!DOCTYPE html><html><head><style>${slidesHtml.match(/<style>[\s\S]*?<\/style>/)[0].replace(/<style>|<\/style>/g, '')}</style></head><body>${slideMatches[i]}</body></html>`;
        const tempSlidePath = path.join(path.dirname(htmlPath), `slide_${i}.html`);
        fs.writeFileSync(tempSlidePath, slideHtml);
        console.log(`Processing slide ${i}...`);
        await html2pptx(tempSlidePath, pres);
      }
    }

    await pres.writeFile({ fileName: outputPath });
    console.log('Presentation created successfully at:', outputPath);
  } catch (error) {
    console.error('Error creating presentation:', error.message);
    console.error(error.stack);
  }
}

createPresentation();
