#!/usr/bin/env python3
"""Browser regression checks for the 240-page themed product site.

The script is intentionally local-only. Keep reports and optional screenshots
outside the repository, and checkpoint the JSON report after every page.
"""

import argparse
import asyncio
import json
import re
import signal
from pathlib import Path
from urllib.parse import urlsplit

from playwright.async_api import async_playwright

from generate import ASTRO_ROUTES, LOCALES, OLD_ROUTES, path


WIDTHS = (320, 360, 375, 390, 414, 768, 1024, 1440)
LANDSCAPE = (844, 390)
CTA_HREFS = (
    "https://t.me/taroshenka_bot?start=ref974025936",
    "https://t.me/astrology_1_bot?start=ref974025936",
    "https://app.taro.mom/?ref=974025936",
)
THEME_STYLESHEET = "/sitegen/assets/product-themes.css"
EXTERNAL_HTTP = re.compile(r"^(?!http://127[.]0[.]0[.]1:8765(?:/|$))https?://")


def selected_routes(args):
    locale_codes = [part.strip() for part in args.locales.split(",")] if args.locales else [x["code"] for x in LOCALES]
    page_keys = [part.strip() for part in args.pages.split(",")] if args.pages else [*OLD_ROUTES, *ASTRO_ROUTES]
    known_locales = {x["code"] for x in LOCALES}
    known_pages = set((*OLD_ROUTES, *ASTRO_ROUTES))
    if not locale_codes or any(code not in known_locales for code in locale_codes):
        raise ValueError("--locales contains an unknown or empty locale")
    if not page_keys or any(key not in known_pages for key in page_keys):
        raise ValueError("--pages contains an unknown or empty page key")
    if len(set(locale_codes)) != len(locale_codes) or len(set(page_keys)) != len(page_keys):
        raise ValueError("--locales and --pages must not contain duplicates")
    return locale_codes, page_keys, [
        (code, key, path(code, key)) for code in locale_codes for key in page_keys
    ]


def checked_base(value):
    parsed = urlsplit(value)
    if parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or parsed.port != 8765:
        raise argparse.ArgumentTypeError("--base must use http://127.0.0.1:8765")
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise argparse.ArgumentTypeError("--base must be exactly http://127.0.0.1:8765")
    return "http://127.0.0.1:8765"


async def main(args):
    locale_codes, page_keys, routes = selected_routes(args)
    output = Path(args.output).resolve()
    repo_root = Path(__file__).resolve().parents[1]
    if output == repo_root or repo_root in output.parents:
        raise ValueError("--output must be outside the repository")
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / "theme-browser-report.json"
    report = {
        "ok": False,
        "base": args.base,
        "requested_locales": locale_codes,
        "requested_pages": page_keys,
        "pages_requested": len(routes),
        "pages_completed": 0,
        "responsive_checks": [],
        "no_javascript_pages": [],
        "image_results": {},
        "console_errors": [],
        "page_errors": [],
        "http_errors": [],
        "blocked_external_requests": [],
        "failures": [],
    }

    def checkpoint():
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    stop_after_page = False

    def request_stop(_signum, _frame):
        nonlocal stop_after_page
        stop_after_page = True

    previous_handlers = {}
    for signum in (signal.SIGINT, signal.SIGTERM):
        previous_handlers[signum] = signal.signal(signum, request_stop)

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            context = await browser.new_context(
                viewport={"width": 390, "height": 900},
                reduced_motion="reduce",
                device_scale_factor=1,
            )

            async def local_only(route):
                parsed = urlsplit(route.request.url)
                if parsed.scheme in ("data", "blob", "about"):
                    await route.continue_()
                elif parsed.scheme == "http" and parsed.hostname == "127.0.0.1" and parsed.port == 8765:
                    await route.continue_()
                else:
                    report["blocked_external_requests"].append(route.request.url)
                    await route.abort("blockedbyclient")

            await context.route(EXTERNAL_HTTP, local_only)
            page = await context.new_page()
            page.on("pageerror", lambda error: report["page_errors"].append(str(error)))
            page.on(
                "console",
                lambda message: report["console_errors"].append(message.text)
                if message.type == "error"
                else None,
            )
            page.on(
                "response",
                lambda response: report["http_errors"].append(
                    {"url": response.url, "status": response.status}
                )
                if response.status >= 400
                else None,
            )

            async def assert_no_horizontal_escape(label):
                result = await page.evaluate(
                    """() => {
                      const excluded = el => !!el.closest('.theme-art');
                      const visible = el => el.checkVisibility({checkOpacity:false,checkVisibilityCSS:true});
                      const bad = [];
                      const controls = 'a,button,input,select,textarea,summary,[tabindex],label';
                      for (const el of document.querySelectorAll(controls)) {
                        if (excluded(el) || !visible(el)) continue;
                        const rect = el.getBoundingClientRect();
                        if (!rect.width || !rect.height) continue;
                        if (rect.left < -1 || rect.right > innerWidth + 1) {
                          bad.push({tag:el.tagName, className:typeof el.className==='string'?el.className:'',
                            text:(el.innerText||'').trim().slice(0,100), left:Math.round(rect.left), right:Math.round(rect.right)});
                        }
                      }
                      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                      let node;
                      while ((node = walker.nextNode())) {
                        const text = node.nodeValue.trim(), parent = node.parentElement;
                        if (!text || !parent || excluded(parent) || !visible(parent)) continue;
                        const range = document.createRange(); range.selectNodeContents(node);
                        for (const line of range.getClientRects()) {
                          if (line.width && (line.left < -1 || line.right > innerWidth + 1)) {
                            bad.push({tag:parent.tagName, className:typeof parent.className==='string'?parent.className:'',
                              text:text.slice(0,100), left:Math.round(line.left), right:Math.round(line.right)});
                            break;
                          }
                        }
                      }
                      return {documentWidth:document.documentElement.scrollWidth, viewportWidth:innerWidth, bad};
                    }"""
                )
                assert result["documentWidth"] <= result["viewportWidth"] + 1 and not result["bad"], (label, result)

            async def check_theme_contract(code, key, route):
                body = page.locator("body")
                assert await body.evaluate("e=>e.classList.contains('theme-product')"), route + " missing body.theme-product"
                assert await page.locator(f'link[rel="stylesheet"][href="{THEME_STYLESHEET}"]').count() == 1, route + " theme stylesheet"
                art = page.locator(".theme-art img")
                if key == "home":
                    assert await page.locator(".hero-art").count() == 1, route + " home hero art"
                    assert await art.count() == 0, route + " unexpected theme art on home"
                else:
                    assert await art.count() == 1, route + " expected one theme-art image"
                    assert await art.get_attribute("alt") == "", route + " theme art must be decorative"
                if key in ("home", "astro"):
                    expected = 10 if key == "home" else 6
                    assert await page.locator(".topic-preview").count() == expected, (route, "topic preview count")
                if key == "horoscopes":
                    assert await page.locator("article.horoscope-format").count() == 3, route + " horoscope cards"

                links = page.locator(".entry-link")
                hrefs = await links.evaluate_all("els=>els.map(e=>e.getAttribute('href'))")
                assert hrefs == [*CTA_HREFS, *CTA_HREFS], (route, "CTA contract changed", hrefs)

            async def check_images(route):
                images = page.locator("img")
                await images.evaluate_all("els=>els.forEach(img=>img.loading='eager')")
                await page.wait_for_function(
                    "Array.from(document.images).every(img=>img.complete&&img.naturalWidth>0)",
                    timeout=30000,
                )
                results = await images.evaluate_all(
                    "els=>els.map(img=>({src:img.getAttribute('src'),loaded:img.complete&&img.naturalWidth>0}))"
                )
                assert all(result["loaded"] for result in results), (route, "image did not load", results)
                await images.evaluate_all("els=>Promise.all(els.map(img=>img.decode()))")
                report["image_results"][route] = results

            async def check_keyboard_and_equal_ctas(route):
                await page.set_viewport_size({"width": 390, "height": 900})
                await page.evaluate("window.scrollTo(0,0)")
                for group in (page.locator(".hero .entry-link"), page.locator(".final-cta .entry-link")):
                    assert await group.count() == 3, (route, "CTA group count")
                    boxes = await group.evaluate_all(
                        "els=>els.map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {width:r.width,background:s.backgroundColor+' '+s.backgroundImage,color:s.color,border:s.borderColor+' '+s.borderWidth+' '+s.borderStyle,radius:s.borderRadius}})"
                    )
                    assert all(
                        abs(box["width"] - boxes[0]["width"]) <= 1
                        and all(box[key] == boxes[0][key] for key in ("background", "color", "border", "radius"))
                        for box in boxes[1:]
                    ), (route, "CTA dimensions differ", boxes)
                    await group.first.focus()
                    assert await group.first.evaluate(
                        "e=>getComputedStyle(e).outlineStyle!=='none' || getComputedStyle(e).boxShadow!=='none'"
                    ), (route, "CTA keyboard focus is not visible")
                    await page.evaluate("document.activeElement.blur()")

            for code, key, route in routes:
                item = {"locale": code, "page": key, "route": route, "status": "running", "checks": []}
                report.setdefault("page_results", []).append(item)
                try:
                    response = await page.goto(args.base + route, wait_until="domcontentloaded", timeout=60000)
                    assert response and response.status == 200, (route, "HTTP status", response.status if response else None)
                    await page.wait_for_function(
                        "href=>{const link=document.querySelector(`link[rel=stylesheet][href=\"${href}\"]`);return !!(link&&link.sheet)}",
                        arg=THEME_STYLESHEET,
                        timeout=60000,
                    )
                    await page.evaluate("document.fonts.ready")
                    await page.evaluate("new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
                    assert await page.locator("h1").count() == 1, route + " h1 count"
                    await check_theme_contract(code, key, route)
                    item["checks"].append("theme contract and CTA hrefs")

                    await page.keyboard.press("Tab")
                    assert await page.evaluate("document.activeElement.classList.contains('skip-link')"), route + " skip link initial focus"
                    await page.keyboard.press("Enter")
                    assert await page.evaluate("document.activeElement.id === 'main-content'"), route + " skip link target"
                    await page.evaluate("document.activeElement.blur();window.scrollTo(0,0)")

                    await page.evaluate("document.documentElement.style.zoom='';document.documentElement.style.fontSize=''")
                    for width in WIDTHS:
                        await page.set_viewport_size({"width": width, "height": 900})
                        await assert_no_horizontal_escape(route + f" width={width}")
                        report["responsive_checks"].append({"route": route, "width": width, "mode": "portrait"})
                    item["checks"].append({"widths": list(WIDTHS), "mode": "portrait"})

                    await page.set_viewport_size({"width": LANDSCAPE[0], "height": LANDSCAPE[1]})
                    await assert_no_horizontal_escape(route + " landscape")
                    report["responsive_checks"].append({"route": route, "width": LANDSCAPE[0], "height": LANDSCAPE[1], "mode": "landscape"})
                    item["checks"].append({"landscape": list(LANDSCAPE)})

                    await page.set_viewport_size({"width": 768, "height": 900})
                    await page.evaluate("document.documentElement.style.zoom='2'")
                    await assert_no_horizontal_escape(route + " zoom 200%")
                    await page.evaluate("document.documentElement.style.zoom=''")
                    report["responsive_checks"].append({"route": route, "width": 768, "mode": "zoom-200"})
                    item["checks"].append("200% zoom")

                    await page.set_viewport_size({"width": 390, "height": 900})
                    await page.evaluate("document.documentElement.style.fontSize='125%'")
                    await assert_no_horizontal_escape(route + " text 125%")
                    await page.evaluate("document.documentElement.style.fontSize=''")
                    report["responsive_checks"].append({"route": route, "width": 390, "mode": "text-125"})
                    item["checks"].append("125% root text size")

                    await check_images(route)
                    item["checks"].append("all images decoded")

                    # A small cross-section exercises focus and equal CTA layouts
                    # while avoiding the cost of repeating interaction at every width.
                    if code in ("en", "ru", "ar") and key in ("home", "astro", "natal", "horoscopes"):
                        await check_keyboard_and_equal_ctas(route)
                        item["checks"].append("keyboard focus and equal CTA dimensions")

                    if args.screenshots:
                        for width in (390, 1440):
                            await page.set_viewport_size({"width": width, "height": 1000})
                            await page.evaluate("window.scrollTo(0,0)")
                            await page.screenshot(path=str(output / f"{code}-{key}-{width}.png"), full_page=False)
                            if width == 1440 and key in ("home", "astro"):
                                await page.locator(".topic-grid").nth(0).screenshot(
                                    path=str(output / f"{code}-{key}-topic-grid-first-1440.png")
                                )
                            if key == "horoscopes":
                                await page.locator(".horoscope-formats").screenshot(
                                    path=str(output / f"{code}-{key}-cards-{width}.png")
                                )
                        item["checks"].append("390px and 1440px first-screen screenshots")

                    item["status"] = "passed"
                    report["pages_completed"] += 1
                except Exception as error:
                    item["status"] = "failed"
                    item["error"] = str(error)
                    report["failures"].append({"route": route, "error": str(error)})
                finally:
                    checkpoint()
                if item["status"] == "failed" or stop_after_page:
                    break

            # Check one no-JavaScript page per requested locale. The native
            # details/summary language menu and all essential copy must work.
            if not report["failures"] and not stop_after_page:
                nojs_context = await browser.new_context(
                    java_script_enabled=False,
                    viewport={"width": 390, "height": 900},
                    device_scale_factor=1,
                )
                await nojs_context.route(EXTERNAL_HTTP, local_only)
                nojs_page = await nojs_context.new_page()
                for code in locale_codes:
                    key = page_keys[0]
                    route = path(code, key)
                    response = await nojs_page.goto(args.base + route, wait_until="domcontentloaded", timeout=60000)
                    assert response and response.status == 200, (route, "no-JS HTTP status")
                    await nojs_page.wait_for_function(
                        "href=>{const link=document.querySelector(`link[rel=stylesheet][href=\"${href}\"]`);return !!(link&&link.sheet)}",
                        arg=THEME_STYLESHEET,
                        timeout=60000,
                    )
                    assert await nojs_page.locator("body.theme-product").count() == 1, route + " no-JS theme"
                    assert await nojs_page.locator("h1").inner_text()
                    assert await nojs_page.locator(".entry-link").count() == 6
                    summary = nojs_page.locator(".locale-switch summary")
                    await summary.click()
                    assert await nojs_page.locator(".locale-menu a").count() == 20
                    assert await nojs_page.locator(".locale-menu").is_visible()
                    report["no_javascript_pages"].append(route)
                    checkpoint()
                await nojs_context.close()

            report["ok"] = (
                not report["failures"]
                and not report["console_errors"]
                and not report["page_errors"]
                and not report["http_errors"]
                and not report["blocked_external_requests"]
                and not stop_after_page
                and report["pages_completed"] == len(routes)
                and len(report["no_javascript_pages"]) == len(locale_codes)
            )
            if report["console_errors"] or report["page_errors"] or report["http_errors"]:
                report["failures"].append({"error": "browser console, page, or HTTP errors were recorded"})
            await context.close()
            await browser.close()
    except Exception as error:
        report["failures"].append({"error": str(error)})
    finally:
        checkpoint()
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)

    summary = {
        "ok": report["ok"],
        "pages_completed": report["pages_completed"],
        "pages_requested": report["pages_requested"],
        "responsive_checks": len(report["responsive_checks"]),
        "no_javascript_pages": len(report["no_javascript_pages"]),
        "report": str(report_path),
        "failures": report["failures"],
    }
    print(json.dumps(summary, ensure_ascii=False))
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=checked_base, default=checked_base("http://127.0.0.1:8765"))
    parser.add_argument("--output", default="/tmp/taro-themed-site-qa")
    parser.add_argument("--locales", help="Comma-separated locale codes; default: all 20")
    parser.add_argument("--pages", help="Comma-separated page keys; default: all 12")
    parser.add_argument("--screenshots", action="store_true", help="Save 390px and 1440px first-screen captures")
    asyncio.run(main(parser.parse_args()))
