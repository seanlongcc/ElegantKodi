# Verification

## Environment

- Kodi 21.2 Omega, Windows Store installation version 21.2.500.0.
- Isolated portable copy of that runtime, GUI ABI 5.17.0.
- Rendered natively in a 1600 x 900 window using the skin's 1920 x 1080 layout.
- A read-only database snapshot and copied artwork supplied populated library tests.
- No original profile settings, databases, credentials or add-ons were changed.

## Results

`python3 -m unittest discover -s tests -v`: 10 tests passed.

Coverage includes manifest compatibility, XML/playlists, included files, fonts,
custom and packed textures, search fallback, radio entry, episode identity,
native windows and attribution assets. Four review regressions were reproduced
as failing tests before their fixes.

`tools/native_smoke.py`: 17 checks passed inside Kodi:

- Skin activation and initial library focus.
- Down navigation through movie resume, episode resume and movie poster shelves.
- Episode information and visible episode identity.
- Movie information and initial Play focus.
- Plot focus, expanded plot dialog and cast navigation.
- Hidden resume shelves skipped correctly.
- Skin settings, native search keyboard and system settings opened.
- Return to Home.

Native screenshots in `.runtime/verified-*.png` were inspected for artwork,
rounded masks, focus borders, text placement and navigation state. The final
native run produced no Kodi log errors. Test scripts and library snapshots are
not included in the distributable ZIP.

## Remaining Limits

- Playback/OSD, live TV/radio, game add-ons and external Global Search have not been
  exercised against live sources. Those windows retain the native Estuary base.
- Kodi 22, touch operation and non-16:9 displays are not verified.
- Secondary library/settings/player layouts are themed Estuary, not replicas of
  every ElegantFin web screen. Kodi does not implement CSS backdrop blur.
- Native captures on this machine appear dimmer than the authored texture values;
  screenshots have not been color-corrected or used to alter global display settings.
