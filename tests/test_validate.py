import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate_evals, validate_skill


class ValidateSkillTest(unittest.TestCase):
    def validate(self, frontmatter: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "sample"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                f"---\n{frontmatter}\n---\n\n# Sample\n"
            )
            return validate_skill("sample", root)

    def test_accepts_valid_block_description(self):
        errors = self.validate("name: sample\ndescription: >\n  A useful skill.")
        self.assertEqual([], errors)

    def test_rejects_name_prefix_match(self):
        errors = self.validate("name: sample-extra\ndescription: A useful skill.")
        self.assertTrue(any("name must match" in error for error in errors))

    def test_accepts_known_optional_keys(self):
        errors = self.validate(
            "name: sample\ndescription: A useful skill.\nversion: 1\nlicense: MIT"
        )
        self.assertEqual([], errors)

    def test_rejects_unknown_keys(self):
        errors = self.validate(
            "name: sample\ndescription: A useful skill.\ndescripton: typo"
        )
        self.assertTrue(any("unknown frontmatter keys" in error for error in errors))

    def test_rejects_missing_description(self):
        errors = self.validate("name: sample")
        self.assertTrue(any("missing required" in error for error in errors))

    def test_rejects_duplicate_keys(self):
        errors = self.validate(
            "name: sample\nname: sample\ndescription: A useful skill."
        )
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_rejects_empty_description(self):
        errors = self.validate('name: sample\ndescription: ""')
        self.assertTrue(any("must not be empty" in error for error in errors))


class ValidateEvalsTest(unittest.TestCase):
    """Malformed manifests must yield error strings, never tracebacks."""

    def validate(self, manifest: object) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cases = root / "evals" / "cases"
            cases.mkdir(parents=True)
            (cases / "sample.json").write_text(json.dumps(manifest))
            return validate_evals("sample", root)

    def test_null_trigger_and_evals_report_errors(self):
        errors = self.validate(
            {"skill_name": "sample", "trigger": None, "evals": None}
        )
        self.assertTrue(any("trigger cases" in error for error in errors))
        self.assertTrue(any("behavioral eval" in error for error in errors))

    def test_non_object_manifest_reports_error(self):
        errors = self.validate(["not", "an", "object"])
        self.assertTrue(any("JSON object" in error for error in errors))

    def test_non_object_eval_case_reports_error(self):
        errors = self.validate({"skill_name": "sample", "evals": ["oops"]})
        self.assertTrue(any("index 0" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
