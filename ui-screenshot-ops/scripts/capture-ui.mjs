#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

const url = arg('--url');
const project = arg('--project', 'default');
const selector = arg('--selector', 'body');
const label = arg('--label', 'capture');
const outRoot = arg('--out', '/tmp/ui-captures');
const waitMs = Number(arg('--wait-ms', '1200'));
const viewportW = Number(arg('--width', '1440'));
const viewportH = Number(arg('--height', '900'));

if (!url) {
  console.error('Usage: capture-ui.mjs --url <url> [--project name] [--selector css] [--label before|after]');
  process.exit(1);
}

const date = new Date().toISOString().slice(0, 10);
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const dir = path.join(outRoot, project, date);
fs.mkdirSync(dir, { recursive: true });

const fullPath = path.join(dir, `${label}-full-${stamp}.png`);
const compPath = path.join(dir, `${label}-component-${stamp}.png`);

let chromium;
try {
  ({ chromium } = await import('playwright'));
} catch {
  try {
    ({ chromium } = await import('/tmp/openclaw-repo/frontend/node_modules/playwright/index.mjs'));
  } catch {
    console.error('Missing playwright. Install with: npm i -D playwright (or run from a repo with playwright).');
    process.exit(2);
  }
}

const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome' });
const page = await browser.newPage({ viewport: { width: viewportW, height: viewportH } });
try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  if (waitMs > 0) await page.waitForTimeout(waitMs);
  await page.screenshot({ path: fullPath, fullPage: true });

  const locator = page.locator(selector).first();
  await locator.waitFor({ timeout: 10000 });
  await locator.screenshot({ path: compPath });

  console.log(JSON.stringify({ ok: true, full: fullPath, component: compPath, selector, url }, null, 2));
} finally {
  await browser.close();
}
