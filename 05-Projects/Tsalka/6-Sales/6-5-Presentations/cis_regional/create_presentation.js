const pptxgen = require('pptxgenjs');
const html2pptx = require('../.agent/skills/pptx/scripts/html2pptx');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Green Canyon Eco Village';
    pptx.title = 'CIS Regional Presentation';

    // Slide 1
    console.log('Processing Slide 1...');
    await html2pptx(path.join(__dirname, 'slides/slide1.html'), pptx);

    // Slide 2
    console.log('Processing Slide 2...');
    const { slide: slide2, placeholders: ph2 } = await html2pptx(path.join(__dirname, 'slides/slide2.html'), pptx);

    // Add Chart to Slide 2
    if (ph2 && ph2.length > 0) {
        // Find mix-chart placeholder
        const mixPh = ph2.find(p => p.id === 'mix-chart') || ph2[0];

        if (mixPh) {
            slide2.addChart(pptx.charts.PIE, [
                {
                    name: "Usage Allocation",
                    labels: ["Rental Income (50 weeks)", "Personal Use (2 weeks)"],
                    values: [96, 4]
                }
            ], {
                x: mixPh.x, y: mixPh.y, w: mixPh.w, h: mixPh.h,
                showLegend: true, legendPos: 'b',
                showTitle: true, title: "Calendar Optimization",
                chartColors: ["2E4053", "D4AC0D"],
                dataLabelFormatCode: '#%'
            });
        }
    }

    // Slide 3
    console.log('Processing Slide 3...');
    await html2pptx(path.join(__dirname, 'slides/slide3.html'), pptx);

    // Slide 4
    console.log('Processing Slide 4...');
    await html2pptx(path.join(__dirname, 'slides/slide4.html'), pptx);

    // Slide 5
    console.log('Processing Slide 5...');
    await html2pptx(path.join(__dirname, 'slides/slide5.html'), pptx);

    // Save
    const outputPath = path.join(__dirname, 'Presentation_CIS_Regional.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Presentation created successfully at ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});
