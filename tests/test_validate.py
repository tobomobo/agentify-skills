import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate_skill


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

    def test_rejects_duplicate_keys(self):
        errors = self.validate(
            "name: sample\nname: sample\ndescription: A useful skill."
        )
        self.assertTrue(any("duplicate" in error for error in errors))

    def test_rejects_empty_description(self):
        errors = self.validate('name: sample\ndescription: ""')
        self.assertTrue(any("must not be empty" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
