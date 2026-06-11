import fs from 'fs';
const content = fs.readFileSync('scratch/vobiz-sdk.cjs', 'utf8');

function findSurroundings(pattern, label) {
  let idx = 0;
  console.log(`=== Matches for ${label} (${pattern}) ===`);
  while ((idx = content.indexOf(pattern, idx)) !== -1) {
    const start = Math.max(0, idx - 100);
    const end = Math.min(content.length, idx + pattern.length + 150);
    console.log(`Index ${idx}: ...${content.substring(start, end).replace(/\r?\n/g, ' ')}...`);
    idx += pattern.length;
  }
}

findSurroundings('appId', 'appId');
findSurroundings('appSecret', 'appSecret');
