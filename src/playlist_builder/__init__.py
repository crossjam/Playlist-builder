import os
import pathlib
from typing import List, Set

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


def create_m3u_playlist(music_files: List[pathlib.Path], output_file: pathlib.Path, relative_paths: bool = False) -> None:
    """Create an M3U playlist file from a list of music files."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        
        for music_file in music_files:
            if relative_paths:
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
@click.option('--output', '-o', type=click.Path(path_type=pathlib.Path), 
              help='Output playlist file path. Default: playlist.m3u in the target directory')
@click.option('--relative/--absolute', default=True, 
              help='Use relative paths in playlist (default: relative)')
@click.option('--verbose', '-v', is_flag=True, help='Show verbose output')
def main(directory: pathlib.Path, output: pathlib.Path, relative: bool, verbose: bool) -> None:
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
        output = directory / 'playlist.m3u'
    
    # Create the playlist
    create_m3u_playlist(music_files, output, relative)
    
    click.echo(f"Created playlist: {output}")
    
    if verbose:
        click.echo("Files included:")
        for music_file in music_files:
            click.echo(f"  {music_file}")


if __name__ == '__main__':
    main()
