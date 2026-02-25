const pptxgen = require('pptxgenjs');
const html2pptx = require('../.agent/skills/pptx/scripts/html2pptx');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Green Canyon Eco Village';
    pptx.title = 'High Yield Investment Presentation';

    // Slide 1
    console.log('Processing Slide 1...');
    await html2pptx(path.join(__dirname, 'slides/slide1.html'), pptx);

    // Slide 2
    console.log('Processing Slide 2...');
    const { slide: slide2, placeholders: ph2 } = await html2pptx(path.join(__dirname, 'slides/slide2.html'), pptx);

    // Add Chart to Slide 2
    if (ph2 && ph2.length > 0) {
        slide2.addChart(pptx.charts.BAR, [
            {
                name: "Yield Comparison",
                labels: ["Batumi", "Edge Village (Target)"],
                values: [10, 12]
            }
        ], {
            x: ph2[0].x, y: ph2[0].y, w: ph2[0].w, h: ph2[0].h,
            showLegend: false,
            showTitle: true, title: "Annual Yield (%)",
            chartColors: ["BDC3C7", "27AE60"],
            valAxisMinVal: 0, valAxisMaxVal: 20,
            barDir: 'col'
        });
    }

    // Slide 3
    console.log('Processing Slide 3...');
    await html2pptx(path.join(__dirname, 'slides/slide3.html'), pptx);

    // Slide 4
    console.log('Processing Slide 4...');
    await html2pptx(path.join(__dirname, 'slides/slide4.html'), pptx);

    // Slide 5
    console.log('Processing Slide 5...');
    const { slide: slide5, placeholders: ph5 } = await html2pptx(path.join(__dirname, 'slides/slide5.html'), pptx);

    // Add Chart to Slide 5
    if (ph5 && ph5.length > 0) {
        slide5.addChart(pptx.charts.LINE, [
            {
                name: "Projected Value",
                labels: ["Year 0", "Year 1", "Year 2"],
                values: [100, 115, 130] // +30% over 2 years
            }
        ], {
            x: ph5[0].x, y: ph5[0].y, w: ph5[0].w, h: ph5[0].h,
            showTitle: true, title: "Asset Value Growth Index",
            chartColors: ["F1C40F"],
            lineSmooth: true,
            lineSize: 4,
            lineDataSymbol: 'circle',
            showLegend: false
        });
    }

    // Save
    const outputPath = path.join(__dirname, 'Presentation_High_Yield.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`Presentation created successfully at ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error creating presentation:', err);
    process.exit(1);
});
