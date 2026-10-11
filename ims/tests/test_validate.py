
import unittest

from validate import validate_manifest


class TestValidateManifest(unittest.TestCase):

    def test_unknown_category(self):
        manifest = {
            "banana": {
                "packages": ["git"]
            }
        }

        errors = validate_manifest(manifest)

        self.assertTrue(
            any("unknown category" in error for error in errors)
        )

    def test_valid_manifest(self):
        manifest = {
            "development": {
                "packages": ["git", "python"]
            },
            "security": {
                "packages": ["nmap"]
            },
        }

        self.assertEqual(validate_manifest(manifest), [])

    def test_empty_manifest(self):
        errors = validate_manifest({})
        self.assertTrue(errors)

    def test_missing_packages_list(self):
        manifest = {
            "development": {}
        }

        errors = validate_manifest(manifest)
        self.assertTrue(errors)

    def test_packages_must_be_a_list(self):
        manifest = {
            "development": {
                "packages": "git"
            }
        }

        errors = validate_manifest(manifest)
        self.assertTrue(errors)

    def test_empty_package_name(self):
        manifest = {
            "development": {
                "packages": ["git", ""]
            }
        }

        errors = validate_manifest(manifest)
        self.assertTrue(errors)

    def test_duplicate_package(self):
        manifest = {
            "development": {
                "packages": ["git"]
            },
            "security": {
                "packages": ["git"]
            },
        }

        errors = validate_manifest(manifest)

        self.assertTrue(
            any("appears in both" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
