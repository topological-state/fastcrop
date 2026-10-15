# FastCrop

FastCrop is a simple, interactive Python application designed for the sequential cropping of large numbers of images. It is particularly useful for converting portrait images (e.g., from smartphones) into landscape formats suitable for desktop displays, while maintaining a specific aspect ratio.

## Features

- **Interactive Cropping**: Drag and drop a selection rectangle to choose the best part of your image.
- **Fixed Aspect Ratios**: Quickly cycle between 1:1, 4:3, and 16:9 aspect ratios.
- **Efficient Workflow**: Save and move to the next image with a single key press.
- **Smart Frame Persistence**: The cropping frame position is preserved when moving between images of the same dimensions.
- **Automatic Scaling**: Cropped images are automatically scaled to a maximum height of 1440px to ensure consistency.
- **Zoom Support**: Zoom in and out of the viewer to precisely position your crop.

## Controls

| Key | Action |
| :--- | :--- |
| **Mouse Drag** | Move the selection rectangle |
| **Enter** | Save crop and move to next image |
| **$\rightarrow$ (Right Arrow)** | Move to next image without saving |
| **$\leftarrow$ (Left Arrow)** | Move to previous image without saving |
| **Num-*** | Cycle aspect ratios (1:1 $\rightarrow$ 4:3 $\rightarrow$ 16:9) |
| **+ / =** | Zoom in |
| **-** | Zoom out |

## Installation

FastCrop uses `uv` for dependency and environment management.

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Synchronize the environment:
   ```bash
   uv sync
   ```

## Usage

Run the application using `uv`. You can provide the source directory as a command-line argument, or leave it blank to use the directory selection dialog.

```bash
uv run main.py /path/to/your/images
```

### Output
Processed images are saved in a subdirectory named `fastcrop` within your source directory.

## Supported Formats
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- TIFF (`.tif`, `.tiff`)
- BMP (`.bmp`)
- WebP (`.webp`)
