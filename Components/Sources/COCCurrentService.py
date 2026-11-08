# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from enigma import eServiceReference, iServiceInformation
from Components.Element import cached
from Components.Sources.CurrentService import CurrentService
from Components.Sources.Event import Event


class COCCurrentService(CurrentService, Event):
    def __init__(self, navcore, player):
        CurrentService.__init__(self, navcore)
        Event.__init__(self)
        self.__player = player

    def cueSheet(self):
        return self.__player

    @cached
    def getInfo(self):
        return self.service and self.__player.getInfo()

    def setInfo(self, value):
        pass  # Dummy setter for OpenVix compatibility

    info = property(getInfo, setInfo)

    @cached
    def getEvent(self):
        return self.service and self.__player.getEvent()

    def setEvent(self, value):
        pass  # Dummy setter for OpenVix compatibility

    event = property(getEvent, setEvent)

    @cached
    def getCurrentService(self):
        service = self.navcore.getCurrentService()
        if service is not None:
            service.cutList = self.cueSheet
        return service

    def setCurrentService(self, value):
        pass  # Dummy setter for OpenVix compatibility

    service = property(getCurrentService, setCurrentService)

    @cached
    def getCurrentPlayer(self):
        return self.__player

    def setCurrentPlayer(self, value):
        pass  # Dummy setter for OpenVix compatibility

    player = property(getCurrentPlayer, setCurrentPlayer)

    @cached
    def getServiceRef(self):
        if hasattr(self.__player, "getInfo"):
            info = self.__player.getInfo()
            if info:
                ref_str = info.getInfoString(None, iServiceInformation.sServiceref)
                if ref_str:
                    return eServiceReference(ref_str)
        return None

    def setServiceRef(self, value):
        pass  # Dummy setter for OpenVix compatibility

    serviceref = property(getServiceRef, setServiceRef)
