"""Run inside the isolated Kodi portable profile, never the user's profile.

RunScript(path/to/native_probe.py,bootstrap|home|down|movies|settings|skinsettings|info)
"""
import json
import os
import sys
import time
import xbmc
import xbmcgui
import xbmcvfs

profile = xbmcvfs.translatePath("special://home/")
if "kodi-skin" not in profile or ".runtime" not in profile:
    raise RuntimeError("This probe only runs in the isolated development profile")
out = os.path.dirname(os.path.dirname(profile.rstrip("\\/")))
mode = sys.argv[1] if len(sys.argv) > 1 else "home"


def rpc(method, params=None):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        payload["params"] = params
    return json.loads(xbmc.executeJSONRPC(json.dumps(payload)))


if mode == "bootstrap":
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.sleep(1500)
    rpc("Addons.SetAddonEnabled", {"addonid": "skin.elegantfin", "enabled": True})
    rpc("Settings.SetSettingValue", {"setting": "lookandfeel.skin", "value": "skin.elegantfin"})
    xbmc.sleep(1500)
elif mode == "down":
    rpc("Input.Down")
elif mode == "movies":
    xbmc.executebuiltin("ActivateWindow(Videos,videodb://movies/titles/,return)")
elif mode == "settings":
    xbmc.executebuiltin("ActivateWindow(Settings)")
elif mode == "skinsettings":
    xbmc.executebuiltin("ActivateWindow(SkinSettings)")
elif mode == "info":
    rpc("Input.Info")
elif mode == "confirm":
    xbmc.executebuiltin("SendClick(11)")
else:
    xbmc.executebuiltin("ActivateWindow(Home)")
xbmc.sleep(6500)
state = {"mode": mode, "skin": xbmc.getSkinDir(), "window": xbmcgui.getCurrentWindowId(),
         "dialog": xbmcgui.getCurrentWindowDialogId(), "focus": xbmc.getInfoLabel("System.CurrentControlId"),
         "containers": {str(i): xbmc.getInfoLabel("Container(%s).NumItems" % i) for i in [9000,5100,5150,5200,5300,5400]}}
with open(os.path.join(out, "probe-" + mode + ".json"), "w") as handle:
    json.dump(state, handle, indent=2)
xbmc.executebuiltin('TakeScreenshot("%s")' % os.path.join(out, mode + ".png"))
