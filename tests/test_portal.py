from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


PORTAL_PATH = Path(__file__).resolve().parents[1] / "app.py"
REGISTRY_MODULE_PATH = PORTAL_PATH.with_name("portal_registry.py")
REGISTRY_PATH = PORTAL_PATH.with_name("portal_apps.json")


def _literal_assignment(module: ast.Module, name: str):
    for node in module.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                return ast.literal_eval(node.value)
    raise AssertionError(f"Missing assignment: {name}")


class PortalAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = PORTAL_PATH.read_text(encoding="utf-8")
        cls.module = ast.parse(cls.source)

        spec = importlib.util.spec_from_file_location("portal_registry", REGISTRY_MODULE_PATH)
        assert spec and spec.loader
        cls.registry_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.registry_module)

    def test_portal_has_two_existing_streamlit_apps(self) -> None:
        apps = self.registry_module.load_portal_apps(REGISTRY_PATH)
        self.assertEqual(len(apps), 2)
        self.assertEqual(
            {app["url"] for app in apps},
            {
                "https://shieldcoating-sds-v24.streamlit.app/",
                "https://insta-process-mobile.streamlit.app/",
            },
        )

    def test_portal_keeps_existing_admin_deep_link(self) -> None:
        apps = self.registry_module.load_portal_apps(REGISTRY_PATH)
        admin_url = apps[0]["admin_url"]
        self.assertEqual(
            admin_url,
            "https://shieldcoating-sds-v24.streamlit.app/?admin=1",
        )

    def test_all_destinations_are_https_streamlit_urls(self) -> None:
        apps = self.registry_module.load_portal_apps(REGISTRY_PATH)
        urls = [app["url"] for app in apps]
        urls.extend(app["admin_url"] for app in apps if app.get("admin_url"))
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(url.startswith("https://"))
                self.assertIn(".streamlit.app/", url)

    def test_portal_uses_current_streamlit_width_api(self) -> None:
        self.assertIn('width="stretch"', self.source)
        self.assertNotIn("use_container_width", self.source)

    def test_registry_rejects_non_streamlit_destinations(self) -> None:
        payload = {
            "apps": [
                {
                    "name": "Unsafe",
                    "description": "Unsafe destination",
                    "url": "https://example.com/",
                    "button": "Open",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "portal_apps.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.registry_module.load_portal_apps(path)


if __name__ == "__main__":
    unittest.main()
