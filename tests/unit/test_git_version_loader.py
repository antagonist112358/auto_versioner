from auto_versioner.version import Version
from auto_versioner.git_version_loader import GitVersionLoader


class TestGitVersionLoader:
    def test_loads_self_version_file(self):
        loader = GitVersionLoader()
        min_version = Version("0.0.0.1")
        assert min_version < loader.highest_version
