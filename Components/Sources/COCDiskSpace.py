# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from Components.Element import cached
from Components.Sources.Source import Source


class COCDiskSpace(Source):
    def __init__(self, player):
        Source.__init__(self)
        self.__player = player

    @cached
    def getDiskSpace(self):
        return self.__player.getBookmarksSpaceInfo()

    space = property(getDiskSpace)
