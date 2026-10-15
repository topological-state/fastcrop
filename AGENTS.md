## Project Domain

`fastcrop` is a simple Python application that provides sequential, interactive cropping of a large number of images.
Its main use case is to crop images in portrait format taken with smartphones to landscape format used on desktops and laptops, keeping only the most interesting part at an aspect ratio between 1:1 and 16:9.

The user interface consists of an image viewer with scaling and cropping functions invoked via the keyboard.
Images are loaded one-by-one from a given directory, modified images are saved in a sub-directory named `fastcrop`.

A selection rectangle indicates the region that will be saved.
The rectangle has a fixed aspect ratio of 1:1, 4:3, or 16:9 selected by the user.
Its size is maximized within the image dimensions but constrained by the aspect ratio.
Its position is set by the user.

For each image, the user has the following controls:

- Drag and drop the mouse to move the selection rectangle.
- Press Enter to save the cropped image and move to the next one.
- Press Right-Arrow to move to the next image without saving.
- Press Left-Arrow to move to the previous image without saving.
- Press Num-* to cycle through aspect ratio constraints 1:1, 4:3, 16:9.

The saved image is cropped to the size of the selection frame and, if necessary, scaled to a maximum height of 1440 pixels.
The selection frame carries over to the next image if its dimensions match the previous one.


## Project Setup and Management

- Python version: 3.14.
- Dependency management: `uv` and `pyproject.toml`. 
  Never use `pip` or a `requirements.txt` file.
- Add a dependency with `uv add <package>`. 
  Never use `uv pip` for dependencies.
- Run the app with `uv run main.py`.
- Branch from `main` as `feature/<name>` and use Conventional Commits.
- Stage changes for review. 
  Don't commit to `main` or push without being asked.


## Coding Conventions

- Type-hint public functions and methods, including their return types.
- Use `pathlib` for path management. Don't use `os.path`.
- Prefer f-strings over `str.format()` or `%` formatting.
- Follow EAFP: handle exceptions rather than checking conditions up front.
- Write Google-style docstrings for every public function and method.
- Embrace idiomatic Python like comprehensions, generators, and decorators.


## Project Structure

- The project contains two modules:
  - `main.py` holds the main app.
  - `viewer.py` holds the window class of the viewer including actions.
- Ask before creating new packages or new files.
- The GUI should be based on `pyside6`.
- For image processing, I suggest to use the pillow library.


## Quality Gates

A task is done only when all of these pass:

- `uv run ruff format` leaves the code unchanged.
- `uv run ruff check` reports no errors.
- `uv run ty main.py` reports no errors.


## Constraints

- Ask before adding any external dependency.
- Declare a task done only after the gates pass and docstrings are
  updated.


## Ignore

Treat everything in `.gitignore` as off-limits to read or edit. On top of
that, never open:

- Secrets and `.env` files
- Large data files unrelated to the current task
- Vendored or generated code

