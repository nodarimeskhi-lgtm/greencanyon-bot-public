const pptxgen = require('pptxgenjs');
const html2pptx = require('../.agent/skills/pptx/scripts/html2pptx');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Green Canyon Eco Village';
    pptx.title = 'Eco-Nomad Base Presentation';

    // Slide 1
    console.log('Processing Slide 1...');
    await html2pptx(path.join(__dirname, 'slides/slide1.html'), pptx);

    // Slide 2
    console.log('Processing Slide 2...');
    await html2pptx(path.join(__dirname, 'slides/slide2.html'), pptx);

    // Slide 3
    console.log('Processing Slide 3...');
    const { slide: slide3, placeholders: ph3 } = await html2pptx(path.join(__dirname, 'slides/slide3.html'), pptx);

    // Add Chart to Slide 3
    if (ph3 && ph3.length > 0) {
        // Find specific placeholder by ID if possible, or just take first
        const ecoPh = ph3.find(p => p.id === 'eco-chart') || ph3[0];

        if (ecoPh) {
            slide3.addChart(pptx.charts.DOUGHNUT, [
                {
                    name: "Energy Mix",
                    labels: ["Solar", "Hydro", "Grid"],
                    values: [60, 30, 10]
                }
            ], {
                x: ecoPh.x, y: ecoPh.y, w: ecoPh.w, h: ecoPh.h,
                showLegend: true, legendPos: 'r',
                showTitle: false,
                chartColors: ["F1C40F", "3498DB", "95A5A6"],
                holeSize: 60
            });
        }
    }

    // Slide 4
    console.log('Processing Slide 4...');
    await html2pptx(path.join(__dirname, 'slides/slide4.html'), pptx);

    // Slide 5
    console.log('Processing Slide 5...');
    await html2pptx(path.join(__dirname, 'slides/slide5.html'), pptx);

    // Save
    const outputPath = path.join(__dirname, 'Presentation_Eco_Nomad.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Presentation created successfully at ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});
