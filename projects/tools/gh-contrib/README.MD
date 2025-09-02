# GitHub Contribution Visualizer

A CLI tool to visualize GitHub contributions using ANSI colors.

## Usage

```bash
go build
./ghcontrib -user <username>
```

Replace `<username>` with the GitHub username you want to visualize.

## Example

```bash
./ghcontrib -user torvalds
```

This will display the contribution graph for Linus Torvalds in the terminal.

## Colors

- White: No contributions
- Green: Low contributions
- Yellow: Medium contributions
- Red: High contributions
