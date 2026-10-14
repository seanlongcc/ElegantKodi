# ElegantKodi

A native Kodi skin inspired by [lscambo13's ElegantFin](https://github.com/lscambo13/ElegantFin).
Built for **Kodi 21 Omega**, including the locally installed **Kodi 21.2 Windows Store edition**.
The Kodi add-on is currently named **ElegantFin**, with ID `skin.elegantfin`.

The home screen uses rounded library tiles, horizontal artwork shelves, white focus
outlines, slate backgrounds and violet accents. Movie details use a full backdrop,
centered clear logo (or title), playback actions, plot and cast. Estuary provides
the complete native library, music, PVR, settings, keyboard and playback foundation.

## Install

1. In Kodi, open **Settings > Add-ons > Install from zip file**.
2. Select `dist/skin.elegantfin-1.0.0.zip` from this project folder. If Kodi blocks
   third-party ZIPs, enable **Settings > System > Add-ons > Unknown sources** yourself,
   then return to Install from zip file.
3. Accept the skin switch and select **Yes** to keep it. Alternatively, choose
   **Settings > Interface > Skin > Skin > ElegantFin**.

On this computer the ZIP is at:

```text
C:\Users\seanl\Documents\Code\kodi-skin\dist\skin.elegantfin-1.0.0.zip
```

To go back, choose **Settings > Interface > Skin > Skin > Estuary**. The add-on has
its own `skin.elegantfin` ID and does not replace Estuary or modify your media database.

## Library And Controls

- Movies and TV shelves read the native Kodi library. Jellyfin for Kodi content
  appears after that add-on syncs it into Kodi. JellyCon-only or other unsynced
  plug-in libraries remain accessible through **Add-ons**, not native shelves.
- Continue Watching appears only for unfinished items with saved resume positions.
- Missing artwork gets a built-in fallback. Clear-logo artwork is optional.
- Arrow keys or a remote navigate rows; Enter opens/plays; Back returns; `I` opens
  information and `C` opens the native context menu.
- Search uses Global Search when installed and enabled; otherwise it uses native video
  search. No helper add-on is required.
- **Settings > Interface > Skin > Configure skin** controls visible shelves,
  clock, fanart, automatic text scrolling and inherited screen animations.
- Kodi's library view menu still offers List, Poster, Wall and other native views.

## Build

Python 3 is sufficient to validate and package the checked-in skin:

```bash
python3 -m unittest discover -s tests -v
python3 tools/package.py
```

The ZIP contains one `skin.elegantfin/` root. Packaging validates XML and resources,
uses stable timestamps and produces a SHA-256 checksum alongside the archive.

Only regenerating the small interface PNGs needs Pillow:

```bash
python3 -m pip install Pillow
python3 tools/generate_assets.py
```

Edit `skin.elegantfin/xml/Home.xml` for home composition,
`xml/Includes_ElegantFin.xml` for shelf/card components, `xml/DialogVideoInfo.xml`
for movie details, and `colors/defaults.xml` for the palette.

## Native Verification

Development uses an isolated portable copy of the existing Kodi installation under
`.runtime/kodi`, launched with `-p -nofs`. The original Kodi profile is not changed.
`tools/native_probe.py` and `tools/native_smoke.py` run inside that isolated Kodi;
both reject ordinary user profiles. `tools/kodi_control.ps1` sends native EventServer
commands over Windows loopback. These development tools are excluded from the ZIP.

Verified on Kodi 21.2 at a 1600 x 900 window: 10 offline package tests and 17 native
interaction checks passed. Native checks cover home navigation, movie/episode
information, full plot, cast, hidden shelves, search, skin settings and system
settings. The Kodi log contained no errors during the final run. Playback controls
and PVR retain their Estuary implementation; live playback and a PVR backend were
not exercised. See `docs/verification.md` for details.

The skin is designed at 1920 x 1080 and scaled by Kodi. Primary target is a 16:9
desktop/TV. Kodi 22 and unusual aspect ratios have not been verified. Kodi's native
renderer does not provide CSS backdrop blur, so the adaptation uses translucent
textures and shading. Secondary layouts retain Estuary structure with shared styling.

## Credits

Independent adaptation, not an official ElegantFin/Jellyfin/Team Kodi release.
See `skin.elegantfin/NOTICE.md` and `skin.elegantfin/LICENSE.txt` for attribution.
Estuary code and new skin code: GPL v2. Interface artwork: CC BY-SA 4.0.
Fonts retain their bundled licenses. Media artwork is supplied by your own library.
