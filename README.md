# Dotbot Copy Plugin

A plugin for [dotbot](https://github.com/anishathalye/dotbot) that provides file copying functionality.

## Purpose

This plugin is designed for scenarios where you need to copy configuration files instead of creating symbolic links. It's particularly useful when you have example configuration files in your dotfiles repository that need to be copied to different machines, where each machine may require its own local modifications. Unlike dotbot's built-in linking functionality, this plugin creates actual copies of the files, allowing for machine-specific customizations while maintaining the original example files in your dotfiles repository.

## Usage

Add the plugin as a submodule to your dotfiles repo:

```bash
git submodule add https://github.com/jelleh/dotbot-copy.git
```

Execute `dotbot` with plugin parameter:

```bash
./install -p dotbot-copy/copy.py
```

## Configuration

All configuration parameters can be specified either globally in `defaults` task or locally for each individual record.

Example containing all options enumerated with their default values:

```yaml
- defaults:
    copy:
      overwrite: false  # Whether to overwrite existing files

- copy:
    ~/.config/myapp/config.json:
      path: dotfiles/myapp/config.json
      overwrite: true  # Override global default for this file
    ~/.local/share/myapp/data:
      path: dotfiles/myapp/data
      overwrite: false  # Use global default
```

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