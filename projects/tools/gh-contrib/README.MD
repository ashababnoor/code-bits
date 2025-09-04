# GitHub Contribution Visualizer

A small CLI that fetches a user's GitHub contributions calendar and renders an ANSI-colored terminal heatmap, plus summary stats (total contributions, date range and current streak).

## Features

- Renders a 7×W grid (week columns × weekday rows) using ANSI color blocks to approximate GitHub's contribution graph.
- Prints month labels, a legend, total contributions and current streak.
- Uses a custom User-Agent to reduce the chance of simple bot blocking.

## Requirements

- Go 1.16+ installed and available on PATH
- Network access to https://github.com

## Build

From this folder run:

```bash
go build -o ghcontrib contrib.go
```

Or run without building:

```bash
go run contrib.go <github-username>
```

## Usage

```bash
# after building
./ghcontrib <github-username>

# or directly
go run contrib.go <github-username>
```

Example:

```bash
./ghcontrib ashababnoor
```

Expected output includes:

- Month labels across the top.
- Week rows labeled Sun..Sat with colored blocks for each day.
- A legend showing color intensity (less → more contributions).
- Date range, total contributions count and the current streak in days.

## Colors / Legend

The program uses ANSI background color blocks for contrast. If your terminal supports 256 colors you will see four green intensity levels and a dark gray "empty" block. If colors don't display correctly, try a different terminal or ensure TERM supports 256 colors (for example: `export TERM=xterm-256color`).

## Notes

- The tool scrapes the contributions HTML for the given user path: `https://github.com/users/<username>/contributions`.
- GitHub may rate-limit or change their HTML structure; if output appears empty or incorrect, inspect the page HTML and adjust parsing accordingly.
- The program attempts to parse tooltip text to compute the total contributions; if GitHub changes tooltip wording this number may be inaccurate.

## Troubleshooting

- "No contributions found or user doesn't exist": the contributions grid was empty or the username/page is unavailable.
- Network errors will be printed to stderr; check connectivity and try again.

## License

MIT

