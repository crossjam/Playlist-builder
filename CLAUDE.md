# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based playlist builder application. The project uses:
- Python 3.13+ (specified in `.python-version`)
- setuptools for building
- Entry point: `playlist_builder:main` (command: `plbuild`)

## Development Setup

```bash
# Install in development mode
uv sync

# Run the application
plbuild
```

## Common Commands

### Building and Installation
```bash
# Install in development mode
uv sync

# Build distribution packages
uv build
```

### Running
```bash
# Run the main application
plbuild

# Or directly with Python
python -m playlist_builder
```

## Architecture

- **Entry Point**: `src/playlist_builder/__init__.py:main()`
- **Package Structure**: Single package `playlist_builder` under `src/`
- **Build System**: setuptools with pyproject.toml configuration
- **Current State**: Minimal "Hello World" application ready for development

## Project Structure

```
playlist-builder/
├── src/playlist_builder/     # Main package
│   └── __init__.py          # Entry point with main() function
├── pyproject.toml           # Project configuration and dependencies
├── .python-version          # Python version specification (3.13)
└── .gitignore              # Standard Python gitignore
```