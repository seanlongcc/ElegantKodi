"""Validate source and build a deterministic Kodi Install-from-ZIP archive."""
from pathlib import Path
import hashlib
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
skin = ROOT / "skin.elegantfin"
addon = ET.parse(skin / "addon.xml").getroot()
output = ROOT / "dist" / f"{addon.get('id')}-{addon.get('version')}.zip"
output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(skin.rglob("*")):
        if not path.is_file():
            continue
        info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(2026, 10, 14, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
    assert "skin.elegantfin/addon.xml" in archive.namelist()
    count = len(archive.namelist())
digest = hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix(".sha256").write_text(f"{digest}  {output.name}\n", encoding="ascii")
print(f"Built {output} ({output.stat().st_size:,} bytes, {count} files)\nSHA256 {digest}")
