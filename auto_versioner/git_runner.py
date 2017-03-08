import re
import subprocess
from auto_versioner import auto_versioner_path


class GitRunner:
    _version_tag_regex = re.compile('[0-9]+\.[0-9]+\.[0-9]+\.*')

    def __init__(self, git_repo_path=auto_versioner_path):
        self.git_installed = GitRunner._check_git_installed()
        self.git_repo_path = git_repo_path
        self._version_tags = None

    def get_version_tags(self):
        if self._version_tags:
            return self._version_tags
        else:
            all_tags = self._run_if_installed("tag").split('\n')
            self._version_tags = [x for x in all_tags if GitRunner._version_tag_regex.match(x)]
            return self._version_tags

    @property
    def latest_version_tag(self):
        v_tags = self.get_version_tags()
        if v_tags:
            return v_tags[-1]
        else:
            return None

    @property
    def current_branch_name(self):
        return self._run_if_installed("rev-parse --abbrev-ref HEAD").rstrip('\n')

    def git_exec(self, commands):
        if isinstance(commands, str):
            commands = commands.split(' ')

        git_commands = ["git"] + commands
        return subprocess.check_output(git_commands, cwd=self.git_repo_path).decode("utf-8")

    def _run_if_installed(self, command):
        if self.git_installed:
            try:
                return self.git_exec(command)
            except Exception:
                raise RuntimeError('The path "{}" does not appear to be a git repository.'.format(self.git_repo_path))
        else:
            raise RuntimeError('git does not appear to be installed on this computer')

    @staticmethod
    def _check_git_installed():
        try:
            _ = GitRunner._raw_git_exec("--version")
            return True
        except Exception:
            return False

    @staticmethod
    def _raw_git_exec(cmd_str):
        commands = cmd_str.split(' ')
        git_command = ["git"] + commands
        return subprocess.check_output(git_command).decode("utf-8")
