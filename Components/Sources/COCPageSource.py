# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from Components.Sources.Source import Source


class COCPageSource(Source):
    """The page numbers of a list that the plugin pages itself (the pages of a web service, not the rows that fit the
    list). A screen has one as an element, the plugin tells it the pages with setPages(), and a COCPager connected to it
    shows them. Pages count from 1, like the numbers the user sees."""

    def __init__(self):
        Source.__init__(self)
        self.currentPage = 1
        self.pageCount = 0
        self.onSelectionChanged = []  # the Pager adds itself here, as it does for a list

    def setPages(self, currentPage, pageCount):
        self.currentPage = currentPage
        self.pageCount = pageCount
        for callback in self.onSelectionChanged[:]:
            callback()
