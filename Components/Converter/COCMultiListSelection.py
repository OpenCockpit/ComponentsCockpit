# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from enigma import gPixmapPtr
from enigma import eListboxPythonMultiContent
from Components.Converter.Converter import Converter
from Components.Element import cached


class COCMultiListSelection(Converter):
    def __init__(self, argstr):
        Converter.__init__(self, argstr)
        self.content = None
        self.element_index = 0
        self.available = -1
        self._visible = 1
        args = argstr.split(',')
        if args[0].isdigit():
            self.element_index = int(args[0])
        if len(args) >= 2 and args[1].isdigit():
            self.available = int(args[1])
            if len(args) >= 3 and args[2].isdigit():
                self._visible = int(args[2])

    def selChanged(self):
        if self.source and self.master:
            cur = self.source.current
            if cur and not cur[self.element_index]:
                self.master.visible = 0
            elif cur and self.available >= 0:
                self.selAvailable(cur)
            else:
                self.master.visible = 1
            self.downstream_elements.changed((self.CHANGED_ALL, 0))

    def selAvailable(self, cur):
        if self.source:
            if cur and len(cur):
                if self.available <= len(cur):
                    value = 1
                    if self._visible == 0 and cur[self.available]:
                        value = 0
                    elif self._visible == 1 and not cur[self.available]:
                        value = 0
                    self.master.visible = value

    @cached
    def getCurrent(self):
        if self.master and self.element_index <= len(self.source.list):
            return self.source.list
        return None

    current = property(getCurrent)

    @cached
    def getText(self):
        cur = self.source.current
        if cur and self.element_index < len(cur):
            return cur[self.element_index]
        return None

    text = property(getText)

    @cached
    def getPixmap(self):
        cur = self.source.current
        if cur and self.element_index < len(cur):
            curindex = cur[self.element_index]
            if isinstance(curindex, gPixmapPtr):
                return curindex
        return gPixmapPtr()

    pixmap = property(getPixmap)

    @cached
    def getValue(self):
        cur = self.source.current
        if cur and self.element_index < len(cur):
            curindex = cur[self.element_index]
            if isinstance(curindex, int):
                return curindex
        return 0

    value = property(getValue)
    range = 100

    def changed(self, what):
        if what[0] == self.CHANGED_ALL and self.master is not None:
            if not self.content:
                self.content = eListboxPythonMultiContent()
            if self.source is not None:
                self.content.setList(self.source.list)
                self.selChanged()
            Converter.changed(self, what)
        elif what[0] == self.CHANGED_DEFAULT:
            if self.selChanged not in self.source.onSelectionChanged:
                self.source.onSelectionChanged.append(self.selChanged)
