import { readdir, cp, mkdir } from 'fs/promises';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const publicDir = join(__dirname, 'public');
const distDir = join(__dirname, 'dist');

async function copyPublicAssets() {
  try {
    // Check if public directory exists
    if (!existsSync(publicDir)) {
      console.log('No public directory found, skipping copy');
      return;
    }

    // Check if dist directory exists
    if (!existsSync(distDir)) {
      console.error('Dist directory not found! Build may have failed.');
      process.exit(1);
    }

    // Get all items in public directory
    const items = await readdir(publicDir, { withFileTypes: true });

    // Copy each item
    for (const item of items) {
      const srcPath = join(publicDir, item.name);
      const destPath = join(distDir, item.name);

      await cp(srcPath, destPath, {
        recursive: true,
        force: true,
      });

      console.log(`  ✓ Copied ${item.name}`);
    }

    console.log('✓ Public assets copied to dist/');
  } catch (error) {
    console.error('Error copying public assets:', error);
    process.exit(1);
  }
}

copyPublicAssets();
