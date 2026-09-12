import sys, io, json, textwrap, datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from PySide6.QtCore import Qt, QUrl, QSize, QPoint, QRect, Signal
from PySide6.QtGui import QPixmap, QImage, QFont, QDesktopServices, QPainter, QPen, QColor, QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QSpinBox, QLineEdit, QTextEdit,
    QFileDialog, QMessageBox, QFrame, QListWidget, QListWidgetItem,
    QSplitter, QCheckBox, QGroupBox, QScrollArea, QSlider, QListWidget, QListWidgetItem, QAbstractItemView
)

APP_NAME = "JASS GURBANI STUDIO"

THEMES = {
    "Royal": {
        "gradient": ((255, 250, 235), (224, 233, 255)),
        "accent": (212, 175, 55),
        "gurbani_color": (20, 20, 20),
        "latin_color": (55, 55, 55),
        "glow": (255, 255, 255),
    },
    "Saffron": {
        "gradient": ((255, 248, 231), (255, 223, 164)),
        "accent": (230, 140, 0),
        "gurbani_color": (35, 25, 15),
        "latin_color": (70, 50, 30),
        "glow": (255, 250, 220),
    },
    "Midnight": {
        "gradient": ((25, 30, 52), (5, 7, 16)),
        "accent": (230, 220, 200),
        "gurbani_color": (248, 248, 248),
        "latin_color": (220, 220, 220),
        "glow": (80, 90, 130),
    },
    "Amrit": {
        "gradient": ((235, 250, 247), (190, 225, 219)),
        "accent": (24, 110, 92),
        "gurbani_color": (20, 45, 42),
        "latin_color": (45, 75, 70),
        "glow": (245, 255, 250),
    },
}


STYLESHEET = """
QMainWindow, QWidget {
    background:#09111f;
    color:#e9eef7;
    font-family:"Segoe UI";
    font-size:13px;
}
QWidget#sidebar {
    background:#0c1526;
    border-right:1px solid #1e3048;
}
QFrame#sidebar {
    background:#0c1526;
    border-right:1px solid #1e3048;
}
QLabel#brand {
    color:#ffffff;
    font-size:24px;
    font-weight:800;
    letter-spacing:0px;
    padding:2px 0;
}
QLabel#eyebrow {
    color:#c8a94b;
    font-size:10px;
    font-weight:800;
    letter-spacing:2px;
    padding:2px 0;
}
QLabel#title {
    color:#f8fafc;
    font-size:29px;
    font-weight:800;
}
QLabel#subtitle_header {
    color:#7f91aa;
    font-size:12px;
}
QLabel#muted {
    color:#7f91aa;
}
QLabel#section {
    color:#d7dfeb;
    font-size:14px;
    font-weight:750;
}
QPushButton {
    min-height:34px;
}
QPushButton#nav {
    text-align:left;
    padding:13px 16px;
    border:1px solid transparent;
    border-radius:10px;
    color:#91a2ba;
    background:transparent;
    font-size:14px;
    font-weight:500;
}
QPushButton#nav:hover {
    background:#132239;
    color:#edf3fb;
    border:1px solid #1d3655;
}
QPushButton#nav:checked {
    background:#2558d9;
    color:white;
    font-weight:700;
    border:1px solid #3970ef;
}
QPushButton#primary {
    background:#2563eb;
    color:white;
    border:1px solid #4b82f4;
    border-radius:10px;
    padding:10px 17px;
    font-weight:750;
}
QPushButton#primary:hover {
    background:#3474ef;
}
QPushButton#primary:pressed {
    background:#1e54c9;
}
QPushButton#secondary {
    background:#111d30;
    color:#cbd6e5;
    border:1px solid #2a3d59;
    border-radius:10px;
    padding:9px 15px;
}
QPushButton#secondary:hover {
    background:#172941;
    color:white;
    border-color:#3a5272;
}
QPushButton#secondary:pressed {
    background:#0e1929;
}
QLineEdit, QComboBox, QSpinBox, QTextEdit {
    background:#101d31;
    color:#f4f7fb;
    border:1px solid #293d5b;
    border-radius:10px;
    padding:9px 11px;
    selection-background-color:#285bd6;
    selection-color:white;
}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover, QTextEdit:hover {
    border-color:#3b5272;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
    border:1px solid #4c78db;
    background:#112138;
}
QTextEdit {
    padding:13px;
    font-size:15px;
}
QComboBox::drop-down {
    width:28px;
    border:0;
}
QSpinBox::up-button, QSpinBox::down-button {
    width:20px;
    border:0;
}
QSlider::groove:horizontal {
    height:5px;
    background:#22334d;
    border-radius:3px;
}
QSlider::sub-page:horizontal {
    background:#3973ea;
    border-radius:3px;
}
QSlider::handle:horizontal {
    width:15px;
    margin:-5px 0;
    background:#d9e4f5;
    border:2px solid #3973ea;
    border-radius:8px;
}
QGroupBox {
    background:#0d1728;
    border:1px solid #21344e;
    border-radius:14px;
    margin-top:13px;
    padding:17px 14px 13px 14px;
    font-weight:700;
}
QGroupBox::title {
    subcontrol-origin:margin;
    left:14px;
    padding:0 7px;
    color:#dbe4ef;
    background:#0d1728;
}
QListWidget {
    background:#0a1424;
    border:1px solid #243852;
    border-radius:11px;
    padding:5px;
    outline:0;
}
QListWidget::item {
    padding:9px 10px;
    margin:2px 0;
    border-radius:8px;
    color:#cbd6e5;
}
QListWidget::item:hover {
    background:#14243a;
}
QListWidget::item:selected {
    background:#2558d9;
    color:white;
}
QCheckBox {
    color:#b9c7d9;
    spacing:8px;
}
QCheckBox::indicator {
    width:15px;
    height:15px;
    border-radius:4px;
    border:1px solid #3a4e69;
    background:#101d31;
}
QCheckBox::indicator:checked {
    background:#2f67e4;
    border-color:#4a7df0;
}
QScrollBar:vertical {
    background:#0b1524;
    width:10px;
    margin:3px;
}
QScrollBar::handle:vertical {
    background:#30445f;
    min-height:35px;
    border-radius:5px;
}
QScrollBar::handle:vertical:hover {
    background:#426081;
}
QScrollBar::add-line, QScrollBar::sub-line {
    height:0;
}
QFrame#previewCard {
    background:#070e19;
    border:1px solid #263b58;
    border-radius:16px;
}
QFrame#previewSurface {
    background:#050a12;
    border:1px solid #1d3048;
    border-radius:12px;
}
QLabel#previewTitle {
    color:#c8a94b;
    font-size:10px;
    font-weight:800;
    letter-spacing:2px;
    padding:3px 5px;
}
QLabel#hint {
    color:#7487a1;
    background:#0b1423;
    border:1px solid #1a2b42;
    border-radius:8px;
    padding:7px 10px;
}
"""

def lerp(a, b, t):
    return a + (b - a) * t

def gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    p = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(lerp(top[i], bottom[i], t)) for i in range(3))
        for x in range(w):
            p[x, y] = c
    return img

def soft_glow(img, color, strength=0.18):
    w, h = img.size
    glow = Image.new("RGBA", (w, h), (*color, 0))
    d = ImageDraw.Draw(glow)
    r = int(min(w, h) * 0.28)
    d.ellipse((w//2-r, h//2-r, w//2+r, h//2+r), fill=(*color, int(255*strength)))
    glow = glow.filter(ImageFilter.GaussianBlur(int(min(w,h)*0.12)))
    return Image.alpha_composite(img.convert("RGBA"), glow)

def vignette(img):
    w, h = img.size
    overlay = Image.new("RGBA", (w,h), (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    d.rectangle((0,0,w,h), fill=(0,0,0,80))
    inner = Image.new("L",(w,h),0)
    di = ImageDraw.Draw(inner)
    di.ellipse((int(w*.06),int(h*.04),int(w*.94),int(h*.96)), fill=255)
    inner = inner.filter(ImageFilter.GaussianBlur(int(min(w,h)*.09)))
    alpha = Image.eval(inner, lambda x: 80-x)
    overlay.putalpha(alpha)
    return Image.alpha_composite(img.convert("RGBA"), overlay)

def font_or_fallback(path, size):
    candidates = []
    if path:
        candidates.append(Path(path))
    candidates += [
        Path("C:/Windows/Fonts/Nirmala.ttf"),
        Path("C:/Windows/Fonts/NirmalaUI.ttf"),
        Path("C:/Windows/Fonts/Raavi.ttf"),
        Path("C:/Windows/Fonts/Gadugi.ttf"),
        Path("/usr/share/fonts/truetype/noto/NotoSansGurmukhi-Regular.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansGurmukhi-Regular.ttf"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()

def latin_font(size):
    for p in [
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def qt_gurmukhi_font(size, preferred_path=""):
    """Return a Qt font with reliable Gurmukhi/Indic shaping."""
    preferred = []
    if preferred_path:
        preferred.append(Path(preferred_path))
    preferred += [
        Path("C:/Windows/Fonts/NirmalaUI.ttf"),
        Path("C:/Windows/Fonts/Nirmala.ttf"),
        Path("C:/Windows/Fonts/Raavi.ttf"),
        Path("C:/Windows/Fonts/Gadugi.ttf"),
    ]
    for p in preferred:
        if p.exists():
            fid = QFontDatabase.addApplicationFont(str(p))
            if fid >= 0:
                families = QFontDatabase.applicationFontFamilies(fid)
                if families:
                    f = QFont(families[0], size)
                    f.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
                    return f
    for family in QFontDatabase.families():
        low = family.lower()
        if any(x in low for x in ("nirmala", "raavi", "gurmukhi")):
            f = QFont(family, size)
            f.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
            return f
    f = QFont("Nirmala UI", size)
    f.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
    return f

def qt_draw_centered(painter, text, font, rect, color, shadow=True):
    painter.setFont(font)
    fm = painter.fontMetrics()
    br = fm.boundingRect(rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)
    x = rect.x()
    y = rect.y() + (rect.height() - br.height()) // 2
    if shadow:
        painter.setPen(QColor(0, 0, 0, 90))
        painter.drawText(x + 2, y + 2, rect.width(), br.height(),
                         Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)
    painter.setPen(QColor(*color))
    painter.drawText(x, y, rect.width(), br.height(),
                     Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)

def wrap_gurmukhi(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]

def draw_centered(draw, lines, font, center_x, y, color, line_gap=1.25, shadow=True):
    step = int(font.size * line_gap)
    for line in lines:
        width = draw.textlength(line, font=font)
        x = center_x - width/2
        if shadow:
            draw.text((x+2,y+2), line, font=font, fill=(0,0,0,100))
        draw.text((x,y), line, font=font, fill=color)
        y += step

def ornate_frame(img, accent, width):
    out = ImageOps.expand(img, border=width, fill=accent)
    out = ImageOps.expand(out, border=3, fill=(255,255,255))
    out = ImageOps.expand(out, border=max(2,width//2), fill=accent)
    return out

def render_image(item, cfg):
    W, H = cfg["size"]
    theme = THEMES[cfg["theme"]]
    gurbani = (item.get("line") or "").strip()
    img = gradient((W, H), *theme["gradient"])
    img = soft_glow(img, theme["glow"], .12)
    img = vignette(img)

    # Draw the background/decorations with PIL, then use Qt's text engine
    # for Gurmukhi. This avoids the square-glyph problem caused by fonts that
    # PIL cannot shape/render correctly for Indic scripts.
    d = ImageDraw.Draw(img)
    pad = cfg["padding"]
    title = str(item.get("title", "")).strip()
    subtitle = str(item.get("subtitle", "")).strip()
    line = str(item.get("line", "")).strip()
    if not line:
        return None

    cx = W // 2
    d.ellipse((cx-7, pad-7, cx+7, pad+7), fill=theme["accent"])
    d.line((cx-80, pad, cx+80, pad), fill=theme["accent"], width=2)

    # Header is deliberately laid out as two separate rows so title and
    # subtitle never collide when using large Gurmukhi fonts.
    y = pad + 8
    if title:
        tf = qt_gurmukhi_font(cfg["title_size"], cfg["font_gurmukhi"])
        y += max(34, cfg["title_size"]) + 8
    if subtitle:
        sf = latin_font(cfg["subtitle_size"])
        sw = d.textlength(subtitle, font=sf)
        d.text(((W-sw)/2, y), subtitle, font=sf, fill=theme["latin_color"])
        y += sf.size * 1.8
    else:
        y += 10

    available_h = int(H * .58)
    max_w = W - 2 * pad

    # Use a Qt image for proper Gurmukhi shaping and line wrapping.
    qimg = QImage(W, H, QImage.Format.Format_ARGB32)
    qimg.fill(QColor(0, 0, 0, 0))
    painter = QPainter(qimg)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

    # Title: use Qt, not PIL.
    if title:
        tf = qt_gurmukhi_font(cfg["title_size"], cfg["font_gurmukhi"])
        painter.setFont(tf)
        painter.setPen(QColor(*theme["gurbani_color"]))
        title_h = int(tf.pointSize() * 1.8)
        painter.drawText(0, pad + 6, W, title_h,
                         Qt.AlignmentFlag.AlignCenter, title)
        y = pad + title_h + 12

    # Composition layers.
    layers=cfg.get("layers") or []
    if not layers:
        layers=[{"name":"Gurbani","kind":"text","text":gurbani,"visible":True,"x":.5,"y":.5,
                 "width":.86,"height":.34,"size":cfg["gurbani_size"],"rotation":0,"opacity":1}]
    for l in layers:
        if not l.get("visible",True) or not str(l.get("text","")).strip(): continue
        textv=str(l["text"]).strip()
        cx=int(W*float(l.get("x",.5))); cy=int(H*float(l.get("y",.5)))
        bw=max(30,int(W*float(l.get("width",.8)))); bh=max(25,int(H*float(l.get("height",.2))))
        fs=max(12,int(l.get("size",48)))
        painter.save(); painter.setOpacity(float(l.get("opacity",1)))
        painter.translate(cx,cy); painter.rotate(float(l.get("rotation",0)))
        font=qt_gurmukhi_font(fs,cfg["font_gurmukhi"]) if l.get("name")=="Gurbani" else QFont(cfg.get("font_latin","Segoe UI"),fs)
        painter.setFont(font)
        painter.setPen(QColor(*theme["gurbani_color"]) if l.get("name")=="Gurbani" else QColor(*theme["latin_color"]))
        align_name = str(cfg.get("alignment", "Center"))
        align_flag = Qt.AlignmentFlag.AlignCenter
        if align_name == "Left":
            align_flag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        elif align_name == "Right":
            align_flag = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        painter.drawText(-bw//2,-bh//2,bw,bh,align_flag|Qt.TextFlag.TextWordWrap,textv)
        painter.restore()

    # Decorative divider.
    divider_y = H - int(pad * .95)
    painter.setPen(QColor(*theme["accent"]))
    painter.drawLine(pad, divider_y, W-pad, divider_y)

    meta = cfg["watermark"].strip()
    source = str(cfg.get("source","") or "").strip()
    # Legacy footer is used only when the project has no explicit layers.
    # This prevents a duplicate Watermark layer from appearing in the artwork.
    if not layers:
        if source:
            sf = QFont("Segoe UI", max(16, cfg["watermark_size"]-2))
            painter.setFont(sf)
            painter.setPen(QColor(*theme["latin_color"]))
            painter.drawText(0, divider_y + 8, W, sf.pointSize()+8,
                             Qt.AlignmentFlag.AlignCenter, source)
            if meta:
                mf = QFont("Segoe UI", cfg["watermark_size"])
                painter.setFont(mf)
                painter.setPen(QColor(*theme["latin_color"]))
                painter.drawText(0, divider_y + sf.pointSize() + 12, W, mf.pointSize()+8,
                                 Qt.AlignmentFlag.AlignCenter, meta)
        elif meta:
            mf = QFont("Segoe UI", cfg["watermark_size"])
            painter.setFont(mf)
            painter.setPen(QColor(*theme["latin_color"]))
            painter.drawText(0, divider_y + 10, W, mf.pointSize() + 10,
                             Qt.AlignmentFlag.AlignCenter, meta)

    painter.end()

    # Composite Qt text over the PIL background.
    text_pil = Image.fromqimage(qimg).convert("RGBA")
    img = Image.alpha_composite(img.convert("RGBA"), text_pil).convert("RGB")

    if cfg["frame"]:
        img = ornate_frame(img, theme["accent"], max(5, int(min(W, H) * .008)))
    return img

def parse_json(data):
    if isinstance(data, dict) and isinstance(data.get("text"), dict):
        title=data.get("originalTitle","")
        subtitle=data.get("englishTitle","")
        out=[]
        for v in data["text"].values():
            if str(v).strip() and not str(v).strip().startswith("#"):
                out.append({"line":v,"title":title,"subtitle":subtitle})
        return out
    if isinstance(data,list):
        return data
    if isinstance(data,dict):
        for k in ("items","data","shabads","lines"):
            if isinstance(data.get(k),list):
                return data[k]
    return []

def qimage_from_pil(img):
    # QImage initially references the PIL-owned byte buffer. copy() makes the
    # returned image fully independent before QPainter uses it.
    data=img.tobytes("raw","RGB")
    q=QImage(data,img.width,img.height,img.width*3,QImage.Format.Format_RGB888)
    return q.copy()

class Layer:
    def __init__(self,name,kind="text",text="",visible=True,locked=False,
                 x=.50,y=.50,width=.80,height=.20,size=48,rotation=0,opacity=1.0):
        self.name=name; self.kind=kind; self.text=text
        self.visible=visible; self.locked=locked
        self.x=x; self.y=y; self.width=width; self.height=height
        self.size=size; self.rotation=rotation; self.opacity=opacity


class GurbaniCanvas(QWidget):
    layerSelected=Signal(int)
    layerChanged=Signal(int)
    textResized=Signal(int)
    textMoved=Signal(int)

    def __init__(self):
        super().__init__()
        self.image=None; self.layers=[]; self.selected=-1
        self.dragging=False; self.resizing=False; self.rotating=False
        self.last_pos=QPoint()
        self.setMouseTracking(True)

    def set_image(self,image):
        self.image=image; self.update()

    def set_layers(self,layers):
        self.layers=layers
        if layers:
            self.selected=max(0,min(self.selected,len(layers)-1))
        else: self.selected=-1
        self.update()

    def _display_rect(self):
        if self.image is None: return QRect()
        iw,ih=self.image.size
        area=self.rect().adjusted(10,10,-10,-10)
        scale=min(area.width()/iw,area.height()/ih)
        w,h=max(1,int(iw*scale)),max(1,int(ih*scale))
        return QRect(area.center().x()-w//2,area.center().y()-h//2,w,h)

    def _rect(self,l):
        r=self._display_rect()
        if r.isNull(): return QRect()
        w=max(35,int(l.width*r.width())); h=max(25,int(l.height*r.height()))
        cx=r.left()+int(l.x*r.width()); cy=r.top()+int(l.y*r.height())
        return QRect(cx-w//2,cy-h//2,w,h)

    def _handle(self,l):
        q=self._rect(l); s=11
        return QRect(q.right()-s,q.bottom()-s,2*s,2*s)

    def _rotate(self,l):
        q=self._rect(l); s=10
        return QRect(q.center().x()-s,q.top()-30-s,2*s,2*s)

    def paintEvent(self,event):
        # Always close the widget painter, even if a paint operation raises.
        # This prevents QBackingStore::endPaint() / active-painter errors.
        p=QPainter()
        if not p.begin(self):
            return
        try:
            p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            p.fillRect(self.rect(), QColor("#070c15"))

            if self.image is not None:
                display = self._display_rect()
                if not display.isNull():
                    p.drawImage(display, qimage_from_pil(self.image))

            # The rendered image already contains all text layers. The canvas
            # therefore draws only selection geometry here.
            for i,l in enumerate(self.layers):
                if not l.visible or not str(l.text).strip():
                    continue
                q=self._rect(l)
                if i==self.selected:
                    p.save()
                    try:
                        p.setPen(QPen(QColor(55,140,255,220),2,Qt.PenStyle.DashLine))
                        p.setBrush(Qt.BrushStyle.NoBrush)
                        p.drawRoundedRect(q,7,7)

                        p.setPen(QPen(Qt.PenStyle.NoPen))
                        p.setBrush(QColor(55,140,255))
                        p.drawEllipse(self._handle(l))

                        p.setBrush(QColor(245,170,55))
                        p.drawEllipse(self._rotate(l))
                    finally:
                        p.restore()
        finally:
            if p.isActive():
                p.end()

    def _hit(self,pos):
        for i in range(len(self.layers)-1,-1,-1):
            if self.layers[i].visible and self._rect(self.layers[i]).contains(pos): return i
        return -1

    def mousePressEvent(self,e):
        if e.button()!=Qt.MouseButton.LeftButton: return
        pos=e.position().toPoint()
        if 0<=self.selected<len(self.layers):
            l=self.layers[self.selected]
            if not l.locked and self._handle(l).contains(pos):
                self.resizing=True; self.last_pos=pos; return
            if not l.locked and self._rotate(l).contains(pos):
                self.rotating=True; self.last_pos=pos; return
        hit=self._hit(pos)
        if hit>=0:
            self.selected=hit; self.layerSelected.emit(hit)
            if not self.layers[hit].locked:
                self.dragging=True; self.last_pos=pos
            self.update()

    def mouseMoveEvent(self,e):
        if not (0<=self.selected<len(self.layers)): return
        l=self.layers[self.selected]; pos=e.position().toPoint(); r=self._display_rect()
        if r.isNull(): return
        if self.resizing and not l.locked:
            dx=pos.x()-self.last_pos.x(); dy=pos.y()-self.last_pos.y()
            l.width=max(.08,min(1.0,l.width+dx/r.width()))
            l.height=max(.05,min(.80,l.height+dy/r.height()))
            if l.kind=="text":
                l.size=max(16,min(180,int(l.size+(dx+dy)/8)))
                self.textResized.emit(l.size)
            self.last_pos=pos; self.layerChanged.emit(self.selected); self.update(); return
        if self.rotating and not l.locked:
            import math
            c=self._rect(l).center()
            a1=math.degrees(math.atan2(self.last_pos.y()-c.y(),self.last_pos.x()-c.x()))
            a2=math.degrees(math.atan2(pos.y()-c.y(),pos.x()-c.x()))
            l.rotation=max(-180,min(180,l.rotation+a2-a1))
            self.last_pos=pos; self.layerChanged.emit(self.selected); self.update(); return
        if self.dragging and not l.locked:
            l.x=max(.03,min(.97,l.x+(pos.x()-self.last_pos.x())/r.width()))
            l.y=max(.03,min(.97,l.y+(pos.y()-self.last_pos.y())/r.height()))
            self.last_pos=pos; self.layerChanged.emit(self.selected); self.textMoved.emit(self.selected); self.update()

    def mouseReleaseEvent(self,e):
        self.dragging=self.resizing=self.rotating=False



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.items=[]
        self.current=0
        self.font_path=""
        self.background_path=""
        self.layers=[
            Layer("Gurbani","text","",True,False,.50,.50,.84,.34,72),
            Layer("Translation","text","",True,False,.50,.73,.78,.13,28),
            Layer("Source / Ang","text","",True,False,.50,.84,.70,.08,20),
            Layer("Watermark","text","JASS GURBANI",True,False,.84,.94,.30,.06,18),
        ]
        self.text_x=0.50
        self.text_y=0.50
        self.text_size=72
        self.setWindowTitle(APP_NAME)
        self.resize(1500,900)
        self.setMinimumSize(1250,760)
        self.build_ui()
        self.new_sample()
        self.text_size = self.gsize.value()

    def build_ui(self):
        root=QWidget(); self.setCentralWidget(root)
        main=QHBoxLayout(root); main.setContentsMargins(0,0,0,0); main.setSpacing(0)

        side=QFrame(); side.setObjectName("sidebar"); side.setFixedWidth(255)
        sl=QVBoxLayout(side); sl.setContentsMargins(18,25,18,18); sl.setSpacing(7)
        brand=QLabel(APP_NAME); brand.setObjectName("brand"); brand.setWordWrap(True); sl.addWidget(brand)
        e=QLabel("GURBANI VISUAL CREATOR"); e.setObjectName("eyebrow"); sl.addWidget(e); sl.addSpacing(25)

        self.nav=[]
        for text in ["⌂  Creator","▣  Library","✦  Themes","⚙  Settings"]:
            b=QPushButton(text); b.setObjectName("nav"); b.setCheckable(True)
            b.clicked.connect(lambda _,i=len(self.nav): self.switch_page(i))
            self.nav.append(b); sl.addWidget(b)
        sl.addStretch()
        q=QLabel("Create respectful Gurbani\nvisuals for personal use.\n\nPNG • JSON • Batch")
        q.setObjectName("muted"); q.setWordWrap(True); sl.addWidget(q)
        main.addWidget(side)

        content=QWidget(); cl=QVBoxLayout(content); cl.setContentsMargins(28,24,28,24); cl.setSpacing(16); main.addWidget(content,1)
        head=QHBoxLayout()
        title=QLabel("Gurbani Creator"); title.setObjectName("title"); head.addWidget(title)
        head_desc=QLabel("Compose • Preview • Export"); head_desc.setObjectName("subtitle_header")
        head_desc.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        head.addWidget(head_desc); head.addStretch()
        imp=QPushButton("Import JSON"); imp.setObjectName("secondary"); imp.clicked.connect(self.import_json); head.addWidget(imp)
        openp=QPushButton("Open Project"); openp.setObjectName("secondary"); openp.clicked.connect(self.open_project); head.addWidget(openp)
        savep=QPushButton("Save Project"); savep.setObjectName("secondary"); savep.clicked.connect(self.save_project); head.addWidget(savep)
        save=QPushButton("Render & Save"); save.setObjectName("primary"); save.clicked.connect(self.save_current); head.addWidget(save)
        batch=QPushButton("Batch Export"); batch.setObjectName("secondary"); batch.clicked.connect(self.batch_export); head.addWidget(batch)
        cl.addLayout(head)

        self.stack=QStackedWidgetCompat()
        cl.addWidget(self.stack,1)
        self.make_creator(); self.make_library(); self.make_themes(); self.make_settings()
        self.switch_page(0)

    def make_creator(self):
        page=QWidget(); layout=QHBoxLayout(page); layout.setContentsMargins(2,2,2,2); layout.setSpacing(20)
        left=QFrame(); left.setObjectName("editorColumn"); ll=QVBoxLayout(left); ll.setContentsMargins(0,0,0,0); ll.setSpacing(10)
        g=QGroupBox("Gurbani")
        gl=QVBoxLayout(g)
        self.text=QTextEdit(); self.text.setPlaceholderText("Enter Gurbani line here…"); self.text.setMinimumHeight(150)
        self.text.textChanged.connect(self.preview)
        gl.addWidget(self.text)
        row=QHBoxLayout()
        self.title_edit=QLineEdit("ੴ"); self.subtitle_edit=QLineEdit("Gurbani")
        row.addWidget(QLabel("Title")); row.addWidget(self.title_edit,1); row.addWidget(QLabel("Subtitle")); row.addWidget(self.subtitle_edit,1)
        gl.addLayout(row)
        row2=QHBoxLayout()
        self.source_edit=QLineEdit(); self.source_edit.setPlaceholderText("Source / Ang e.g. Ang 123")
        row2.addWidget(QLabel("Source")); row2.addWidget(self.source_edit,1)
        gl.addLayout(row2)
        row3=QHBoxLayout()
        self.translation_edit=QLineEdit(); self.translation_edit.setPlaceholderText("English translation (optional)")
        row3.addWidget(QLabel("Translation")); row3.addWidget(self.translation_edit,1)
        gl.addLayout(row3); ll.addWidget(g)

        layers_box=QGroupBox("Layers")
        layers_layout=QVBoxLayout(layers_box)
        self.layer_list=QListWidget()
        self.layer_list.currentRowChanged.connect(self.layer_selected)
        layers_layout.addWidget(self.layer_list)
        rowL=QHBoxLayout()
        for label,fn in [("+ Text",self.add_text_layer),("Duplicate",self.duplicate_layer),
                         ("Delete",self.delete_layer),("↑",self.layer_up),("↓",self.layer_down)]:
            b=QPushButton(label); b.clicked.connect(fn); rowL.addWidget(b)
        layers_layout.addLayout(rowL)
        rowL2=QHBoxLayout()
        self.layer_visible=QCheckBox("Visible"); self.layer_visible.setChecked(True)
        self.layer_visible.stateChanged.connect(self.toggle_layer_visibility)
        self.layer_locked=QCheckBox("Locked")
        self.layer_locked.stateChanged.connect(self.toggle_layer_lock)
        rowL2.addWidget(self.layer_visible); rowL2.addWidget(self.layer_locked)
        layers_layout.addLayout(rowL2)

        settings=QGroupBox("Design & Typography")
        sg=QGridLayout(settings); sg.setHorizontalSpacing(12); sg.setVerticalSpacing(9)
        self.theme=QComboBox(); self.theme.addItems(THEMES.keys()); self.theme.currentTextChanged.connect(self.preview)
        self.size=QComboBox(); self.size.addItems(["1080 × 1350  Portrait","1080 × 1080  Square","1920 × 1080  Landscape"]); self.size.currentIndexChanged.connect(self.preview)
        self.gsize=QSpinBox()
        self.gsize.setRange(24,180)
        self.gsize.setSingleStep(2)
        self.gsize.setValue(72)
        self.gsize.setSuffix(" px")
        self.gsize.valueChanged.connect(self.sync_font_slider)

        self.gsize_slider=QSlider(Qt.Orientation.Horizontal)
        self.gsize_slider.setRange(24,180)
        self.gsize_slider.setValue(72)
        self.gsize_slider.setTickInterval(10)
        self.gsize_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.gsize_slider.valueChanged.connect(self.sync_font_spin)

        self.auto_fit=QCheckBox("Auto-fit text to canvas")
        self.auto_fit.setChecked(True)
        self.auto_fit.stateChanged.connect(self.preview)

        self.frame=QCheckBox("Ornamental frame")
        self.frame.setChecked(True)
        self.frame.stateChanged.connect(self.preview)
        self.water=QLineEdit("JASS GURBANI")
        self.water.textChanged.connect(self.preview)

        self.snap_center=QCheckBox("Snap to center")
        self.snap_center.setChecked(True)
        self.snap_center.stateChanged.connect(self.preview)

        self.align=QComboBox()
        self.align.addItems(["Center","Left","Right"])
        self.align.currentTextChanged.connect(self.preview)

        sg.addWidget(QLabel("Theme"),0,0); sg.addWidget(self.theme,0,1,1,2)
        sg.addWidget(QLabel("Canvas"),1,0); sg.addWidget(self.size,1,1,1,2)
        sg.addWidget(QLabel("Gurbani size"),2,0); sg.addWidget(self.gsize,2,1)
        sg.addWidget(self.gsize_slider,2,2)
        sg.addWidget(self.auto_fit,3,0,1,3)
        sg.addWidget(QLabel("Alignment"),4,0); sg.addWidget(self.align,4,1,1,2)
        sg.addWidget(QLabel("Watermark"),5,0); sg.addWidget(self.water,5,1,1,2)
        sg.addWidget(self.frame,6,0,1,2)
        sg.addWidget(self.snap_center,6,2)
        ll.addWidget(layers_box)
        ll.addWidget(settings); ll.addStretch()
        layout.addWidget(left,1)

        preview_box=QFrame(); preview_box.setObjectName("previewCard")
        pl=QVBoxLayout(preview_box); pl.setContentsMargins(10,10,10,10); pl.setSpacing(9)
        lab=QLabel("LIVE PREVIEW"); lab.setObjectName("previewTitle"); pl.addWidget(lab)
        surface=QFrame(); surface.setObjectName("previewSurface")
        surface_layout=QVBoxLayout(surface); surface_layout.setContentsMargins(10,10,10,10)
        self.canvas=GurbaniCanvas()
        self.canvas.setMinimumSize(520,560)
        self.canvas.textMoved.connect(self.canvas_text_moved)
        self.canvas.textResized.connect(self.canvas_text_resized)
        self.canvas.layerChanged.connect(lambda _index: self.preview())
        surface_layout.addWidget(self.canvas,1)
        pl.addWidget(surface,1)
        hint=QLabel("Drag to move  •  Drag corner to resize  •  Select a layer to edit")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setObjectName("hint")
        pl.addWidget(hint)
        nav=QHBoxLayout()
        prev=QPushButton("‹ Previous"); prev.setObjectName("secondary"); prev.clicked.connect(self.previous)
        nxt=QPushButton("Next ›"); nxt.setObjectName("secondary"); nxt.clicked.connect(self.next)
        nav.addWidget(prev); nav.addStretch(); nav.addWidget(nxt); pl.addLayout(nav)
        layout.addWidget(preview_box,2)
        self.stack.addWidget(page)

    def make_library(self):
        page=QWidget(); l=QVBoxLayout(page)
        h=QLabel("Imported Lines"); h.setObjectName("section"); l.addWidget(h)
        self.list=QListWidget(); self.list.itemClicked.connect(self.select_item); l.addWidget(self.list,1)
        self.stack.addWidget(page)

    def make_themes(self):
        page=QWidget(); l=QVBoxLayout(page)
        h=QLabel("Visual Themes"); h.setObjectName("section"); l.addWidget(h)
        desc=QLabel("Choose a visual mood for your Gurbani artwork."); desc.setObjectName("muted"); l.addWidget(desc)
        grid=QGridLayout()
        for i,name in enumerate(THEMES):
            b=QPushButton(name); b.setMinimumHeight(70); b.setObjectName("secondary")
            b.clicked.connect(lambda _,n=name:self.choose_theme(n))
            grid.addWidget(b,i//2,i%2)
        l.addLayout(grid); l.addStretch(); self.stack.addWidget(page)

    def make_settings(self):
        page=QWidget(); l=QVBoxLayout(page)
        box=QGroupBox("Gurmukhi Font")
        bl=QVBoxLayout(box)
        self.font_label=QLineEdit(); self.font_label.setReadOnly(True); self.font_label.setPlaceholderText("Qt Gurmukhi shaping: automatic font detection")
        choose=QPushButton("Choose Font…"); choose.setObjectName("secondary"); choose.clicked.connect(self.choose_font)
        bl.addWidget(self.font_label); bl.addWidget(choose)
        l.addWidget(box)
        note=QLabel("Tip: Windows users can use Nirmala UI or another font with Gurmukhi support.")
        note.setObjectName("muted"); note.setWordWrap(True); l.addWidget(note); l.addStretch()
        self.stack.addWidget(page)

    def switch_page(self,i):
        if i >= len(self.nav): return
        for n,b in enumerate(self.nav): b.setChecked(n==i)
        self.stack.setCurrentIndex(i)
        self.preview()

    def sync_font_slider(self, value):
        if hasattr(self, "gsize_slider"):
            self.gsize_slider.blockSignals(True)
            self.gsize_slider.setValue(value)
            self.gsize_slider.blockSignals(False)
        self.preview()

    def sync_font_spin(self, value):
        if hasattr(self, "gsize"):
            self.gsize.blockSignals(True)
            self.gsize.setValue(value)
            self.gsize.blockSignals(False)
        self.preview()

    def choose_theme(self,n):
        self.theme.setCurrentText(n); self.switch_page(0)

    def choose_font(self):
        p,_=QFileDialog.getOpenFileName(self,"Choose Gurmukhi Font","","Fonts (*.ttf *.otf)")
        if p:
            self.font_path=p; self.font_label.setText(p); self.preview()

    def new_sample(self):
        self.items=[{"line":"ਸਤਿਗੁਰੁ ਸੇਵਿ ਗੁਣ ਅੰਤਰਿ ਧਿਆਇ ॥","title":"ੴ","subtitle":"Gurbani"}]
        self.load_item(0)

    def load_item(self,i):
        if not self.items: return
        self.current=max(0,min(i,len(self.items)-1)); item=self.items[self.current]
        self.text.blockSignals(True); self.text.setPlainText(item.get("line","")); self.text.blockSignals(False)
        self.title_edit.setText(item.get("title","")); self.subtitle_edit.setText(item.get("subtitle",""))
        self.preview()

    def select_item(self,item):
        self.load_item(item.data(Qt.ItemDataRole.UserRole))

    def previous(self):
        if self.items: self.load_item((self.current-1)%len(self.items))

    def next(self):
        if self.items: self.load_item((self.current+1)%len(self.items))

    def config(self):
        idx=self.size.currentIndex()
        dims=[(1080,1350),(1080,1080),(1920,1080)][idx]
        return {
            "size":dims,"padding":80,"theme":self.theme.currentText(),
            "font_gurmukhi":self.font_path,"font_latin":"Segoe UI","title_size":42,"subtitle_size":24,
            "gurbani_size":self.gsize.value(),"auto_fit":False,
            "text_x":getattr(self,"text_x",0.50),"text_y":getattr(self,"text_y",0.50),
            "text_size":getattr(self,"text_size",self.gsize.value()),
            "alignment":self.align.currentText(),
            "source":self.source_edit.text().strip(),"translation":self.translation_edit.text().strip(),
            "watermark":self.water.text(),
            "watermark_size":20,"frame":self.frame.isChecked(),
            "layers":[{
                "name":l.name,"kind":l.kind,"text":l.text,"visible":l.visible,
                "locked":l.locked,"x":l.x,"y":l.y,"width":l.width,"height":l.height,
                "size":l.size,"rotation":l.rotation,"opacity":l.opacity
            } for l in self.layers]
        }

    def current_item(self):
        return {
            "line":self.text.toPlainText().strip(),
            "title":self.title_edit.text().strip(),
            "subtitle":self.subtitle_edit.text().strip(),
            "source":self.source_edit.text().strip(),"translation":self.translation_edit.text().strip(),
        }

    def make_image(self):
        item=self.current_item()
        if not item["line"]: return None
        return render_image(item,self.config())

    def canvas_text_moved(self, index):
        # Keep the selected layer's position synchronized with the editor.
        if hasattr(self, "layer_list") and 0 <= index < self.layer_list.count():
            self.layer_list.blockSignals(True)
            self.layer_list.setCurrentRow(index)
            self.layer_list.blockSignals(False)
        if hasattr(self, "preview"):
            self.preview()

    def sync_layers(self):
        if len(self.layers)<4: return
        self.layers[0].text=self.text.toPlainText().strip()
        self.layers[0].size=self.gsize.value()
        self.layers[1].text=self.translation_edit.text().strip()
        self.layers[2].text=self.source_edit.text().strip()
        self.layers[3].text=self.water.text().strip()
        self.canvas.set_layers(self.layers)
        self.refresh_layer_list()

    def preview(self):
        if not hasattr(self,"canvas"): return
        self.sync_layers()
        img=self.make_image()
        if img: self.canvas.set_image(img); self.canvas.set_layers(self.layers); self.canvas.update()

    def canvas_text_resized(self,size):
        self.text_size=int(size)
        self.gsize.blockSignals(True); self.gsize.setValue(int(size)); self.gsize.blockSignals(False)
        self.preview()

    def refresh_layer_list(self):
        if not hasattr(self,"layer_list"): return
        self.layer_list.blockSignals(True); self.layer_list.clear()
        for l in self.layers:
            self.layer_list.addItem(("👁 " if l.visible else "○ ")+l.name+(" 🔒" if l.locked else ""))
        if self.layers: self.layer_list.setCurrentRow(max(0,min(self.canvas.selected,len(self.layers)-1)))
        self.layer_list.blockSignals(False)

    def layer_selected(self,index):
        if not (0<=index<len(self.layers)): return
        self.canvas.selected=index; l=self.layers[index]
        self.layer_visible.blockSignals(True); self.layer_visible.setChecked(l.visible); self.layer_visible.blockSignals(False)
        self.layer_locked.blockSignals(True); self.layer_locked.setChecked(l.locked); self.layer_locked.blockSignals(False)

    def layer_changed(self,index):
        self.preview()

    def add_text_layer(self):
        n=len(self.layers)+1
        self.layers.append(Layer(f"Text {n}","text","New text",True,False,.50,.50,.72,.16,42))
        self.canvas.selected=len(self.layers)-1; self.refresh_layer_list(); self.preview()

    def duplicate_layer(self):
        i=self.canvas.selected
        if not 0<=i<len(self.layers): return
        l=self.layers[i]
        self.layers.insert(i+1,Layer(l.name+" Copy",l.kind,l.text,l.visible,l.locked,
            min(.95,l.x+.03),min(.95,l.y+.03),l.width,l.height,l.size,l.rotation,l.opacity))
        self.canvas.selected=i+1; self.refresh_layer_list(); self.preview()

    def delete_layer(self):
        i=self.canvas.selected
        if len(self.layers)<=1 or not 0<=i<len(self.layers): return
        self.layers.pop(i); self.canvas.selected=max(0,i-1); self.refresh_layer_list(); self.preview()

    def layer_up(self):
        i=self.canvas.selected
        if i<=0: return
        self.layers[i-1],self.layers[i]=self.layers[i],self.layers[i-1]
        self.canvas.selected=i-1; self.refresh_layer_list(); self.preview()

    def layer_down(self):
        i=self.canvas.selected
        if i<0 or i>=len(self.layers)-1: return
        self.layers[i+1],self.layers[i]=self.layers[i],self.layers[i+1]
        self.canvas.selected=i+1; self.refresh_layer_list(); self.preview()

    def toggle_layer_visibility(self,state):
        i=self.canvas.selected
        if 0<=i<len(self.layers): self.layers[i].visible=bool(state); self.refresh_layer_list(); self.preview()

    def toggle_layer_lock(self,state):
        i=self.canvas.selected
        if 0<=i<len(self.layers): self.layers[i].locked=bool(state); self.refresh_layer_list(); self.preview()

    def choose_background(self):
        p,_=QFileDialog.getOpenFileName(self,"Choose Background Image","","Images (*.png *.jpg *.jpeg *.webp)")
        if p: self.background_path=p; self.preview()

    def resizeEvent(self,e):
        super().resizeEvent(e)
        if hasattr(self,"canvas"):
            self.canvas.update()


    def import_json(self):
        p,_=QFileDialog.getOpenFileName(self,"Import Gurbani JSON","","JSON Files (*.json)")
        if not p: return
        try:
            data=json.loads(Path(p).read_text(encoding="utf-8"))
            self.items=parse_json(data)
            self.list.clear()
            for i,item in enumerate(self.items):
                li=QListWidgetItem(f"{i+1:03d}  {item.get('line','')[:75]}")
                li.setData(Qt.ItemDataRole.UserRole,i); self.list.addItem(li)
            if self.items:
                self.load_item(0); self.switch_page(1)
            else:
                QMessageBox.information(self,"Import","No usable Gurbani lines were found.")
        except Exception as ex:
            QMessageBox.critical(self,"Import Error",str(ex))

    def project_state(self):
        return {
            "format": "JASS-GURBANI-PROJECT",
            "version": "1.5",
            "layers":[vars(l).copy() for l in self.layers],
            "background_path":self.background_path,
            "created": datetime.datetime.now().isoformat(timespec="seconds"),
            "item": self.current_item(),
            "design": {
                "theme": self.theme.currentText(),
                "canvas": self.size.currentText(),
                "font_size": self.gsize.value(),
                "font_path": self.font_path,
                "watermark": self.water.text(),
                "frame": self.frame.isChecked(),
                "auto_fit": self.auto_fit.isChecked(),
                "alignment": self.align.currentText(),
                "snap_center": self.snap_center.isChecked(),
                "text_x": getattr(self, "text_x", 0.50),
                "text_y": getattr(self, "text_y", 0.50),
                "text_size": getattr(self, "text_size", self.gsize.value()),
            }
        }

    def save_project(self):
        p,_=QFileDialog.getSaveFileName(
            self,"Save Gurbani Project",
            "gurbani_project.gurbani",
            "Gurbani Project (*.gurbani);;JSON (*.json)"
        )
        if not p:
            return
        try:
            Path(p).write_text(
                json.dumps(self.project_state(), ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            QMessageBox.information(self,"Project Saved",f"Project saved to:\n{p}")
        except Exception as ex:
            QMessageBox.critical(self,"Save Error",str(ex))

    def open_project(self):
        p,_=QFileDialog.getOpenFileName(
            self,"Open Gurbani Project","","Gurbani Project (*.gurbani *.json);;All Files (*)"
        )
        if not p:
            return
        try:
            data=json.loads(Path(p).read_text(encoding="utf-8"))
            item=data.get("item",{})
            design=data.get("design",{})
            loaded=data.get("layers")
            if isinstance(loaded,list) and loaded:
                self.layers=[]
                for d in loaded:
                    self.layers.append(Layer(
                        d.get("name","Text"),d.get("kind","text"),d.get("text",""),
                        bool(d.get("visible",True)),bool(d.get("locked",False)),
                        float(d.get("x",.50)),float(d.get("y",.50)),
                        float(d.get("width",.80)),float(d.get("height",.20)),
                        int(d.get("size",48)),float(d.get("rotation",0)),float(d.get("opacity",1))
                    ))
            self.background_path=data.get("background_path","")

            self.text.setPlainText(item.get("line",""))
            self.title_edit.setText(item.get("title",""))
            self.subtitle_edit.setText(item.get("subtitle",""))
            self.source_edit.setText(item.get("source",""))

            theme=design.get("theme")
            if theme in THEMES:
                self.theme.setCurrentText(theme)
            canvas=design.get("canvas")
            if canvas:
                idx=self.size.findText(canvas)
                if idx>=0: self.size.setCurrentIndex(idx)

            fp=design.get("font_path","")
            if fp and Path(fp).exists():
                self.font_path=fp
                self.font_label.setText(fp)

            self.water.setText(design.get("watermark","JASS GURBANI"))
            self.frame.setChecked(bool(design.get("frame",True)))
            self.auto_fit.setChecked(bool(design.get("auto_fit",False)))
            self.snap_center.setChecked(bool(design.get("snap_center",True)))

            al=design.get("alignment","Center")
            idx=self.align.findText(al)
            if idx>=0: self.align.setCurrentIndex(idx)

            self.text_x=float(design.get("text_x",0.50))
            self.text_y=float(design.get("text_y",0.50))
            self.text_size=int(design.get("text_size",design.get("font_size",72)))
            self.gsize.setValue(self.text_size)
            self.preview()
            QMessageBox.information(self,"Project Loaded",f"Project loaded from:\n{p}")
        except Exception as ex:
            QMessageBox.critical(self,"Open Error",str(ex))

    def save_current(self):
        img=self.make_image()
        if not img: QMessageBox.warning(self,"Nothing to render","Enter a Gurbani line first."); return
        p,_=QFileDialog.getSaveFileName(self,"Save Gurbani Image",f"gurbani_{datetime.datetime.now():%Y%m%d_%H%M%S}.png","PNG Image (*.png)")
        if p:
            img.save(p,"PNG"); QMessageBox.information(self,"Saved",f"Image saved to:\\n{p}")

    def batch_export(self):
        if not self.items:
            QMessageBox.warning(self,"Batch Export","Import a JSON file first."); return
        folder=QFileDialog.getExistingDirectory(self,"Choose Export Folder")
        if not folder: return
        cfg=self.config(); count=0
        for i,item in enumerate(self.items,1):
            img=render_image(item,cfg)
            if img:
                img.save(Path(folder)/f"gurbani_{i:03d}.png","PNG"); count+=1
        QMessageBox.information(self,"Batch Complete",f"Exported {count} images to:\\n{folder}")

class QStackedWidgetCompat(QWidget):
    """Tiny stacked-page compatibility wrapper."""
    def __init__(self):
        super().__init__()
        from PySide6.QtWidgets import QStackedLayout
        self._layout=QStackedLayout(self)
    def addWidget(self,w): self._layout.addWidget(w)
    def setCurrentIndex(self,i): self._layout.setCurrentIndex(i)

if __name__=="__main__":
    app=QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    win=MainWindow()
    win.show()
    sys.exit(app.exec())
