import os
import runpy
import functools
import logging as log
import auto_versioner
from auto_versioner.version import Version


class VersionFileLoader:
    _version_file_names = [name + ".py" for name in ['version', '__version', '__version__', '_version_']]
    _version_attribs = ['VERSION', 'version', '__version__']

    def __init__(self, loader_path=auto_versioner.current_working_path):
        self._loader_path = loader_path
        self._loader_module = loader_path.split('/')[-1]
        self._loaded_version = []
        version_files = self._check_for_version_files()

        if len(version_files) > 1:
            log.warning("Found multiple version files ({})".format(", ".join(version_files)))

        versions = []
        for found_file in version_files:
            self._load_version_attributes(found_file, versions)

        if versions:
            versions_string = ", ".join(map(lambda v: str(v), versions))
            log.info("Found versions '{}' in project version file(s)".format(versions_string))
            self._loaded_versions = versions

    @property
    def versions(self):
        return self._loaded_versions

    @property
    def highest_version(self):
        if len(self._loaded_versions) > 0:
            return functools.reduce(lambda v1, v2: v1 if v1 > v2 else v2, self._loaded_versions)
        else:
            return None

    def _check_for_version_files(self):
        found_files = []
        for filename in VersionFileLoader._version_file_names:
            if os.path.exists(os.path.join(self._loader_path, filename)):
                found_files.append(filename)

        return found_files

    def _load_version_attributes(self, filename, version_attributes):
        search_attribs = VersionFileLoader._version_attribs
        loader_path = self._loader_path
        absolute_filepath = os.path.join(loader_path, filename)

        try:
            version_module = runpy.run_path(absolute_filepath)
            found_attributes = [attrib for attrib in search_attribs if attrib in version_module]
            for found_attrib in found_attributes:
                version_attrib = str(version_module[found_attrib])
                log.info("Found version attribute '{}' in file: {}".format(version_attrib, filename))
                try:
                    version = Version(version_attrib)
                    version_attributes.append(version)
                except:
                    log.warning("Could not parse version string '{}' from file: {}".format(version_attrib, filename))
        except Exception:
            log.warning("Could not load any version attributes from version file: {}".format(filename))
