import os

auto_versioner_path = os.path.dirname(os.path.realpath(__file__))
current_working_path = os.getcwd()

__version__ = "0.1.0.0"

from auto_versioner.version import Version
from auto_versioner.git_runner import GitRunner
from auto_versioner.git_version_loader import GitVersionLoader
from auto_versioner.version_file_loader import VersionFileLoader as FileVersionLoader
from auto_versioner.controller import Controller
