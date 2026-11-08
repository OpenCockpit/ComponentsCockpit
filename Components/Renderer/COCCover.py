# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


import io
import os
import struct
import tempfile
from enigma import ePixmap, gPixmapPtr, ePicLoad, ePoint, eSize
from Components.Renderer.Renderer import Renderer
from Components.AVSwitch import AVSwitch

PNG_SIGNATURE = bytes([0x89]) + b"PNG" + bytes([0x0D, 0x0A, 0x1A, 0x0A])
JPEG_SOI = bytes([0xFF, 0xD8])
JPEG_NO_SIZE_MARKERS = (0xC4, 0xC8, 0xCC)  # inside the SOF range, but not frame headers


def getImageSize(data):
    """(width, height) of a JPEG or PNG picture, read from its header, or None. ePicLoad only reports the size of a
    picture after decoding it, and by then it has padded it to the box it was asked for."""
    try:
        f = io.BytesIO(data)
        head = f.read(24)
        if head.startswith(PNG_SIGNATURE):
            return struct.unpack(">II", head[16:24])
        if not head.startswith(JPEG_SOI):
            return None
        f.seek(2)
        while True:
            byte = f.read(1)
            if not byte:
                return None
            if byte[0] != 0xFF:
                continue
            marker = f.read(1)
            while marker and marker[0] == 0xFF:  # fill bytes
                marker = f.read(1)
            if not marker:
                return None
            code = marker[0]
            if code == 0x01 or 0xD0 <= code <= 0xD8 or code == 0x00:  # no length field
                continue
            length = struct.unpack(">H", f.read(2))[0]
            if 0xC0 <= code <= 0xCF and code not in JPEG_NO_SIZE_MARKERS:
                _precision, height, width = struct.unpack(">BHH", f.read(5))
                return width, height
            f.seek(length - 2, 1)
    except (struct.error, IndexError):
        return None


class COCCover(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        self.skinAttributes = None
        Renderer.__init__(self)
        self.backgroundColor = "#00000000"
        self.picload = None
        self.tmp_cover_path = None
        self.box = None  # (x, y, width, height) the skin gave the widget

    def destroy(self):
        self.removeTmpCover()
        Renderer.destroy(self)

    def removeTmpCover(self):
        if self.tmp_cover_path:
            try:
                os.unlink(self.tmp_cover_path)
            except OSError:
                pass
            self.tmp_cover_path = None

    def applySkin(self, desktop, parent):
        if self.skinAttributes:
            for (attrib, value) in self.skinAttributes:
                if attrib == "backgroundColor":
                    self.backgroundColor = value
        return Renderer.applySkin(self, desktop, parent)

    def getBox(self):
        """The area the skin gave the widget. Remembered on first use, because fitWidget() resizes the widget itself."""
        if self.box is None:
            self.box = (self.instance.position().x(), self.instance.position().y(),
                        self.instance.size().width(), self.instance.size().height())
        return self.box

    def fitWidget(self, data):
        """The cover is scaled into the widget keeping its aspect ratio, so it is usually smaller than the widget and
        the widget's rounded corners (cornerRadius) would sit on the empty part of the box instead of on the cover.
        The widget is shrunk to the size of the scaled cover, centered in the skin's box, to put them on it."""
        box_x, box_y, box_w, box_h = self.getBox()
        width, height = box_w, box_h
        dimensions = getImageSize(data) if data else None
        if dimensions and dimensions[0] > 0 and dimensions[1] > 0:
            factor = min(box_w / dimensions[0], box_h / dimensions[1])
            width = max(1, int(dimensions[0] * factor))
            height = max(1, int(dimensions[1] * factor))
        self.instance.move(ePoint(box_x + (box_w - width) // 2, box_y + (box_h - height) // 2))
        self.instance.resize(eSize(width, height))

    def changed(self, what):
        if self.instance is not None:
            if what[0] != self.CHANGED_CLEAR:
                if self.source.cover:
                    # the previous decode is abandoned below (its ePicLoad is replaced,
                    # so its callback never fires): drop its temp file now, not never
                    self.removeTmpCover()
                    scale = AVSwitch().getFramebufferScale()
                    self.fitWidget(self.source.cover)
                    size = self.instance.size()
                    self.picload = ePicLoad()
                    self.picload.PictureData.get().append(self.displayPixmapCallback)
                    self.picload.setPara(
                        (size.width(), size.height(), scale[0], scale[1], True, 1, self.backgroundColor))
                    # OpenVix doesn't have startDecodeBuffer, use temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(self.source.cover)
                        tmp_path = tmp.name
                    self.picload.startDecode(tmp_path)
                    # Clean up temp file after a delay (will be done in callback)
                    self.tmp_cover_path = tmp_path
                else:
                    self.instance.setPixmap(gPixmapPtr())
            else:
                self.instance.setPixmap(gPixmapPtr())

    def displayPixmapCallback(self, picinfo=None):
        if self.picload and picinfo:
            self.instance.setPixmap(self.picload.getData())
        self.removeTmpCover()
