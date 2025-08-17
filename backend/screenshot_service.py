import logging
import subprocess
import sys

logger = logging.getLogger(__name__)

def run_screenshot_subprocess(url: str) -> str:
    try:
        result = subprocess.run(
            [sys.executable, "backend/capture_screenshot.py", url],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("Screenshot completed")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error("Screenshot subprocess failed: %s", e.stderr.strip())
    except Exception:
        logger.exception("Unexpected screenshot error")
    return ""
