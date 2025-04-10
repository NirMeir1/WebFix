import os
import sys
import uuid
import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def capture_screenshot(url: str) -> str:
    screenshot_dir = "static/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    filename = f"mobile_{uuid.uuid4()}.png"
    path = os.path.join(screenshot_dir, filename)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 360, "height": 700},
                device_scale_factor=1,      # High-resolution look
                is_mobile=True,
                has_touch=True
            )
            page = context.new_page()
            page.goto(url, timeout=20000)      # max page load
            page.wait_for_timeout(3000)        # max for visible render
            page.screenshot(path=path)         # Only visible viewport (fast)
            browser.close()

        logger.info(f"Screenshot saved at {path}")
        print(path, end="")  # Output path for subprocess
        return path
    except Exception as e:
        logger.error(f"Screenshot failed for {url}: {str(e)}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        capture_screenshot(sys.argv[1])
    else:
        print("No URL provided", file=sys.stderr)