# ElegantFin for Kodi

Build an installable Kodi skin inspired by lscambo13's ElegantFin for Jellyfin.
The local installation is Kodi 21.2 Omega, Microsoft Store package 21.2.500.0,
with skin ABI 5.17.0. Media comes from the existing Kodi library, including
items synced by Jellyfin for Kodi. No server configuration belongs in the skin.

## Design

Use the installed Estuary 4.0.0 as the complete native window/dialog foundation.
Ship under a separate `skin.elegantfin` ID. Keep licenses and attribution.
Create a spacious horizontal home: centered Home/Favourites navigation,
library shortcuts, conditional resume shelves, and recently added movie/TV rows.
Use rounded artwork, subtle slate surfaces, white focus outlines, muted metadata,
violet actions and green watched indicators, matching the supplied reference.
Artwork must come from the user's library. Empty libraries remain navigable.
Retheme shared backgrounds, dialogs and controls; retain native library views,
music, PVR, keyboard, settings, playback OSD and accessibility functions.

## Delivery And Verification

Deliver editable source, an installable ZIP, a deterministic package command,
and clear Windows/Store installation and rollback steps. Require no helper add-on.
Validate XML, includes, fonts, assets, add-on metadata and archive structure.
Test the skin in an isolated Kodi 21.2 portable profile if the installed executable
can run there. Use Kodi's own screenshot API for visual verification. Do not
rewrite the user's database, media, or Jellyfin configuration.

## Scope

This is a native visual adaptation, not a CSS import or an official ElegantFin port.
Kodi cannot reproduce browser backdrop blur exactly. Existing Estuary secondary
layouts receive the shared theme; Jellyfin-specific web administration is absent.
