import unittest
from unittest.mock import patch, Mock

import install


class TestInstallPackages(unittest.TestCase):

    @patch("install.subprocess.run")
    def test_runs_pacman_with_missing_packages(self, mock_run):
        mock_run.return_value = Mock(returncode=0)

        result = install.install_packages(["git", "nmap"])

        mock_run.assert_called_once_with(
            ["sudo", "pacman", "-S", "--needed", "git", "nmap"],
            check=False,
        )
        self.assertEqual(result, 0)

    @patch("install.subprocess.run")
    def test_returns_pacman_failure(self, mock_run):
        mock_run.return_value = Mock(returncode=7)

        result = install.install_packages(["git"])

        self.assertEqual(result, 7)


class TestInstallerMain(unittest.TestCase):

    def setUp(self):
        self.manifest = {
            "development": {
                "packages": ["git", "python"]
            }
        }

    @patch("install.install_packages")
    @patch("install.get_installed_packages", return_value={"git"})
    @patch("install.load_manifest")
    @patch("builtins.input", return_value="n")
    def test_cancellation_prevents_installation(
        self, mock_input, mock_manifest, mock_installed, mock_install
    ):
        mock_manifest.return_value = self.manifest

        result = install.main()

        self.assertEqual(result, 0)
        mock_install.assert_not_called()

    @patch("install.install_packages", return_value=0)
    @patch("install.get_installed_packages", return_value={"git"})
    @patch("install.load_manifest")
    @patch("builtins.input", return_value="y")
    def test_confirmation_starts_installation(
        self, mock_input, mock_manifest, mock_installed, mock_install
    ):
        mock_manifest.return_value = self.manifest

        result = install.main()

        self.assertEqual(result, 0)
        mock_install.assert_called_once_with(["python"])

    @patch("install.install_packages", return_value=7)
    @patch("install.get_installed_packages", return_value={"git"})
    @patch("install.load_manifest")
    @patch("builtins.input", return_value="y")
    def test_installation_failure_is_reported(
        self, mock_input, mock_manifest, mock_installed, mock_install
    ):
        mock_manifest.return_value = self.manifest

        result = install.main()

        self.assertEqual(result, 7)


if __name__ == "__main__":
    unittest.main()
