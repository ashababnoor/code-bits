package main

import (
	"fmt"
	"net/http"
	"os"
	"sort"
	"strconv"
	"time"

	"golang.org/x/net/html"
)

// ANSI color blocks
var (
	colorEmpty  = "\033[48;5;232m  \033[0m" // gray/black
	colorLevel1 = "\033[48;5;28m  \033[0m"  // very dark green
	colorLevel2 = "\033[48;5;22m  \033[0m"  // dark green
	colorLevel3 = "\033[48;5;34m  \033[0m"  // medium green
	colorLevel4 = "\033[48;5;120m  \033[0m" // light green
	colorNoCell = "\033[0m \033[0m"
)

func getContributions(username string) (map[string]int, error) {
	url := fmt.Sprintf("https://github.com/users/%s/contributions", username)

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", "go-contrib-cli")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	doc, err := html.Parse(resp.Body)
	if err != nil {
		return nil, err
	}

	results := make(map[string]int)

	var traverse func(*html.Node)
	traverse = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "td" {
			var date string
			var level int
			for _, attr := range n.Attr {
				switch attr.Key {
				case "data-date":
					date = attr.Val
				case "data-level":
					if val, err := strconv.Atoi(attr.Val); err == nil {
						level = val
					}
				}
			}
			if date != "" {
				results[date] = level
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			traverse(c)
		}
	}
	traverse(doc)

	return results, nil
}

func colorBlock(level int) string {
	switch level {
	case 0:
		return colorEmpty
	case 1:
		return colorLevel1
	case 2:
		return colorLevel2
	case 3:
		return colorLevel3
	case 4:
		return colorLevel4
	default:
		return colorNoCell
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: contrib <github-username>")
		os.Exit(1)
	}
	username := os.Args[1]

	contribs, err := getContributions(username)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

	// Extract and sort dates
	dates := make([]time.Time, 0, len(contribs))
	for d := range contribs {
		t, err := time.Parse("2006-01-02", d)
		if err == nil {
			dates = append(dates, t)
		}
	}
	sort.Slice(dates, func(i, j int) bool { return dates[i].Before(dates[j]) })

	// Build grid: rows = weekdays (Sun=0 ... Sat=6), cols = weeks
	start := dates[0]
	// align start to previous Sunday
	offset := int(start.Weekday())
	start = start.AddDate(0, 0, -offset)

	end := dates[len(dates)-1]
	// align end to next Saturday
	offset = 6 - int(end.Weekday())
	end = end.AddDate(0, 0, offset)

	weeks := int(end.Sub(start).Hours()/24/7) + 1
	grid := make([][]int, 7)
	for i := range grid {
		grid[i] = make([]int, weeks)
	}

	// Fill grid
	for i := 0; i < weeks*7; i++ {
		d := start.AddDate(0, 0, i)
		week := i / 7
		day := int(d.Weekday())
		if lvl, ok := contribs[d.Format("2006-01-02")]; ok {
			grid[day][week] = lvl
		} else {
			grid[day][week] = 0
		}
	}

	// Print rows (Sun=top row, Sat=bottom)
	for row := 0; row < 7; row++ {
		for col := 0; col < weeks; col++ {
			fmt.Print(colorBlock(grid[row][col]))
		}
		fmt.Println()
	}
}
