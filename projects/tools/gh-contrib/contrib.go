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

const (
	userAgent string = "GitHubContributionsCLI/1.0"
)

type Week struct {
	start time.Time
	end   time.Time
}

func (w Week) String() string {
	return fmt.Sprintf("%s - %s", w.start.Format("2006-01-02"), w.end.Format("2006-01-02"))
}

func (w Week) GetMonth() Month {
	middleOfWeek := w.start.AddDate(0, 0, 3)
	return Month{
		year:  middleOfWeek.Year(),
		month: middleOfWeek.Month(),
		label: middleOfWeek.Format("Jan"),
	}
}

type Month struct {
	year  int
	month time.Month
	label string
}

func (m Month) String() string {
	return fmt.Sprintf("%d-%02d (%s)", m.year, int(m.month), m.label)
}

// ANSI color blocks with better contrast
var (
	colorEmpty  = "\033[48;5;235m  \033[0m" // dark gray (more like GitHub)
	colorLevel1 = "\033[48;5;29m  \033[0m"  // dark green
	colorLevel2 = "\033[48;5;36m  \033[0m"  // medium green
	colorLevel3 = "\033[48;5;42m  \033[0m"  // bright green
	colorLevel4 = "\033[48;5;47m  \033[0m"  // very bright green
)

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
		return colorEmpty
	}
}

func getContributions(username string) (map[string]int, error) {
	url := fmt.Sprintf("https://github.com/users/%s/contributions", username)

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", userAgent)

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

func getMonthLabels(start time.Time, weeks int) map[Week]string {
	labels := make(map[Week]string)

	for week := 0; week < weeks; week++ {
		startOfWeek := start.AddDate(0, 0, week*7)
		middleOfWeek := startOfWeek.AddDate(0, 0, 3)
		endOfWeek := startOfWeek.AddDate(0, 0, 6)

		labels[Week{start: startOfWeek, end: endOfWeek}] = middleOfWeek.Format("Jan")
	}
	return labels
}

func printMonthLabels(labels map[Week]string) {
	fmt.Print("    ") // Space for weekday labels

	var months []Month
	for week, label := range labels {
		middleOfWeek := week.start.AddDate(0, 0, 3)
		months = append(months, Month{
			year:  middleOfWeek.Year(),
			month: middleOfWeek.Month(),
			label: label,
		})
	}

	labelSizes := make(map[Month]int64)
	for _, month := range months {
		if size, found := labelSizes[month]; !found {
			labelSizes[month] = size
		}
		labelSizes[month] += 2
	}

	weeks := make([]Week, 0, len(labels))
	for week := range labels {
		weeks = append(weeks, week)
	}

	sort.Slice(weeks, func(i, j int) bool { return weeks[i].start.Before(weeks[j].start) })

	labelString := ""
	lastLabel := "abc" // Initialize with a value that won't match any month label
	for i := 0; i < len(weeks); i++ {
		week := weeks[i]
		month := week.GetMonth()
		label := month.label
		labelSize := labelSizes[month]

		if len(label) > int(labelSize) {
			label = ""
		}
		if label != lastLabel {
			labelString += fmt.Sprintf("%-*s", labelSize, label)
			lastLabel = label
		}
	}

	fmt.Println(labelString)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: ghcontrib <github-username>")
		os.Exit(1)
	}
	username := os.Args[1]

	fmt.Printf("GitHub Contributions for @%s\n\n", username)

	contribs, err := getContributions(username)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

	if len(contribs) == 0 {
		fmt.Println("No contributions found or user doesn't exist")
		os.Exit(0)
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

	// Generate month labels
	monthLabels := getMonthLabels(start, weeks)

	// Print month labels
	printMonthLabels(monthLabels)

	weekdays := []string{"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}

	// Print the grid with better spacing
	for row := 0; row < 7; row++ {
		// Print weekday label on first column
		fmt.Printf("%-4s", weekdays[row])

		for col := 0; col < weeks; col++ {
			fmt.Print(colorBlock(grid[row][col]))
		}
		fmt.Println()
	}

	// Print legend
	fmt.Println("\nLegend:")
	fmt.Printf("Less %s%s%s%s More\n", colorLevel1, colorLevel2, colorLevel3, colorLevel4)

	// Calculate and display total contributions
	total := 0
	for _, level := range contribs {
		// Convert level to approximate contribution count
		switch level {
		case 1:
			total += 1
		case 2:
			total += 4
		case 3:
			total += 8
		case 4:
			total += 12
		}
	}
	fmt.Printf("\nTotal contributions: %d\n", total)

	// Show date range
	fmt.Printf("Date range: %s to %s\n",
		dates[0].Format("Jan 2, 2006"),
		dates[len(dates)-1].Format("Jan 2, 2006"))

	// Show current streak (simplified)
	currentStreak := 0
	today := time.Now().Format("2006-01-02")
	yesterday := time.Now().AddDate(0, 0, -1).Format("2006-01-02")

	if contribs[today] > 0 {
		currentStreak++
	}
	if contribs[yesterday] > 0 {
		currentStreak++
	}

	if currentStreak > 0 {
		fmt.Printf("Current streak: %d days\n", currentStreak)
	}
}
