const pptxgen = require('pptxgenjs');
const html2pptx = require('../.agent/skills/pptx/scripts/html2pptx');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Green Canyon Eco Village';
    pptx.title = 'Family Sanctuary Presentation';

    // Slide 1
    console.log('Processing Slide 1...');
    await html2pptx(path.join(__dirname, 'slides/slide1.html'), pptx);

    // Slide 2
    console.log('Processing Slide 2...');
    await html2pptx(path.join(__dirname, 'slides/slide2.html'), pptx);

    // Slide 3
    console.log('Processing Slide 3...');
    await html2pptx(path.join(__dirname, 'slides/slide3.html'), pptx);

    // Slide 4
    console.log('Processing Slide 4...');
    await html2pptx(path.join(__dirname, 'slides/slide4.html'), pptx);

    // Slide 5
    console.log('Processing Slide 5...');
    await html2pptx(path.join(__dirname, 'slides/slide5.html'), pptx);

    // Slide 6
    console.log('Processing Slide 6...');
    await html2pptx(path.join(__dirname, 'slides/slide6.html'), pptx);

    // Save
    const outputPath = path.join(__dirname, 'Presentation_Family_Sanctuary.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Presentation created successfully at ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});
