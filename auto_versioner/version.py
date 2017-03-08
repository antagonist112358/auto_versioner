class Version:
    def __init__(self, *args):
        if len(args) == 1:
            self.__init_from_version_tag__(args[0])
        else:
            self.__init_from_components__(*args)

    def __init_from_components__(self, major, minor, revision=0, fix=0):
        if isinstance(major, str):
            major = int(major)
        if isinstance(minor, str):
            minor = int(minor)
        if isinstance(revision, str):
            revision = int(revision)
        if isinstance(fix, str):
            fix = int(fix)
        self.major_version = major
        self.minor_version = minor
        self.revision = revision
        self.fix_version = fix
        self.version_tag = "{}.{}.{}.{}".format(major, minor, revision, fix)

    def __init_from_version_tag__(self, version_tag):
        self.version_tag = version_tag
        version_comps = version_tag.split('.')
        self.major_version = int(version_comps[0])
        self.minor_version = int(version_comps[1])
        self.revision = int(version_comps[2] or 0)
        self.fix_version = int(version_comps[3] or 0)

    def __str__(self):
        return self.version_tag

    def __hash__(self):
        return hash(self.version_tag)

    def __lt__(self, other):
        if isinstance(other, Version):
            return self.version_tag < other.version_tag
        else:
            raise ValueError("{} is not a Version object".format(str(other)))

    def __gt__(self, other):
        if isinstance(other, Version):
            return self.version_tag > other.version_tag
        else:
            raise ValueError("{} is not a Version object".format(str(other)))

    def __eq__(self, other):
        if isinstance(other, Version):
            return self.version_tag == other.version_tag
        else:
            raise ValueError("{} is not a Version object".format(str(other)))

    def __ne__(self, other):
        if isinstance(other, Version):
            return self.version_tag != other.version_tag
        else:
            raise ValueError("{} is not a Version object".format(str(other)))
