const sharp = require('sharp');
const pngToIco = require('png-to-ico');
const fs = require('fs');

const inputImage = 'public/images/logo.png';
const outputDir = 'public';

async function generate() {
  console.log('Generating favicon sizes...');

  const sizes = [
    { name: 'favicon-16x16.png', size: 16 },
    { name: 'favicon-32x32.png', size: 32 },
    { name: 'apple-touch-icon.png', size: 180 },
    { name: 'android-chrome-192x192.png', size: 192 },
    { name: 'android-chrome-512x512.png', size: 512 }
  ];

  for (const item of sizes) {
    await sharp(inputImage)
      .resize(item.size, item.size, {
        fit: 'contain',
        background: { r: 255, g: 255, b: 255, alpha: 0 }
      })
      .toFile(`${outputDir}/${item.name}`);
    console.log(`Generated ${item.name}`);
  }

  // Generate ICO from 32x32
  console.log('Generating favicon.ico...');
  const buf = await pngToIco(`${outputDir}/favicon-32x32.png`);
  fs.writeFileSync(`${outputDir}/favicon.ico`, buf);
  console.log('Generated favicon.ico');
}

generate().catch(err => {
  console.error(err);
  process.exit(1);
});
