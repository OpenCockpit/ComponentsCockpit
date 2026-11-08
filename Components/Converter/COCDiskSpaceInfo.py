# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from Components.Element import cached
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll


class COCDiskSpaceInfo(Poll, Converter):
    SPACEINFO = 0

    def __init__(self, atype):
        Converter.__init__(self, atype)
        Poll.__init__(self)

        self.type = self.SPACEINFO
        self.poll_interval = 2500
        self.poll_enabled = True

    @cached
    def getText(self):
        return self.source.space

    text = property(getText)
