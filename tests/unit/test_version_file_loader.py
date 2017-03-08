from auto_versioner import Version
from auto_versioner import FileVersionLoader


class TestVersionFileLoader:
    def test_loads_self_version_file(self):
        loader = FileVersionLoader()
        min_version = Version("0.0.0.1")
        assert min_version < loader.highest_version
