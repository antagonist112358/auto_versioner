import sys
import os
from auto_versioner import current_working_path, FileVersionLoader, GitRunner, GitVersionLoader, Version


class Controller:
    def __init__(self, project_path=current_working_path):
        self.project_path = project_path
        self._file_loader = FileVersionLoader(project_path)
        try:
            self._git_loader = GitVersionLoader(project_path)
        except:
            sys.stderr.writeln("auto_versioner requires git to be installed.")
            sys.exit(2)
        try:
            self._git_runner = GitRunner(project_path)
            _ = self._git_runner.git_exec("status")
        except:
            sys.stderr.writeln("auto_versioner must be run from within a git repository directory")
            sys.exit(3)

    def run(self):
        self._collect_information()
        self._update_version_information()

    def _collect_information(self):
        file_version = self._file_loader.highest_version
        git_version = self._git_loader.highest_version
        git_branch = self._git_runner.current_branch_name

        # If we have neither a git tag version nor a {version}.py file version, we cannot continue
        if not file_version and not git_version:
            sys.stderr.writeln("auto_versioner - no version information found for project in {}"
                               .format(current_working_path))
            print("You must have a version defined in either:")
            print("\tgit - as a version number tag (e.g. '0.4.1')")
            print("\t{version}.py - as a version field (e.g. 'version = '0.4.1')")
            print("As no version information has been found, auto_versioner cannot continue.")
            sys.exit(1)

        print("Detected git branch: {}".format(git_branch))

        if file_version:
            print("Found (highest) version: {} in version file(s)".format(file_version))
        if git_version:
            print("Found (highest) version: {} in git tags".format(git_version))

        self.file_version = file_version
        self.git_version = git_version
        self.branch_name = git_branch

    def _update_version_information(self):
        def update_when_no_file_version(git_version):
            print("No file versions found...computing version from git tag version: {}".format(git_version))
            revision = self._determine_revision_number()
            if self.branch_name == 'master':
                current_version = Version(git_version.major_version, git_version.minor_version, 0, revision)
            else:
                current_version = Version(git_version.major_version, git_version.minor_version, revision, 0)

            print("Writing 'version.py'...")
            with open(os.path.join(self.project_path, "version.py"), "w") as file:
                file.write("VERSION = {}".format(current_version))
            return current_version

        def update_when_no_git_version(file_version):
            print("No git versions found...computing version from version file version: {}".format(file_version))
            revision = self._determine_revision_number()
            if self.branch_name == 'master':
                current_version = Version(file_version.major_version, file_version.minor_version, 0, revision)
            else:
                current_version = Version(file_version.major_version, file_version.minor_version, revision, 0)

            print("Adding git tag for version...")
            self._git_runner.git_exec("tag {} HEAD".format(current_version))
            return current_version

        def update(file_version, git_version):
            newest_version = None if file_version == git_version else \
                file_version if file_version > git_version else git_version

            print("Highest found version number is: {}".format(newest_version or git_version))

            # Update the version file or the git tag if a new major/minor version exists
            if newest_version:
                file_maj_min_v = Version(file_version.major_version, file_version.minor_version, 0, 0)
                git_maj_min_v = Version(git_version.major_version, git_version.minor_version, 0, 0)

                if file_maj_min_v > git_maj_min_v:
                    print("Adding git tag for newest version...")
                    self._git_runner.git_exec("tag {} HEAD".format(file_version))
                    return file_version
                elif git_maj_min_v > file_maj_min_v:
                    print("Updating 'version.py' to newest version...")
                    with open(os.path.join(self.project_path, "version.py"), "w") as file:
                        file.write("VERSION = {}".format(git_version))
                    return git_version
                else:
                    # Major/Minor version numbers are the same, so just pick the highest
                    revision = self._determine_revision_number()
                    print("Git revision number is: {}".format(revision))
                    nv = newest_version
                    return Version(nv.major_version, nv.minor_version, nv.revision + revision, nv.fix_version)

            # git / file versions only differ by revision or fix version
            else:
                revision = self._determine_revision_number()
                print("Git revision number is: {}".format(revision))

                if self.branch_name == "master":
                    print("In master branch, so revision will be written to 'fix_version'")
                    current_version = Version(git_version.major_version, git_version.minor_version,
                                              git_version.revision, revision)
                else:
                    current_version = Version(git_version.major_version, git_version.minor_version,
                                              revision, 0)
                return current_version

        git_v = self.git_version
        file_v = self.file_version

        if git_v and not file_v:
            curr_version = update_when_no_file_version(git_v)
        elif file_v and not git_v:
            curr_version = update_when_no_git_version(file_v)
        else:
            curr_version = update(file_v, git_v)

        print("Project is now at version: {}".format(curr_version))
        self.current_version = curr_version

    def _determine_revision_number(self):
        if self.git_version:
            # Determine from git tags
            latest_git_version = self._git_runner.latest_version_tag
            if latest_git_version:
                count = self._git_runner.git_exec("rev-list {}..HEAD --count".format(latest_git_version))
                return int(count)
            else:
                count = self._git_runner.git_exec("rev-list HEAD --count")
                return int(count)
        else:
            # Determine from file version
            return self.file_version.revision
