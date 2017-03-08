import subprocess

major_version = 0
minor_version = 1

# Auto-versioner generated information - DO NOT EDIT
last_tag = subprocess.check_output("git describe --abbrev=0 --tags".split(' ')).decode("utf-8")
revision = subprocess.check_output("git rev-list {}..HEAD --count".format(last_tag).split(' ')).decode("utf-8")
VERSION = "{}.{}.{}".format(major_version, minor_version, revision)
