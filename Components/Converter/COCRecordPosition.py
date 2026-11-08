# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from Components.Converter.ServicePosition import ServicePosition
from Components.Element import cached


class COCRecordPosition(ServicePosition):
    def __init__(self, atype):
        ServicePosition.__init__(self, atype)
        self.poll_interval = 1000

    @cached
    def getCutlist(self):
        return []

    cutlist = property(getCutlist)

    @cached
    def getPosition(self):
        return self.source.player.getRecordingPosition()

    position = property(getPosition)

    @cached
    def getLength(self):
        return self.source.player.getLength()

    length = property(getLength)
