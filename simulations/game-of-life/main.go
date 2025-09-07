package main

import (
	"bufio"
	"flag"
	"fmt"
	"math/rand"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"
)

var (
	width     = flag.Int("w", 80, "grid width")
	height    = flag.Int("h", 24, "grid height")
	interval  = flag.Int("ms", 200, "millisecond delay between generations")
	prob      = flag.Float64("p", 0.15, "random fill probability for live cells (0..1)")
	seed      = flag.Int64("seed", 0, "random seed (0 = time.Now())")
	gens      = flag.Int("gens", 0, "number of generations to run (0 = infinite)")
	wrapEdges = flag.Bool("wrap", true, "toroidal (wrap) edges")
	pattern   = flag.String("pattern", "", "builtin pattern name (glider) or path to simple text pattern file")
)

type Grid struct {
	w, h  int
	cells []bool
}

func NewGrid(w, h int) *Grid {
	return &Grid{w: w, h: h, cells: make([]bool, w*h)}
}

func (g *Grid) idx(x, y int) int {
	return y*g.w + x
}

func (g *Grid) Get(x, y int) bool {
	if x < 0 || x >= g.w || y < 0 || y >= g.h {
		return false
	}
	return g.cells[g.idx(x, y)]
}

func (g *Grid) Set(x, y int, v bool) {
	if x < 0 || x >= g.w || y < 0 || y >= g.h {
		return
	}
	g.cells[g.idx(x, y)] = v
}

func (g *Grid) CountNeighbors(x, y int, wrap bool) int {
	count := 0
	for dy := -1; dy <= 1; dy++ {
		for dx := -1; dx <= 1; dx++ {
			if dx == 0 && dy == 0 {
				continue
			}
			nx := x + dx
			ny := y + dy
			if wrap {
				nx = (nx%g.w + g.w) % g.w
				ny = (ny%g.h + g.h) % g.h
			}
			if nx < 0 || nx >= g.w || ny < 0 || ny >= g.h {
				continue
			}
			if g.Get(nx, ny) {
				count++
			}
		}
	}
	return count
}

func (g *Grid) Step(wrap bool) *Grid {
	ng := NewGrid(g.w, g.h)
	for y := 0; y < g.h; y++ {
		for x := 0; x < g.w; x++ {
			n := g.CountNeighbors(x, y, wrap)
			alive := g.Get(x, y)
			if alive {
				if n == 2 || n == 3 {
					ng.Set(x, y, true)
				} else {
					ng.Set(x, y, false)
				}
			} else {
				if n == 3 {
					ng.Set(x, y, true)
				}
			}
		}
	}
	return ng
}

func (g *Grid) Render() string {
	var b strings.Builder
	for y := 0; y < g.h; y++ {
		for x := 0; x < g.w; x++ {
			if g.Get(x, y) {
				b.WriteRune('█')
			} else {
				b.WriteRune(' ')
			}
		}
		if y < g.h-1 {
			b.WriteRune('\n')
		}
	}
	return b.String()
}

func seedRandom(g *Grid, p float64) {
	for i := range g.cells {
		g.cells[i] = rand.Float64() < p
	}
}

func placePattern(g *Grid, lines []string, ox, oy int) {
	for y, ln := range lines {
		for x, ch := range ln {
			if ch == 'O' || ch == '1' || ch == 'X' || ch == '*' {
				g.Set(ox+x, oy+y, true)
			}
		}
	}
}

func loadSimplePattern(path string) ([]string, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return lines, nil
}

func clearScreen() {
	fmt.Print("\x1b[H\x1b[2J")
}

func hideCursor() { fmt.Print("\x1b[?25l") }
func showCursor() { fmt.Print("\x1b[?25h") }

func main() {
	flag.Parse()

	if *width <= 0 || *height <= 0 {
		fmt.Fprintln(os.Stderr, "invalid width/height")
		os.Exit(2)
	}

	if *seed == 0 {
		*seed = time.Now().UnixNano()
	}
	rand.Seed(*seed)

	g := NewGrid(*width, *height)

	// pattern placement or random seed
	if *pattern != "" {
		if *pattern == "glider" {
			// small glider centred
			p := []string{
				" O",
				"  O",
				"OOO",
			}
			placePattern(g, p, g.w/2-1, g.h/2-1)
		} else {
			if lines, err := loadSimplePattern(*pattern); err == nil {
				placePattern(g, lines, 0, 0)
			} else {
				fmt.Fprintf(os.Stderr, "failed loading pattern '%s': %v\n", *pattern, err)
				os.Exit(1)
			}
		}
	} else {
		seedRandom(g, *prob)
	}

	// setup signal handler to restore cursor on exit
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sig
		showCursor()
		fmt.Println()
		os.Exit(0)
	}()

	hideCursor()
	defer showCursor()

	ticker := time.NewTicker(time.Duration(*interval) * time.Millisecond)
	defer ticker.Stop()

	gen := 0
	for {
		clearScreen()
		fmt.Printf("Conway's Game of Life — gen=%d (seed=%d) — w=%d h=%d\n", gen, *seed, g.w, g.h)
		fmt.Println(g.Render())

		gen++
		if *gens > 0 && gen >= *gens {
			break
		}

		<-ticker.C
		g = g.Step(*wrapEdges)
	}
}
