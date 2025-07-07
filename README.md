# Playlist Builder

A Python-based playlist builder application.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

```bash
# Install in development mode
uv sync
```

## Usage

```bash
# Run the application
uv run plbuild

# Or directly with Python
uv run python -m playlist_builder

# Or activate the virtual environment and run directly
source .venv/bin/activate
plbuild
```

## Development

### Building

```bash
# Build distribution packages
uv build
```

## Entry Point

The main application entry point is `playlist_builder:main`, accessible via the `uv run plbuild` command.