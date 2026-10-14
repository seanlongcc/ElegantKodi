"""Offline release checks for the Kodi skin, including inherited windows."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "skin.elegantfin"


class SkinPackageTests(unittest.TestCase):
    def test_installable_omega_manifest(self):
        self.assertTrue((SKIN / "addon.xml").exists(), "Installable skin manifest is missing")
        root = ET.parse(SKIN / "addon.xml").getroot()
        self.assertEqual(root.get("id"), "skin.elegantfin")
        self.assertEqual(root.find("requires/import[@addon='xbmc.gui']").get("version"), "5.17.0")
        self.assertIsNotNone(root.find("extension[@point='xbmc.gui.skin']/res[@default='true']"))

    def test_all_xml_and_playlists_parse(self):
        files = list(SKIN.rglob("*.xml")) + list(SKIN.rglob("*.xsp"))
        self.assertGreater(len(files), 80, "Full native window/dialog foundation is missing")
        for file in files:
            with self.subTest(file=file.name):
                ET.parse(file)

    def test_included_files_and_fonts_exist(self):
        self.assertTrue((SKIN / "xml/Includes.xml").exists())
        for file in (SKIN / "xml").glob("*.xml"):
            root = ET.parse(file).getroot()
            for include in root.findall(".//include[@file]"):
                self.assertTrue((file.parent / include.get("file")).is_file(), include.get("file"))
        for filename in ET.parse(SKIN / "xml/Font.xml").findall(".//filename"):
            # Arial is Kodi's own Unicode fallback, shipped in media/Fonts.
            self.assertTrue(filename.text == "arial.ttf" or (SKIN / "fonts" / filename.text).is_file(), filename.text)

    def test_custom_assets_resolve(self):
        self.assertTrue((SKIN / "xml/Includes_ElegantFin.xml").exists())
        for file in (SKIN / "xml").glob("*.xml"):
            for name in re.findall(r"elegantfin/[a-zA-Z0-9_./-]+\.png", file.read_text(encoding="utf-8-sig")):
                self.assertTrue((SKIN / "media" / name).is_file(), f"{file.name}: {name}")

    def test_custom_screens_have_no_missing_static_textures(self):
        packed = set(re.findall(rb"[a-zA-Z0-9_./-]+\.png", (SKIN / "media/Textures.xbt").read_bytes()))
        for name in ("Home", "Includes_ElegantFin", "DialogVideoInfo", "SkinSettings"):
            for node in ET.parse(SKIN / "xml" / f"{name}.xml").iter():
                values = [node.text or ""] + list(node.attrib.values())
                for value in values:
                    if value.endswith(".png") and "$" not in value:
                        self.assertTrue((SKIN / "media" / value).is_file() or value.lower().encode() in packed, value)

    def test_search_falls_back_for_disabled_addon(self):
        search = ET.parse(SKIN / "xml/Home.xml").find(".//control[@id='12']")
        for action in search.findall("onclick"):
            self.assertIn("System.AddonIsEnabled(script.globalsearch)", action.get("condition"))

    def test_radio_only_users_have_an_entry(self):
        items = ET.parse(SKIN / "xml/Home.xml").findall(".//control[@id='9000']/content/item")
        self.assertTrue(any(item.findtext("visible") == "PVR.HasRadioChannels" and
                            "radio" in item.findtext("onclick", "").lower() for item in items))

    def test_episode_identity_is_not_replaced_by_series_logo(self):
        labels = ET.parse(SKIN / "xml/DialogVideoInfo.xml").findall(".//control[@type='label']")
        self.assertTrue(any("VideoInfoSubLabelVar" in node.findtext("label", "") and
                            "episode" in node.findtext("visible", "") for node in labels))

    def test_native_windows_remain_available(self):
        for name in ["Home", "MyVideoNav", "MyMusicNav", "Settings", "SettingsCategory",
                     "DialogVideoInfo", "DialogKeyboard", "VideoOSD", "MyPVRGuide"]:
            self.assertTrue((SKIN / "xml" / f"{name}.xml").is_file(), name)

    def test_attribution_and_metadata_assets(self):
        self.assertTrue((SKIN / "LICENSE.txt").is_file())
        self.assertTrue((SKIN / "NOTICE.md").is_file())
        self.assertTrue((SKIN / "addon.xml").is_file())
        for asset in ET.parse(SKIN / "addon.xml").findall(".//assets/*"):
            self.assertTrue((SKIN / asset.text).is_file(), asset.text)


if __name__ == "__main__":
    unittest.main()
