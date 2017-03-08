import functools
import logging as log
from auto_versioner import current_working_path
from auto_versioner.version import Version
from auto_versioner.git_runner import GitRunner


class GitVersionLoader:
    def __init__(self, loader_path=current_working_path):
        self._loader_path = loader_path
        self._git = GitRunner(loader_path)
        self._loaded_versions = self._load_git_versions()

    @property
    def versions(self):
        return self._loaded_versions

    @property
    def highest_version(self):
        if len(self._loaded_versions) > 0:
            return functools.reduce(lambda v1, v2: v1 if v1 > v2 else v2, self._loaded_versions)
        else:
            return None

    def _load_git_versions(self):
        versions = []
        try:
            version_strings = self._git.get_version_tags()
            for version_str in version_strings:
                try:
                    version = Version(version_str)
                    versions.append(version)
                except:
                    log.warning("Could not parse git tag '{}' as a version number".format(version_str))
        except:
            log.warning("Could not load any git tags")

        return versions
