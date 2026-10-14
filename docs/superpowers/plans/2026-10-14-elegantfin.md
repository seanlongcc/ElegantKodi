# ElegantFin Implementation Plan

**Goal:** Deliver a usable, packaged Kodi 21.2 skin matching ElegantFin's visual language.
**Architecture:** Complete Estuary foundation plus custom home, shared colors and textures.
**Tech Stack:** Kodi XML, PNG assets, Python standard-library validation/packaging; Pillow for asset generation.
**Spec:** `docs/superpowers/specs/2026-10-14-elegantfin-design.md`

## Global Constraints

- Add-on ID `skin.elegantfin`; Kodi GUI ABI 5.17.0.
- No required third-party helper services.
- Keep attribution and original license notices.
- Preserve user's existing Kodi profile and Jellyfin configuration.

## Review Focus

- Empty libraries: functional library shortcuts and no dead shelves.
- Missing artwork: bundled fallbacks and readable labels.
- Long titles: constrained widths and focused scrolling.
- Keyboard navigation: reachable navigation, content, settings and exit.
- Packaging: every include, font and custom texture available offline.

## Tasks

- [x] 1. Add validation tests, observe missing-package failure, import matching Estuary foundation.
- [x] 2. Implement theme assets, custom home and native shelves; validate XML and resource contracts.
- [x] 3. Verify native rendering and navigation in isolated Kodi profile; repair observed issues.
- [x] 4. Package ZIP, document installation/rollback, run final validation and review.
