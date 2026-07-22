import qrcode
import os
from datetime import datetime

TOOL_NAME = "qr"
TOOL_DESCRIPTION = "generates a QR code image from text or a URL"
TOOL_ARGS = {"content": "str"}

OUTPUT_DIR = os.path.expanduser("~/zyp/state/qrcodes")


def run(args: dict) -> dict:
    content = args.get("content", "").strip()

    if not content:
        return {"status": "error", "result": "no content provided"}

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(OUTPUT_DIR, filename)

        img = qrcode.make(content)
        img.save(path)

        return {"status": "ok", "result": f"QR code saved to {path}"}
    except Exception as e:
        return {"status": "error", "result": f"qr generation failed: {e}"}
