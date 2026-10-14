"""Native integration checks. Invoke with RunScript from the isolated test Kodi."""
import json
import os
import xbmc
import xbmcgui
import xbmcvfs

profile = xbmcvfs.translatePath("special://home/")
if "kodi-skin" not in profile or ".runtime" not in profile:
    raise RuntimeError("Smoke checks must only run in the isolated development profile")
out = os.path.dirname(os.path.dirname(profile.rstrip("\\/")))
results = []


def rpc(method, params=None):
    command = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        command["params"] = params
    return json.loads(xbmc.executeJSONRPC(json.dumps(command)))


def check(name, condition, detail=""):
    results.append({"name": name, "passed": bool(condition), "detail": detail})
    with open(os.path.join(out, "smoke.json"), "w") as handle:
        json.dump(results, handle, indent=2)


def focus():
    return xbmc.getInfoLabel("System.CurrentControlId")


def builtin(action):
    xbmc.executebuiltin(action)
    xbmc.sleep(1000)


def key(action):
    rpc("Input." + action)
    xbmc.sleep(800)


def shot(name):
    xbmc.executebuiltin('TakeScreenshot("%s")' % os.path.join(out, name + ".png"))
    xbmc.sleep(300)


xbmc.sleep(6500)
builtin("Dialog.Close(all,true)")
builtin("ActivateWindow(Home)")
builtin("SetFocus(9000)")
check("skin active", xbmc.getSkinDir() == "skin.elegantfin")
check("home focus", focus() == "9000", focus())
shot("verified-home")
key("Down")
check("down reaches resume row", focus() == "5100", focus())
key("Down")
check("down reaches TV resume row", focus() == "5150", focus())
key("Info")
check("episode info opens", xbmcgui.getCurrentWindowDialogId() == 12003)
check("episode title visible", xbmc.getCondVisibility("Control.IsVisible(400)"))
shot("verified-episode")
key("Back")
key("Down")
check("down reaches posters", focus() == "5200", focus())
shot("verified-posters")
key("Info")
check("movie info opens", xbmcgui.getCurrentWindowDialogId() == 12003)
check("movie play focused", focus() == "8", focus())
shot("verified-info")
key("Down")
check("plot reachable", focus() == "138", focus())
key("Select")
check("full plot opens", xbmcgui.getCurrentWindowDialogId() == 11102, str(xbmcgui.getCurrentWindowDialogId()))
key("Back")
key("Down")
check("cast reachable", focus() == "50", focus())
shot("verified-cast")
key("Back")
builtin("ActivateWindow(Home)")
builtin("Skin.SetBool(ef_hide_resume)")
builtin("SetFocus(9000)")
key("Down")
check("hidden resume rows skipped", focus() == "5200", focus())
builtin("Skin.Reset(ef_hide_resume)")
builtin("ActivateWindow(SkinSettings)")
check("skin settings opens", xbmcgui.getCurrentWindowId() == 10035, str(xbmcgui.getCurrentWindowId()))
shot("verified-skinsettings")
builtin("ActivateWindow(Home)")
builtin("SetFocus(12)")
key("Select")
check("native search opens keyboard", xbmcgui.getCurrentWindowDialogId() == 10103, str(xbmcgui.getCurrentWindowDialogId()))
shot("verified-search")
key("Back")
builtin("ActivateWindow(Settings)")
check("system settings opens", xbmcgui.getCurrentWindowId() == 10004)
shot("verified-settings")
builtin("ActivateWindow(Home)")
check("returned home", xbmcgui.getCurrentWindowId() == 10000)
