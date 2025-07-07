import os
import pathlib
import sys
from typing import List, Set, Union, TextIO

import click


MUSIC_EXTENSIONS: Set[str] = {
    '.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg', '.wma', '.mp4', '.m4v'
}


def find_music_files(root_dir: pathlib.Path) -> List[pathlib.Path]:
    """Recursively find music files in the given directory."""
    music_files = []
    
    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in MUSIC_EXTENSIONS:
            music_files.append(file_path)
    
    return sorted(music_files)


def validate_m3u_filename(filename: pathlib.Path) -> pathlib.Path:
    """Validate and potentially modify the M3U filename."""
    if not filename.suffix.lower() == '.m3u':
        suggested_name = filename.with_suffix('.m3u')
        if click.confirm(f"Filename '{filename}' doesn't end with .m3u. Add .m3u extension?", default=True):
            return suggested_name
        else:
            return filename
    return filename


def create_m3u_playlist(music_files: List[pathlib.Path], output_file: Union[pathlib.Path, TextIO], relative_paths: bool = False) -> None:
    """Create an M3U playlist file from a list of music files."""
    if isinstance(output_file, pathlib.Path):
        # Writing to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            _write_playlist_content(f, music_files, output_file, relative_paths)
    else:
        # Writing to stdout or other file-like object
        _write_playlist_content(output_file, music_files, None, relative_paths)


def _write_playlist_content(f: TextIO, music_files: List[pathlib.Path], output_file: Union[pathlib.Path, None], relative_paths: bool) -> None:
    """Write the M3U playlist content to the file object."""
    f.write('#EXTM3U\n')
    
    for music_file in music_files:
        if relative_paths and output_file is not None:
            # Make path relative to the playlist file's directory
            try:
                path_to_write = music_file.relative_to(output_file.parent)
            except ValueError:
                # If files are not under the same root, use absolute path
                path_to_write = music_file.resolve()
        else:
            path_to_write = music_file.resolve()
        
        f.write(f'{path_to_write}\n')


@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=pathlib.Path))
@click.option('--output', '-o', type=str, 
              help='Output playlist file path or "-" for stdout. Default: playlist.m3u in the target directory')
@click.option('--relative/--absolute', default=True, 
              help='Use relative paths in playlist (default: relative)')
@click.option('--verbose', '-v', is_flag=True, help='Show verbose output')
def main(directory: pathlib.Path, output: str, relative: bool, verbose: bool) -> None:
    """Create an M3U playlist from music files found recursively in DIRECTORY."""
    
    if verbose:
        click.echo(f"Scanning directory: {directory}")
    
    # Find all music files
    music_files = find_music_files(directory)
    
    if not music_files:
        click.echo("No music files found in the specified directory.")
        return
    
    if verbose:
        click.echo(f"Found {len(music_files)} music files")
    
    # Determine output file path
    if output is None:
        output_file = directory / 'playlist.m3u'
        create_m3u_playlist(music_files, output_file, relative)
        click.echo(f"Created playlist: {output_file}")
    elif output == '-':
        # Write to stdout
        create_m3u_playlist(music_files, sys.stdout, relative)
    else:
        # Validate the provided filename
        output_file = validate_m3u_filename(pathlib.Path(output))
        create_m3u_playlist(music_files, output_file, relative)
        click.echo(f"Created playlist: {output_file}")
    
    if verbose:
        click.echo("Files included:")
        for music_file in music_files:
            click.echo(f"  {music_file}")


if __name__ == '__main__':
    main()
