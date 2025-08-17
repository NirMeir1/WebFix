import base64
import sys
import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def capture_screenshot_base64(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 360, "height": 700},
                device_scale_factor=2,
                is_mobile=True,
                has_touch=True
            )
            page = context.new_page()
            page.goto(url, timeout=10000)
            page.wait_for_timeout(1000)  # minimal wait for speed

            # Capture screenshot directly as bytes (in-memory)
            screenshot_bytes = page.screenshot(type='png')
            browser.close()

            # Convert to Base64 immediately
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            return screenshot_b64

    except Exception as e:
        logger.error(f"Screenshot capture failed for {url}: {e}")
        return ""
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = capture_screenshot_base64(sys.argv[1])
        if result:
            print(result, end="")  # ✅ Send base64 to stdout (no newline)
    else:
        print("No URL provided", file=sys.stderr)

