"""Copy media databases/artwork into the stopped, isolated portable test profile."""
import argparse
from pathlib import Path
import shutil
import sqlite3

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path, help="Existing Kodi userdata folder (read only)")
args = parser.parse_args()
target = Path(__file__).resolve().parents[1] / ".runtime/kodi/portable_data/userdata"
if not (target / "Database").is_dir():
    raise SystemExit("Start and stop the isolated Kodi profile once first")
for name in ("MyVideos131.db", "MyMusic83.db", "Textures13.db"):
    source = args.source / "Database" / name
    if source.exists():
        with sqlite3.connect(source.as_uri() + "?mode=ro", uri=True) as src:
            with sqlite3.connect(target / "Database" / name) as dst:
                src.backup(dst)
        print(f"Copied {name}")
shutil.copytree(args.source / "Thumbnails", target / "Thumbnails", dirs_exist_ok=True)
print("Copied artwork cache; original profile unchanged")
