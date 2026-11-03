'use strict';
// Optional browser validation. Playwright is a development tool, not a site dependency.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = (process.env.SITE_URL || 'http://127.0.0.1:8000/').replace(/\/?$/, '/');
const output = process.env.PREVIEW_DIR;
const pages = ['index.html', 'creative-lab.html', 'performing-systems.html', 'reliable-systems.html', 'projets.html', 'a-propos.html', 'contact.html'];

(async () => {
  const browser = await chromium.launch({
    ...(process.env.BROWSER_PATH ? { executablePath: process.env.BROWSER_PATH } : {}),
    args: ['--no-sandbox'],
  });
  const errors = [];
  let checks = 0;
  try {
    for (const width of [320, 390, 768, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: width < 700 ? 844 : 1000 }, reducedMotion: 'reduce' });
      const page = await context.newPage();
      page.on('pageerror', e => errors.push(e.message));
      page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
      page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
      for (const file of pages) {
        const response = await page.goto(base + file);
        assert.equal(response.status(), 200);
        await page.locator('h1').waitFor();
        assert.equal(await page.locator('h1').count(), 1);
        assert.equal(await page.locator('.navigation [aria-current=page]').getAttribute('href'), file);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width}px overflow on ${file}`);
        // Detect clipped large headings even where a hero has overflow:hidden.
        assert(await page.locator('h1').evaluate(el => el.scrollWidth <= el.clientWidth + 1), `${width}px clipped heading on ${file}`);
        const images = await page.locator('img').evaluateAll(async imgs => {
          await Promise.all(imgs.map(img => { img.loading = 'eager'; return img.decode().catch(() => {}); }));
          return imgs.every(img => img.complete && img.naturalWidth > 0);
        });
        assert(images, `Broken image on ${file}`);
        // Every navigation destination is visited via an actual link.
        if (width <= 1100) {
          await page.locator('.menu-toggle').click();
          assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'true');
          await page.keyboard.press('Escape');
          assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
          assert(await page.locator('.menu-toggle').evaluate(el => el === document.activeElement));
          await page.locator('.menu-toggle').click();
        }
        const next = pages[(pages.indexOf(file) + 1) % pages.length];
        await page.locator(`.navigation a[href="${next}"]`).click();
        assert(page.url().endsWith('/' + next));
        checks++;
      }
      await page.goto(base + 'projets.html');
      const search = page.locator('#project-query');
      await search.fill('mylene');
      assert.equal(await page.locator('[data-project]:visible').count(), 3);
      await search.fill('2024 justice');
      assert.equal(await page.locator('[data-project]:visible').count(), 1);
      await search.fill('aucun-resultat-xyz');
      assert(await page.locator('#project-empty').isVisible());
      await search.fill('');
      assert.equal(await page.locator('[data-project]:visible').count(), 40);
      if (width <= 1100) {
        await page.locator('.menu-toggle').click();
        const lastLink = page.locator('.navigation a').last();
        await lastLink.focus(); await page.keyboard.press('Tab');
        assert(await page.locator('.menu-toggle').evaluate(el => el === document.activeElement));
        await page.keyboard.press('Shift+Tab');
        assert(await lastLink.evaluate(el => el === document.activeElement));
        await page.keyboard.press('Escape');
      }
      if (output && [390, 1440].includes(width)) {
        fs.mkdirSync(output, { recursive: true });
        for (const file of ['index.html', 'creative-lab.html', 'projets.html', 'contact.html']) {
          await page.goto(base + file);
          const stem = file === 'index.html' ? 'accueil' : file.replace('.html', '');
          await page.screenshot({ path: `${output}/${stem}-${width === 390 ? 'mobile' : 'desktop'}.png`, fullPage: true });
        }
      }
      await context.close();
    }
    const noJS = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
    const fallback = await noJS.newPage();
    for (const file of pages) {
      await fallback.goto(base + file);
      assert(await fallback.locator('.navigation a').first().isVisible());
      assert(await fallback.locator('h1').isVisible());
      assert(await fallback.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    }
    await noJS.close();
    // Exercise actual scroll reveals with motion enabled, then reduced-motion switching.
    const animated = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const p = await animated.newPage();
    p.on('pageerror', e => errors.push(e.message));
    await p.goto(base);
    for (const element of await p.locator('[data-reveal]').all()) {
      await element.scrollIntoViewIfNeeded();
      await element.waitFor({ state: 'visible' });
      await p.waitForFunction(el => el.classList.contains('is-visible'), await element.elementHandle());
    }
    await p.emulateMedia({ reducedMotion: 'reduce' });
    assert.equal(await p.locator('.will-reveal:not(.is-visible)').count(), 0);
    await animated.close();
    assert.deepEqual(errors, [], 'Browser errors or failed resources');
    console.log(`PASS: ${checks} page/viewport checks; navigation, images, headings, search, keyboard menu, no-JS fallback and motion preferences; no browser errors. Base: ${base}`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
