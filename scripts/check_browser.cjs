'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = (process.env.SITE_URL || 'http://127.0.0.1:8000/').replace(/\/?$/, '/');
const pages = ['index.html', 'creative-lab.html', 'performing-systems.html', 'reliable-systems.html', 'contact.html'];
const output = process.env.PREVIEW_DIR;

(async () => {
  const browser = await chromium.launch({
    ...(process.env.BROWSER_PATH ? { executablePath: process.env.BROWSER_PATH } : {}),
    args: ['--no-sandbox'],
  });
  const errors = [];
  let checks = 0;
  try {
    for (const width of [320, 390, 768, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: width < 700 ? 844 : 1000 } });
      const page = await context.newPage();
      page.on('pageerror', e => errors.push(e.message));
      page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
      page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
      for (const file of pages) {
        assert.equal((await page.goto(base + file)).status(), 200);
        assert.equal(await page.locator('h1').count(), 1);
        assert.equal(await page.locator('nav [aria-current=page]').getAttribute('href'), file);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width}px overflow on ${file}`);
        assert(await page.locator('h1').evaluate(el => el.scrollWidth <= el.clientWidth + 1), `${width}px clipped h1 on ${file}`);
        assert(await page.locator('img').evaluateAll(async images => {
          await Promise.all(images.map(img => { img.loading = 'eager'; return img.decode().catch(() => {}); }));
          return images.every(img => img.naturalWidth > 0);
        }), `Broken logo on ${file}`);
        assert.equal(await page.locator('img[src*="visual-"]').count(), 0);
        assert.equal(await page.locator('a[href^="tel:"]').count(), 1);
        assert.equal(await page.locator('a[href^="mailto:"]').count(), 1);
        assert(await page.locator('a[href^="tel:"], a[href^="mailto:"]').evaluateAll(links=>links.every(el=>el.closest('.contact-band'))));
        assert.equal(await page.locator('a[href^="mailto:"]').getAttribute('href'), 'mailto:anthony@playback-solutions.com');
        assert.equal(await page.locator('.brand img').getAttribute('src'), 'assets/logo_playback_WHITE_HORIZONTAL.png');
        assert.equal(await page.locator('[lang="en"]').count(), 0);
        // All page canvases, placeholders and the drawer must remain dark.
        assert(await page.locator('body, .menu-panel, .presentation, .contact-band, .references-section, .media.awaiting-photo').evaluateAll(elements=>elements.every(el=>{
          const rgb=getComputedStyle(el).backgroundColor.match(/[0-9.]+/g).slice(0,3).map(Number);
          return rgb.every(channel=>channel<=40);
        })), `Light surface on ${file}`);
        // Check contrast of actual body/headings and placeholder text on their solid backgrounds.
        assert(await page.locator('body, .placeholder-subject, .placeholder-label').evaluateAll(elements=>{
          const rgb=value=>value.match(/[0-9.]+/g).slice(0,3).map(Number);
          const luminance=color=>rgb(color).map(c=>{c/=255;return c<=.04045?c/12.92:((c+.055)/1.055)**2.4}).reduce((sum,c,i)=>sum+c*[.2126,.7152,.0722][i],0);
          return elements.every(el=>{
            let parent=el;
            while(parent && getComputedStyle(parent).backgroundColor==='rgba(0, 0, 0, 0)')parent=parent.parentElement;
            if(!parent)return false;
            const a=luminance(getComputedStyle(el).color),b=luminance(getComputedStyle(parent).backgroundColor);
            return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)>=4.5;
          });
        }), `Insufficient contrast on ${file}`);
        await page.locator('.menu-toggle').click();
        await page.locator('.menu-panel').waitFor({state:'visible'});
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'true');
        assert.equal(await page.locator('.menu-panel').getAttribute('aria-modal'), 'true');
        assert(await page.locator('main').evaluate(el => el.inert));
        const first = page.locator('.menu-panel a').first();
        const last = page.locator('.menu-panel nav a').last();
        await last.focus(); await page.keyboard.press('Tab');
        assert(await first.evaluate(el => el === document.activeElement));
        await page.keyboard.press('Shift+Tab');
        assert(await last.evaluate(el => el === document.activeElement));
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
        assert(await page.locator('.menu-toggle').evaluate(el => el === document.activeElement));
        assert(await page.locator('.menu-panel').evaluate(el => el.inert));
        assert(!(await page.locator('main').evaluate(el => el.inert)));
        await page.locator('.menu-toggle').click();
        await page.locator('.menu-close').click();
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
        await page.locator('.menu-toggle').click();
        const next = pages[(pages.indexOf(file)+1)%pages.length];
        await page.locator(`.menu-panel nav a[href="${next}"]`).click();
        assert(page.url().endsWith('/'+next));
        checks++;
      }
      await page.goto(base);
      const featured = page.locator('.reference-card h3');
      assert.deepEqual(await featured.allTextContents(), ['Justice','Polo & Pan','Mylène Farmer','Eddy de Pretto','Kungs','Damso','Jeux olympiques de Paris 2024']);
      assert.equal(await page.locator('.reference-card .media').count(), 7);
      assert.equal(await page.locator('.skills-strip li').count(), 6);
      assert.equal(await page.locator('.skills-strip svg').count(), 6);
      const strip = await page.locator('.skills-strip').boundingBox();
      assert(strip.height < (width <= 600 ? 380 : 160), `Capabilities strip too tall at ${width}px`);
      const details = page.locator('.reference-collection');
      const summary = details.locator('summary');
      assert(!(await details.evaluate(el=>el.open)));
      assert.equal(await page.locator('.collection-card:visible').count(), 0);
      await summary.focus();
      await page.keyboard.press('Enter');
      assert(await details.evaluate(el=>el.open));
      assert.equal(await page.locator('.collection-card:visible').count(), 34);
      assert.equal(await page.locator('.collection-card').evaluateAll(cards=>cards.flatMap(card=>card.dataset.projectSlugs.split(' ')).length), 39);
      assert((await page.locator('[data-project-slugs~="mylene-farmer-nevermore"]').textContent()).includes('2019 · Nevermore'));
      assert((await page.locator('[data-project-slugs~="jarre-al-ula"]').textContent()).includes('Al Ula · The Green Concert'));
      assert(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth+1), `Collection overflow at ${width}px`);
      assert((await page.locator('[data-project-slugs~="mc-solaar-2022"]').textContent()).includes('2022 · 2023'));
      assert((await page.locator('[data-project-slugs~="mylene-farmer-nevermore"]').textContent()).includes('2019 · Nevermore · Mylène le retour'));
      assert((await page.locator('[data-project-slugs~="claire-laffut-2021"]').textContent()).includes('Claire Laffut'));
      assert.equal(await page.locator('[data-project-slugs~="mc-2023"]').count(), 0);
      await summary.click();
      assert(!(await details.evaluate(el=>el.open)));
      await page.locator('.references-section').scrollIntoViewIfNeeded();
      assert(await featured.first().isVisible());
      const next = page.locator('.slide-next');
      await next.click();
      assert.equal(await page.locator('.slide-counter').textContent(), '02 / 03');
      assert.equal(await page.locator('.carousel-slide:visible').count(), 1);
      assert(await page.locator('#slide-2').isVisible());
      await page.keyboard.press('ArrowRight');
      assert(await page.locator('#slide-3').isVisible());
      await page.keyboard.press('ArrowRight');
      assert(await page.locator('#slide-1').isVisible());
      await page.locator('.slide-prev').click();
      assert(await page.locator('#slide-3').isVisible());
      await page.keyboard.press('ArrowLeft');
      assert(await page.locator('#slide-2').isVisible());
      await page.locator('.menu-toggle').click();
      await page.locator('.menu-backdrop').click({position:{x:width-5,y:500}});
      assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
      await page.emulateMedia({reducedMotion:'reduce'});
      assert.equal(await page.locator('#slide-2').evaluate(el=>getComputedStyle(el).animationName), 'none');
      if (output && [390,1440].includes(width)) {
        fs.mkdirSync(output, {recursive:true});
        for (const file of pages) {
          await page.goto(base+file);
          await page.screenshot({path:`${output}/${file.replace('.html','')}-${width}.png`,fullPage:true});
        }
        await page.goto(base);
        await page.locator('.reference-collection summary').click();
        await page.evaluate(()=>scrollTo(0,0));
        await page.screenshot({path:`${output}/references-${width}.png`,fullPage:true});
        await page.goto(base);
        await page.locator('.menu-toggle').click();
        await page.screenshot({path:`${output}/menu-${width}.png`});
      }
      await context.close();
    }
    const noJS = await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const p = await noJS.newPage();
    for(const file of pages) {
      await p.goto(base+file);
      assert(await p.locator('nav a').first().isVisible());
      assert(await p.locator('h1').isVisible());
      if(file==='index.html') { await p.locator('.reference-collection summary').click(); assert.equal(await p.locator('.collection-card:visible').count(),34); }
      assert(await p.evaluate(()=>document.documentElement.scrollWidth <= innerWidth+1),`No-JS overflow on ${file}`);
    }
    await noJS.close();
    assert.deepEqual(errors,[]);
    console.log(`PASS: ${checks} page/viewport checks; all navigation destinations; drawer keyboard/focus/backdrop/close; carousel navigation/wrap/keyboard; logos; dark surfaces/contrast; contact-only phone/email; 6 compact pictograms; 7 featured references; 39 approved entries/34 native expandable groups; no-JS fallback; reduced motion; no JavaScript or HTTP errors. Base: ${base}`);
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1});
