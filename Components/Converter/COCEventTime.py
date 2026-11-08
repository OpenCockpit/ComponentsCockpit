# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from time import time
from Components.Converter.Poll import Poll
from Components.Element import cached
from Components.Converter.Converter import Converter


class COCEventTime(Poll, Converter):
    """Elapsed/remaining time of the current EPG event, formatted like
    COCServicePosition (+h:mm:ss, a sign in front, optional Negate), for a
    live stream whose event - not the stream itself - defines the duration.

    Source: any ServiceEvent-like source (e.g. session.Event_Now).
    Types: Position (elapsed), Remaining. Options: Negate, ShowNoSeconds.
    """

    POSITION = 1
    REMAINING = 2

    def __init__(self, atype):
        Converter.__init__(self, atype)
        Poll.__init__(self)
        args = atype.split(",")
        atype = args.pop(0)
        self.negate = "Negate" in args
        self.showNoSeconds = "ShowNoSeconds" in args
        if atype == "Position":
            self.type = self.POSITION
        elif atype == "Remaining":
            self.type = self.REMAINING
        else:
            raise ValueError("COCEventTime: type must be {Position|Remaining} with optional arguments {Negate|ShowNoSeconds}")
        self.poll_interval = 1000
        self.poll_enabled = True

    @cached
    def getText(self):
        text = ""
        event = self.source.event
        if event:
            start_time = event.getBeginTime()
            duration = event.getDuration()
            now = int(time())
            if self.type == self.REMAINING:
                value = start_time + duration - now
            else:
                value = now - start_time
            value = max(0, min(value, duration))
            if self.negate:
                value = -value
            sign = "-" if value < 0 else "+"
            value = abs(value)
            text = f"{sign}{value // 3600}:{value % 3600 // 60:02d}"
            if not self.showNoSeconds:
                text += f":{value % 60:02d}"
        return text

    text = property(getText)
