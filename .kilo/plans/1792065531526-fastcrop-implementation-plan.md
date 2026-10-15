# FastCrop Implementation Plan

## Context
`fastcrop` is a Python application for sequential, interactive cropping of images. It allows users to select a region with a fixed aspect ratio and save the cropped result.

## Decisions
- **GUI**: PySide6 using `QGraphicsView` and `QGraphicsRectItem` for the viewer and cropping frame.
- **Image Processing**: Pillow for cropping and scaling (max height 1440px).
- **Aspect Ratios**: 1:1, 4:3, 16:9.
- **Input**: Directory path from CLI argument, falling back to `QFileDialog`.
- **Output**: Saved images go into a `fastcrop/` subdirectory of the source directory.
- **Viewer Features**: 
    - Zoom in/out using `+` and `-` keys.
    - Interactive drag-and-drop of the cropping frame.
- **Controls**:
    - `Enter`: Crop, save, and move to next image.
    - `Right Arrow`: Move to next image without saving.
    - `Left Arrow`: Move to previous image without saving.
    - `Num-*`: Cycle aspect ratios.

## Task List

### 1. Environment Setup
- [ ] Install dependencies: `uv add pyside6 pillow`.

### 2. Viewer Implementation (`viewer.py`)
- [ ] Create `FastCropViewer` window class.
- [ ] Implement `QGraphicsView` for image display.
- [ ] Implement the cropping rectangle (`QGraphicsRectItem`):
    - Initialize to the largest possible size for the current aspect ratio.
    - Implement aspect ratio cycling logic.
    - Implement drag-and-drop repositioning.
- [ ] Implement keyboard event handlers for navigation and aspect ratio cycling.
- [ ] Implement zoom functionality (`+`/`-`).

### 3. Main Application Implementation (`main.py`)
- [ ] Implement directory resolution (CLI argument $\rightarrow$ Dialog).
- [ ] Implement image discovery (listing supported formats in the directory).
- [ ] Create the main application loop and coordinate with `FastCropViewer`.
- [ ] Implement the cropping and scaling pipeline using Pillow:
    - Crop to the selection frame.
    - Scale to max height of 1440px while maintaining aspect ratio.
    - Save to the `fastcrop/` subdirectory.

### 4. Validation & Quality Gates
- [ ] Update Google-style docstrings and type-hints for all public methods.
- [ ] Run `uv run ruff format` to ensure formatting.
- [ ] Run `uv run ruff check` to ensure no lint errors.
- [ ] Run `uv run ty main.py` for type checking.

## Boundaries & Risks
- **Image Formats**: Support common formats (JPEG, PNG, TIFF) supported by Pillow.
- **Performance**: Load images one-by-one to avoid high memory usage with large datasets.
- **Coordinate Mapping**: Ensure correct mapping between the `QGraphicsView` coordinates and the original image pixels.
