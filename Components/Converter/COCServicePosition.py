# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


import time
from enigma import iPlayableServicePtr
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached, ElementError


class COCServicePosition(Poll, Converter):

    TYPE_LENGTH = 0
    TYPE_REMAINING = 1
    TYPE_ENDTIME = 2
    TYPE_POSITION = 3

    def __init__(self, atype):
        Poll.__init__(self)
        Converter.__init__(self, atype)

        args = atype.split(',')
        ptype = args.pop(0)

        self.negate = 'Negate' in args
        self.detailed = 'Detailed' in args
        self.showHours = 'ShowHours' in args
        self.showNoSeconds = 'ShowNoSeconds' in args

        if ptype == "Length":
            self.type = self.TYPE_LENGTH
        elif ptype == "Position":
            self.type = self.TYPE_POSITION
        elif ptype == "Remaining":
            self.type = self.TYPE_REMAINING
        elif ptype == "EndTime":
            self.type = self.TYPE_ENDTIME
        else:
            raise ElementError("type must be {EndTime|Length|Position|Remaining} with optional arguments {Negate|Detailed|ShowHours|ShowNoSeconds} for ServicePosition converter")

        if self.detailed:
            self.poll_interval = 100
        elif self.type == self.TYPE_LENGTH:
            self.poll_interval = 2000
        else:
            self.poll_interval = 1000

        self.poll_enabled = True

    def getSeek(self):
        s = self.source.service
        if isinstance(s, iPlayableServicePtr):
            return s and s.seek()
        return None

    @cached
    def getCutlist(self):
        cutlist = []
        if self.source.service is not None:
            cut = self.source.service.cutList()
            if cut:
                cutlist = cut.getCutList()
        return cutlist

    cutlist = property(getCutlist)

    @cached
    def getLength(self):
        # Cockpit player screens provide source.player (a custom controller
        # with its own getLength()/getPosition()); other sources bound here
        # (e.g. stock session.CurrentService) don't, so fall back to the
        # standard seek() API - the same one getSeek()/getCutlist() already
        # use - instead of hard-requiring a Cockpit-specific source.
        if hasattr(self.source, "player"):
            return self.source.player.getLength()
        seek = self.getSeek()
        if seek is None:
            return None
        length = seek.getLength()
        if length[0]:
            return 0
        return length[1]

    length = property(getLength)

    @cached
    def getPosition(self):
        if hasattr(self.source, "player"):
            return self.source.player.getPosition()
        seek = self.getSeek()
        if seek is None:
            return None
        pos = seek.getPlayPosition()
        if pos[0]:
            return 0
        return pos[1]

    position = property(getPosition)

    @cached
    def getTime(self):
        length = self.getLength()
        return length / 90000 if length else 0

    time = property(getTime)

    @cached
    def getValue(self):
        pos = self.position
        if pos is None:
            return None
        return pos // 90000

    value = property(getValue)

    @cached
    def getRange(self):
        length = self.getLength()
        if length is None:
            return None
        return length // 90000

    range = property(getRange)

    def getEventTimes(self):
        # Length and position (90 kHz) of the current EPG event, for a live
        # service that has no seekable length of its own.
        service = self.source.service
        if isinstance(service, iPlayableServicePtr):
            info = service.info()
            event = info and info.getEvent(0)
            if event and event.getDuration() > 0:
                duration = event.getDuration()
                elapsed = max(0, min(int(time.time()) - event.getBeginTime(), duration))
                return duration * 90000, elapsed * 90000
        return None, None

    @cached
    def getText(self):
        text = ""
        pos = 0
        if self.getSeek() is not None and self.length:
            length, position = self.length, self.position
        else:
            length, position = self.getEventTimes()
        if length:
            if self.type == self.TYPE_ENDTIME:
                pos = (length - position) / 90000
                t = time.localtime(time.time() + pos)
                text = f"{t.tm_hour:02d}:{t.tm_min:02d}"
                if not self.showNoSeconds:
                    text += f":{t.tm_sec:02d}"
                if pos >= 0:
                    text = ">" + text
                else:
                    text = text + "<"
            else:
                if self.type == self.TYPE_LENGTH:
                    pos = length
                elif self.type == self.TYPE_POSITION:
                    pos = position
                elif self.type == self.TYPE_REMAINING:
                    pos = length - position

                pos = -pos if self.negate else pos
                if self.type == self.TYPE_LENGTH:
                    sign = ""
                else:
                    sign = "-" if pos < 0 else "+"

                pos = abs(pos)
                milliseconds = (pos % 90000) / 90
                pos /= 90000
                if self.showHours:
                    text += f"{sign}{int(pos / 3600)}"  # hours
                    text += f":{int(pos % 3600 / 60):02d}"  # minutes
                else:
                    text += f"{sign}{int(pos / 60)}"  # minutes
                if not self.showNoSeconds:
                    text += f":{int(pos % 60):02d}"  # seconds
                    if self.detailed:
                        text += f":{int(milliseconds):03d}"  # milliseconds
        return text

    text = property(getText)
