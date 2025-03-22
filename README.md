# Dotbot Copy Plugin

A plugin for [dotbot](https://github.com/anishathalye/dotbot) that provides file copying functionality.

## Installation

```bash
pip install -e .
```

## Usage

Add the following to your `install.conf.yaml`:

```yaml
- defaults:
    copy:
      overwrite: false  # Global default for overwrite option

- copy:
    ~/.config/myapp/config.json:
      path: dotfiles/myapp/config.json
      overwrite: true  # Override global default for this file
    ~/.local/share/myapp/data:
      path: dotfiles/myapp/data
      overwrite: false  # Use global default
```

## Configuration

The plugin supports the following configuration options:

### Global Defaults
- `overwrite`: (boolean) Global default for whether to overwrite existing files. Defaults to `false`.

### File Options
- `path`: (string) The source path of the file to copy
- `overwrite`: (boolean) Whether to overwrite this specific file if it exists. If not specified, uses the global default.

### Simple Format
You can also use a simpler format for files that don't need the overwrite option:

```yaml
- copy:
    ~/.config/myapp/config.json: dotfiles/myapp/config.json
```

### Using Destination Basename
If the source location is omitted or set to null, the plugin will use the basename of the destination, with a leading . stripped if present. This makes the following two configurations equivalent:

```yaml
- copy:
    ~/.vimrc: vimrc
    ~/.vimrc:
        path: vimrc
```

## License

MIT License 