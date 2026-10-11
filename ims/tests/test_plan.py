import unittest

from plan import build_plan


class TestBuildPlan(unittest.TestCase):

    def test_no_missing_packages(self):
        manifest = {
            "development": {
                "packages": ["git", "python"]
            }
        }
        installed = {"git", "python", "nmap"}

        self.assertEqual(build_plan(manifest, installed), [])

    def test_finds_missing_packages(self):
        manifest = {
            "development": {
                "packages": ["git", "python"]
            },
            "security": {
                "packages": ["nmap"]
            }
        }
        installed = {"git"}

        self.assertEqual(
            build_plan(manifest, installed),
            ["nmap", "python"]
        )

    def test_empty_manifest(self):
        self.assertEqual(build_plan({}, {"git"}), [])


if __name__ == "__main__":
    unittest.main()
