# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from Components.Element import cached
from Components.Sources.ServiceEvent import ServiceEvent


class COCServiceEvent(ServiceEvent):
    def __init__(self, servicecenter):
        ServiceEvent.__init__(self)
        self.__servicecenter = servicecenter

    @cached
    def getInfo(self):
        return self.service and self.__servicecenter.info(self.service)

    info = property(getInfo)

    @cached
    def getCover(self):
        return self.service and self.__servicecenter.info(self.service).getCover()

    cover = property(getCover)
