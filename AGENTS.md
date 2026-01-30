# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Boxes.py is a Python library and web application for generating parametrized laser-cut box designs. It outputs SVG files and supports multiple export formats (PostScript, DXF, PLT, GCode, PDF, LBRN2). The project serves as:
- An online box generator at https://boxes.hackerspace-bamberg.de/
- An Inkscape plugin
- A reusable library for custom generators

## Development Commands

```bash
# Install package
pip install .
pip install .[dev]              # Include dev dependencies (pytest, mypy, pre-commit)

# Run web server locally
scripts/boxesserver             # Starts Flask dev server
docker-compose up               # Alternative: runs on http://localhost:4455

# CLI usage
boxes --help                    # List available generators
boxes Box --x 100 --y 100 --h 50  # Generate a box

# Code quality (runs pytest, mypy, autoflake, etc.)
pre-commit run --all-files

# Generate example SVGs
boxes --examples
git add -f examples/*.svg       # Examples must be force-added

# Build documentation
cd documentation/src && make html
```

## Architecture

### Core Classes

- **`boxes.Boxes`** (`boxes/__init__.py`): The main API class (~6000 lines). All generators inherit from this. Provides drawing methods, parameter handling, and output format management.

- **`boxes.edges`** (`boxes/edges.py`): Edge joint implementations (FingerJoint, DoveTail, Hinge, Flex, etc.). Edges define how pieces connect at boundaries.

- **`boxes.drawing`**: Rendering backend using Context/Surface pattern for multiple output formats.

### Generator Pattern

Generators live in `boxes/generators/`. Each is a Python file with a class inheriting from `boxes.Boxes`:

```python
from boxes import *

class MyBox(Boxes):
    """Description shown in UI"""

    ui_group = "Box"  # Category: Box, FlexBox, Tray, Shelf, WallMounted, Holes, Part, Misc, Unstable

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)  # Enable edge settings
        self.buildArgParser(x=100, y=100, h=50)          # Add parameters

    def render(self):
        # Drawing code here using self.rectangularWall(), self.move(), etc.
```

Use `boxes/generators/_template.py` as starting point for new generators.

### Auto-Discovery

Generators are automatically discovered via `pkgutil.walk_packages()` in `boxes/generators/__init__.py`. Files starting with `_` are excluded. Custom generators can be added via `BOXES_GENERATOR_PATH` environment variable.

### UI Groups

Generators are categorized by `ui_group` attribute. Available groups are defined in `boxes/generators/__init__.py`:
- Box, FlexBox, Tray, Shelf, WallMounted, Holes, Part, Misc, Unstable

### Key Concepts

- **Burn parameter**: Compensates for material removed by laser cutting
- **Thickness**: Material thickness, automatically adjusts finger joint sizing
- **Finger joints**: Primary joining method for 90° edges and T-connections
- **Flex cuts**: Allow material bending for rounded edges and living hinges
- **`move()` method**: Handles layout/positioning of parts on cutting sheet

## Entry Points

Defined in `pyproject.toml`:
- `boxes` → `boxes/scripts/boxes_main.py` (CLI)
- `boxesserver` → `boxes/scripts/boxesserver.py` (Flask web server)
- `boxes_proxy` → `boxes/scripts/boxes_proxy.py` (Inkscape integration)

## Code Quality

Pre-commit hooks enforce:
- mypy type checking (strict mode)
- autoflake (remove unused imports)
- pyupgrade (Python 3.10+ syntax)
- pytest (runs on every commit)
- codespell, shellcheck, rstcheck

Python 3.10+ required.
