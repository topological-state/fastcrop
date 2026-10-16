from pathlib import Path
from typing import ClassVar

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
)


class CropRectItem(QGraphicsRectItem):
    """An interactive cropping rectangle with a fixed aspect ratio."""

    def __init__(self, aspect_ratio: float):
        super().__init__()
        self.aspect_ratio = aspect_ratio
        self.setFlags(
            QGraphicsRectItem.ItemIsMovable
            | QGraphicsRectItem.ItemIsSelectable
            | QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setPen(QPen(QColor("yellow"), 3))
        self.setBrush(QColor(255, 255, 0, 50))

    def set_aspect_ratio(self, ratio: float):
        """Update the aspect ratio and resize accordingly."""
        self.aspect_ratio = ratio

    def update_size(self, image_width: float, image_height: float):
        """Maximize the rectangle size within the image dimensions."""
        if image_width / image_height > self.aspect_ratio:
            h = image_height
            w = image_height * self.aspect_ratio
        else:
            w = image_width
            h = image_width / self.aspect_ratio

        self.setRect(0, 0, w, h)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange and hasattr(
            self, "image_size"
        ):
            img_w, img_h = self.image_size
            rect_w = self.rect().width()
            rect_h = self.rect().height()

            new_pos = value
            new_pos.setX(max(0, min(new_pos.x(), img_w - rect_w)))
            new_pos.setY(max(0, min(new_pos.y(), img_h - rect_h)))
            return new_pos
        return super().itemChange(change, value)


class CropView(QGraphicsView):
    """Custom GraphicsView to handle key events for the viewer."""

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.viewer = None

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.viewer:
            self.viewer.keyPressEvent(event)
        else:
            super().keyPressEvent(event)


class FastCropViewer(QMainWindow):
    """Main window for viewing and cropping images."""

    saveRequested = Signal(QRectF, Path)
    nextRequested = Signal()
    prevRequested = Signal()
    firstRequested = Signal()
    lastRequested = Signal()

    ASPECT_RATIOS: ClassVar = [
        (1.0, "1:1"),
        (4 / 3, "4:3"),
        (16 / 9, "16:9"),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastCrop")

        self.scene = QGraphicsScene()
        self.view = CropView(self.scene)
        self.view.viewer = self
        self.setCentralWidget(self.view)

        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)

        self.pixmap_item: QGraphicsPixmapItem | None = None
        self.crop_rect: CropRectItem | None = None

        self.current_ratio_idx = 0
        self.zoom_factor = 1.0

        self.current_image_path: Path | None = None
        self.image_list: list[Path] = []
        self.current_index = -1

    def load_image(self, path: Path, index: int = -1, total: int = -1) -> None:
        """Load an image into the viewer."""
        self.current_image_path = path
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            return

        # Store current crop state and image size before clearing
        prev_rect_pos = None
        prev_image_size = None
        if self.pixmap_item and self.crop_rect:
            prev_rect_pos = self.crop_rect.pos()
            prev_image_size = (
                self.pixmap_item.pixmap().width(),
                self.pixmap_item.pixmap().height(),
            )

        self.scene.clear()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        # Always create a new crop rect since the old one was deleted by scene.clear()
        self.crop_rect = CropRectItem(self.ASPECT_RATIOS[self.current_ratio_idx][0])

        img_w, img_h = pixmap.width(), pixmap.height()
        self.crop_rect.update_size(img_w, img_h)

        # Restore position if image dimensions match
        if prev_image_size == (img_w, img_h) and prev_rect_pos:
            self.crop_rect.setPos(prev_rect_pos)
        else:
            # Center it initially
            rect_w = self.crop_rect.rect().width()
            rect_h = self.crop_rect.rect().height()
            self.crop_rect.setPos((img_w - rect_w) / 2, (img_h - rect_h) / 2)

        self.scene.addItem(self.crop_rect)

        # Constraints for moving the crop rect
        self.crop_rect.image_size = (img_w, img_h)

        self.view.fitInView(
            self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.zoom_factor = 1.0
        self.view.setTransform(self.view.transform())  # reset if needed

        # Update window title
        if index != -1 and total != -1:
            name = path.name
            if len(name) > 32:
                name = f"{name[:16]}...{name[-16:]}"
            self.setWindowTitle(f"{name} ({index + 1}/{total}) {img_w}x{img_h}")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle keyboard input for navigation and controls."""
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.handle_save()
        elif event.key() == Qt.Key.Key_Right:
            self.handle_next()
        elif event.key() == Qt.Key.Key_Left:
            self.handle_prev()
        elif event.key() == Qt.Key.Key_Home:
            self.handle_first()
        elif event.key() == Qt.Key.Key_End:
            self.handle_last()
        elif event.key() == Qt.Key.Key_Asterisk:  # Num-*
            self.cycle_aspect_ratio()
        elif event.key() == Qt.Key.Plus or event.key() == Qt.Key.Equal:
            self.zoom(1.2)
        elif event.key() == Qt.Key.Minus:
            self.zoom(0.8)
        else:
            super().keyPressEvent(event)

    def cycle_aspect_ratio(self) -> None:
        """Cycle through the predefined aspect ratio constraints."""
        self.current_ratio_idx = (self.current_ratio_idx + 1) % len(self.ASPECT_RATIOS)
        ratio = self.ASPECT_RATIOS[self.current_ratio_idx][0]
        if self.crop_rect and self.pixmap_item:
            self.crop_rect.set_aspect_ratio(ratio)
            self.crop_rect.update_size(
                self.pixmap_item.pixmap().width(), self.pixmap_item.pixmap().height()
            )

    def zoom(self, factor: float) -> None:
        """Zoom the viewer by the given factor."""
        self.zoom_factor *= factor
        self.view.setTransform(self.view.transform().scale(factor, factor))

    def handle_save(self):
        """Save the current crop and move to next."""
        if self.crop_rect and self.current_image_path:
            # Get the crop rect in image coordinates
            crop_rect_f = self.crop_rect.sceneBoundingRect()
            self.saveRequested.emit(crop_rect_f, self.current_image_path)

    def handle_next(self):
        """Move to next image."""
        self.nextRequested.emit()

    def handle_prev(self):
        """Move to previous image."""
        self.prevRequested.emit()

    def handle_first(self):
        """Jump to first image."""
        self.firstRequested.emit()

    def handle_last(self):
        """Jump to last image."""
        self.lastRequested.emit()
