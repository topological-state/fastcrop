## Project Domain

`fastcrop` is a simple Python application that displays an image and lets the user apply a scale and/or crop operation. 
Images are loaded one-by-one from a given directory, modified images are saved in a separate directory.

For each image, the user has the following controls:

- Drag and drop the mouse to move the selection rectangle.
- Press Enter to save the cropped image and move to the next one.
- Press Tab to move to the next image without saving.
- Press Shift-Tab to move to the previous image without saving.
- Press + or - to upscale or downscale the image, respectively, in steps of 10%.

The selection frame has a fixed size as specified on the command line, only the position can be changed.
The saved image is cropped to the size of the selection frame.
If the frame is larger than the image, black padding is added to both sides of the image.


## Project Setup and Management

- Python version: 3.12.
- Dependency management: `uv` and `pyproject.toml`. Never use `pip`
  or a `requirements.txt` file.
- Add a dependency with `uv add <package>`. Never use `uv pip`
  for dependencies.
- Run the app with `uv run main.py`.
- Branch from `main` as `feature/<name>` and use Conventional Commits.
- Stage changes for review. Don't commit to `main` or push without
  being asked.
- The GUI should be based on `pyside6`.


## Coding Conventions

- Type-hint public functions and methods, including their return types.
- Use `pathlib` for path management. Don't use `os.path`.
- Prefer f-strings over `str.format()` or `%` formatting.
- Follow EAFP: handle exceptions rather than checking conditions up front.
- Write Google-style docstrings for every public function and method.
- Embrace idiomatic Python like comprehensions, generators, and decorators.


## Project Structure

- The project is flat: `main.py` holds the app and `cars.json` holds
  the data.
- The `main.py` file is the only module to edit when adding features.
- Put tests in `tests/test_main.py`.
- Don't create new packages or new files without being asked.


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
