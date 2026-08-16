"""Regression tests for the skills exposed by the Claude plugin manifest."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = REPO_ROOT / ".claude-plugin" / "plugin.json"
CANONICAL_SKILL_PATH = "./skills/planning-with-files"
LOCALIZED_SKILL_PATHS = [
    "./skills/planning-with-files-ar",
    "./skills/planning-with-files-de",
    "./skills/planning-with-files-es",
    "./skills/planning-with-files-zh",
    "./skills/planning-with-files-zht",
]


def read_declared_skills() -> list[str]:
    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    return manifest["skills"]


def resolve_plugin_path(declared_path: str) -> Path:
    return REPO_ROOT / declared_path.removeprefix("./")


class ClaudePluginPackagingTests(unittest.TestCase):
    def test_manifest_exposes_only_the_canonical_skill(self) -> None:
        declared_skills = read_declared_skills()

        self.assertEqual(declared_skills, [CANONICAL_SKILL_PATH])
        canonical_skill = resolve_plugin_path(declared_skills[0])
        self.assertTrue(canonical_skill.is_dir(), canonical_skill)
        self.assertTrue((canonical_skill / "SKILL.md").is_file())

    def test_localized_skills_remain_available_but_are_not_exposed(self) -> None:
        declared_skills = read_declared_skills()

        for localized_path in LOCALIZED_SKILL_PATHS:
            with self.subTest(localized_path=localized_path):
                self.assertTrue(resolve_plugin_path(localized_path).is_dir())
                self.assertNotIn(localized_path, declared_skills)


if __name__ == "__main__":
    unittest.main()
