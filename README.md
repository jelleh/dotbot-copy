# Dotbot Copy Plugin

A plugin for [dotbot](https://github.com/anishathalye/dotbot) that provides file copying functionality.

## Purpose

This plugin is designed for scenarios where you need to copy configuration files instead of creating symbolic links. It's particularly useful when you have example configuration files in your dotfiles repository that need to be copied to different machines, where each machine may require its own local modifications. Unlike dotbot's built-in linking functionality, this plugin creates actual copies of the files, allowing for machine-specific customizations while maintaining the original example files in your dotfiles repository.

## Safety Features

The plugin includes several safety measures to prevent accidental file operations:

1. **Home Directory Restriction**: All operations are restricted to the user's home directory. Any attempts to copy files outside the home directory will be blocked.

2. **Overwrite Protection**: By default, existing files are never overwritten. The `overwrite` option must be explicitly set to `true` to allow overwriting files.

3. **Directory Safety**: When copying directories, the plugin checks for existing files in the destination to prevent accidental overwrites of any files within the directory structure.

4. **Parent Directory Control**: The `create` option controls whether parent directories should be created. When set to `false` (default), the plugin will fail if parent directories don't exist, preventing accidental directory creation.

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
      create: false     # Whether to create parent directories as needed

- copy:
    ~/.config/myapp/config.json:
      path: config/myapp/config.json
      overwrite: true   # Override global default for this file
      create: true      # Create parent directories for this file
    ~/.local/share/myapp/data:
      path: local/share/myapp/data
      overwrite: false  # Use global default
      create: false     # Use global default
```

### Simple Format
You can also use a simpler format for files that don't need the overwrite option:

```yaml
- copy:
    ~/.config/myapp/config.json: config/myapp/config.json
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