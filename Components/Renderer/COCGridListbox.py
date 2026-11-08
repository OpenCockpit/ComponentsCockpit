from Components.ActionMap import ActionMap
from Components.Renderer.Listbox import Listbox

# A listbox for a grid (orientation orGrid) in which the left and right keys move through the items in reading
# order: right on the last item of a row selects the first item of the next row, left on the first item of a row
# selects the last item of the previous row, and the last/first item of the list wraps around (if wrap around is
# enabled, which it is unless the skin or the source says otherwise).
#
# eListbox moves left and right only within the current row (wrapping to the same row's other end). This renderer
# takes the two keys before the listbox sees them, the page keys are left to eListbox.
#
# Up and down move one row, in the same column (as eListbox does): on a last row that is shorter than the one above,
# down from a column that it does not have selects its last item; down from the last row and up from the first one
# wrap around to the other end of the same column (if wrap around is enabled), else the cursor stays. The renderer
# takes these keys too, and only while it has a selection (selection_enabled): with several grids on one screen the
# keys are for the grid that has the cursor, and the others do nothing with them (return 0 so that they go on).
#
# Use it in a skin like Listbox:
#   <widget source="list" render="GridListbox" ...>
#     <convert type="TemplatedMultiContent">{... "orientation": "orGrid", ...}</convert>
#   </widget>


class COCGridListbox(Listbox):
    def __init__(self):
        Listbox.__init__(self)
        # below the priority (0) of the listbox's own keys, a lower number is served first
        self.navigationActions = ActionMap(["NavigationActions", "DirectionActions"], {
            "left": self.keyLeft,
            "right": self.keyRight,
            "up": self.keyUp,
            "down": self.keyDown,
        }, -1)

    def execBegin(self):
        Listbox.execBegin(self)
        self.navigationActions.execBegin()

    def execEnd(self):
        self.navigationActions.execEnd()
        Listbox.execEnd(self)

    def keyLeft(self):
        return self.moveInReadingOrder(-1)

    def keyRight(self):
        return self.moveInReadingOrder(1)

    def keyUp(self):
        return self.moveInRows(-1)

    def keyDown(self):
        return self.moveInRows(1)

    def itemList(self):
        # The source of a renderer is its converter (TemplatedMultiContent), which has no list of its own: the list is
        # that of the data source behind it (Components.Sources.List), found by following the converters' sources.
        source = self.source
        while source is not None and not hasattr(source, "list"):
            source = getattr(source, "source", None)
        return source.list if source is not None else []

    def moveInReadingOrder(self, step):
        # returns 0 (key not handled) if there is nothing to move, so the key goes on to whoever else wants it
        if self.instance is None or not self.selection_enabled or self.source is None:
            return 0
        count = len(self.itemList())
        if count < 2:
            return 0
        index = self.index + step
        if not 0 <= index < count:
            if not self.wrap_around:
                return 1   # at the end of the list: stay, the key is used up
            index %= count
        self.moveToIndex(index)   # the setter of Listbox.index
        return 1

    def columns(self):
        # the number of columns the way eListbox makes it: the width of the widget divided by the width of an item
        itemWidth = self.content.getItemSize().width() if self.content is not None else 0
        return max(1, self.instance.size().width() // itemWidth) if itemWidth > 0 else 1

    def moveInRows(self, step):
        # one row up (-1) or down (1) in the same column; returns 0 (key not handled) if there is nothing to move
        if self.instance is None or not self.selection_enabled or self.source is None:
            return 0
        count = len(self.itemList())
        if count < 2:
            return 0
        columns = self.columns()
        current = self.index
        column = current % columns
        index = current + step * columns
        if index < 0:
            if not self.wrap_around:
                return 1   # in the first row: stay, the key is used up
            index = (count - 1) // columns * columns + column   # the same column of the last row
            if index >= count:
                index -= columns   # the last row does not have it: the row above
        elif index >= count:
            if current // columns < (count - 1) // columns:
                index = count - 1   # the last row is shorter: its last item
            elif not self.wrap_around:
                return 1   # in the last row: stay
            else:
                index = column   # the same column of the first row
        self.moveToIndex(index)   # the setter of Listbox.index
        return 1
