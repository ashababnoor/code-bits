# Conway's Game of Life (terminal)

Small terminal-based Conway's Game of Life implementation in Go.

Features
- Configurable grid size, speed, wrapping edges
- Random seeding or place a simple `glider` pattern or load a text pattern
- ANSI rendering using full-block characters

Build
```bash
go build -o golife main.go
```

Run
```bash
# random 80x24 grid, 200ms between generations
./golife -w 80 -h 24 -ms 200

# run with a glider pattern
./golife -w 40 -h 20 -pattern glider

# load a pattern from a file (simple text with O or * as live cells)
./golife -pattern patterns/my_pattern.txt

# run for a fixed number of generations
./golife -gens 200
```

Flags
- `-w` width (default 80)
- `-h` height (default 24)
- `-ms` interval in milliseconds between generations (default 200)
- `-p` random fill probability (default 0.15)
- `-seed` random seed (0 = time.Now())
- `-gens` number of generations (0 = infinite)
- `-wrap` wrap edges (toroidal) default true
- `-pattern` builtin `glider` or path to a simple text pattern file

Notes
- Use Ctrl+C to quit; the cursor will be restored on exit.
- Text pattern files should be lines of characters where `O`, `X`, `*`, or `1` denote live cells.

License: MIT
