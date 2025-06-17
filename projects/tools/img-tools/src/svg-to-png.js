const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// ---- CONFIG ----
const inputSvgPath = path.resolve(__dirname, '../svg/git-merge.svg'); // Change this if needed
const fillColor = '#0366D6'; // GitHub Blue

// ---- Derive output path from input ----
const inputFileName = path.basename(inputSvgPath, '.svg'); // e.g. "git-merge"
const outputDir = path.resolve(__dirname, '../png');
const outputFilePath = path.join(outputDir, `${inputFileName}.png`);

// ---- Ensure Output Directory Exists ----
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// ---- Read and Process SVG ----
fs.readFile(inputSvgPath, 'utf8', (err, data) => {
  if (err) {
    console.error('❌ Error reading SVG file:', err);
    return;
  }

  const coloredSvg = injectFillColor(data, fillColor);

  sharp(Buffer.from(coloredSvg))
    .resize(128, 128) // Optional: set desired icon size
    .png({ quality: 100 })
    .toFile(outputFilePath)
    .then(() => {
      console.log(`✅ PNG saved at ${outputFilePath} with fill color ${fillColor}`);
    })
    .catch((error) => {
      console.error('❌ Error converting to PNG:', error);
    });
});

// ---- Helper Function to Inject Fill Color ----
function injectFillColor(svgContent, fillColor) {
  // Add fill to <svg> tag if not already present
  let updated = svgContent.replace(
    /<svg([^>]*)(?<!fill="[^"]*")>/,
    `<svg$1 fill="${fillColor}">`
  );

  // Replace all existing fill values
  updated = updated.replace(/fill="[^"]*"/g, `fill="${fillColor}"`);

  return updated;
}
