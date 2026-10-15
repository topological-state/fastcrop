import sys
from pathlib import Path
from typing import ClassVar

from PIL import Image
from PySide6.QtWidgets import QApplication, QFileDialog

from viewer import FastCropViewer


class FastCropApp:
    """Main application controller for FastCrop."""

    SUPPORTED_EXTENSIONS: ClassVar = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tif",
        ".tiff",
        ".bmp",
        ".webp",
    }

    def __init__(self) -> None:
        """Initialize the FastCrop application."""
        self.app = QApplication(sys.argv)
        self.viewer = FastCropViewer()

        self.source_dir: Path = Path()
        self.images: list[Path] = []
        self.current_index = -1

        # Connect signals
        self.viewer.saveRequested.connect(self.save_crop)
        self.viewer.nextRequested.connect(self.next_image)
        self.viewer.prevRequested.connect(self.prev_image)

    def resolve_directory(self) -> None:
        """Determine the source directory from CLI or dialog."""
        if len(sys.argv) > 1:
            path = Path(sys.argv[1])
            if path.is_dir():
                self.source_dir = path
                return

        # Fallback to dialog
        path = QFileDialog.getExistingDirectory(self.viewer, "Select Image Directory")
        if path:
            self.source_dir = Path(path)
        else:
            sys.exit(0)

    def discover_images(self) -> None:
        """Find all supported images in the source directory."""
        self.images = sorted(
            [
                p
                for p in self.source_dir.iterdir()
                if p.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ]
        )
        if not self.images:
            print("No supported images found in the directory.")
            sys.exit(0)

    def next_image(self) -> None:
        """Advance to the next image."""
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.viewer.load_image(self.images[self.current_index])

    def prev_image(self) -> None:
        """Return to the previous image."""
        if self.current_index > 0:
            self.current_index -= 1
            self.viewer.load_image(self.images[self.current_index])

    def save_crop(self, crop_rect, image_path: Path) -> None:
        """Crop, scale, and save the image."""
        # crop_rect is a QRectF (x, y, w, h)
        x, y, w, h = crop_rect.x(), crop_rect.y(), crop_rect.width(), crop_rect.height()

        try:
            with Image.open(image_path) as img:
                # Crop using Pillow (left, top, right, bottom)
                cropped = img.crop((x, y, x + w, y + h))

                # Scale to max height of 1440px
                max_h = 1440
                if cropped.height > max_h:
                    scale = max_h / cropped.height
                    new_w = int(cropped.width * scale)
                    new_h = max_h
                    cropped = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

                # Save to subdirectory 'fastcrop'
                output_dir = self.source_dir / "fastcrop"
                output_dir.mkdir(exist_ok=True)

                output_path = output_dir / image_path.name
                cropped.save(output_path)

                print(f"Saved: {output_path}")

            # After saving, move to next image
            self.next_image()

        except (OSError, Image.UnidentifiedImageError) as e:
            print(f"Error saving crop for {image_path}: {e}")

    def run(self) -> None:
        """Start the application."""
        self.resolve_directory()
        self.discover_images()

        self.current_index = 0
        self.viewer.load_image(self.images[self.current_index])

        self.viewer.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = FastCropApp()
    app.run()
