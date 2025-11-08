import { cp } from 'fs/promises';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const publicDir = join(__dirname, 'public');
const distDir = join(__dirname, 'dist');

try {
  await cp(publicDir, distDir, {
    recursive: true,
    force: true,
    filter: (src) => {
      // Copy everything
      return true;
    }
  });
  console.log('✓ Public assets copied to dist/');
} catch (error) {
  console.error('Error copying public assets:', error);
  process.exit(1);
}
