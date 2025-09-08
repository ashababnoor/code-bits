package main

import (
	"fmt"
	"net/http"
	"os"
	"sort"
	"strconv"
	"strings"
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

	colorEmptyWithLabel  = "\033[38;5;235m\033[48;5;235m 0\033[0m" // dark gray (more like GitHub)
	colorLevel1WithLabel = "\033[38;5;29m\033[48;5;29m 1\033[0m"   // dark green
	colorLevel2WithLabel = "\033[38;5;36m\033[48;5;36m 2\033[0m"   // medium green
	colorLevel3WithLabel = "\033[38;5;42m\033[48;5;42m 3\033[0m"   // bright green
	colorLevel4WithLabel = "\033[38;5;47m\033[48;5;47m 4\033[0m"   // very bright green
)

func colorBlock(level int, showLabel bool) string {
	switch level {
	case 0:
		if showLabel {
			return colorEmptyWithLabel
		}
		return colorEmpty
	case 1:
		if showLabel {
			return colorLevel1WithLabel
		}
		return colorLevel1
	case 2:
		if showLabel {
			return colorLevel2WithLabel
		}
		return colorLevel2
	case 3:
		if showLabel {
			return colorLevel3WithLabel
		}
		return colorLevel3
	case 4:
		if showLabel {
			return colorLevel4WithLabel
		}
		return colorLevel4
	default:
		return colorEmpty
	}
}

func parseContributionLevels(doc *html.Node) map[string]int {
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

	return results
}

func getDayWiseContributions(doc *html.Node) map[string]int {
	seen := make(map[string]bool)
	contributions := make(map[string]int)

	// parseTooltipText extracts a date (YYYY-MM-DD) and count from the tooltip text.
	parseTooltipText := func(text string) (string, int, bool) {
		text = strings.TrimSpace(text)
		if strings.HasPrefix(text, "No contributions") {
			return "", 0, false
		}
		if !strings.Contains(text, "contribution") {
			return "", 0, false
		}

		var count int
		var monthStr string
		var day int
		if _, err := fmt.Sscanf(text, "%d contributions on %s %d", &count, &monthStr, &day); err == nil {
			dateStr := fmt.Sprintf("%s %d, %d", monthStr, day, time.Now().Year())
			if t, err := time.Parse("January 2, 2006", dateStr); err == nil {
				return t.Format("2006-01-02"), count, true
			}
		}
		return "", 0, false
	}

	// getNodeText returns the concatenated text of the node's immediate text children.
	getNodeText := func(n *html.Node) string {
		var sb strings.Builder
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			if c.Type == html.TextNode {
				sb.WriteString(c.Data)
			}
		}
		return sb.String()
	}

	// iterative traversal using a queue to avoid deep recursion nesting
	queue := []*html.Node{doc}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]

		if node.Type == html.ElementNode && node.Data == "tool-tip" {
			text := getNodeText(node)
			if date, count, ok := parseTooltipText(text); ok {
				if !seen[date] {
					contributions[date] = count
					seen[date] = true
				}
			}
		}

		for c := node.FirstChild; c != nil; c = c.NextSibling {
			queue = append(queue, c)
		}
	}

	return contributions
}

func getTotalContributions(contributions map[string]int) int {
	total := 0
	for _, count := range contributions {
		total += count
	}
	return total
}

func getLastDateContributions(contributions map[string]int) (string, int, bool) {
	var lastDate string
	var lastCount int
	for date, count := range contributions {
		if date > lastDate {
			lastDate = date
			lastCount = count
		}
	}
	if lastDate == "" {
		return "", 0, false
	}
	return lastDate, lastCount, true
}

func getContributionData(username string) (map[string]int, map[string]int, int, error) {
	url := fmt.Sprintf("https://github.com/users/%s/contributions", username)

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", userAgent)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, nil, 0, err
	}
	defer resp.Body.Close()

	doc, err := html.Parse(resp.Body)
	if err != nil {
		return nil, nil, 0, err
	}

	contributionLevels := parseContributionLevels(doc)

	contributions := getDayWiseContributions(doc)
	totalContribution := getTotalContributions(contributions)

	return contributionLevels, contributions, totalContribution, nil
}

func getWeekMonthMapping(start time.Time, weeks int) map[Week]string {
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

func computeCurrentStreak(contribs map[string]int) int {
	const layout = "2006-01-02"

	// Find the latest date present in the map.
	var max time.Time
	first := true
	for ds := range contribs {
		t, err := time.Parse(layout, ds)
		if err != nil {
			continue
		}
		if first || t.After(max) {
			max = t
			first = false
		}
	}
	if first { // map was empty or all parse failures
		return 0
	}

	// Count consecutive days with level > 0, ending at the latest date.
	streak := 0
	for d := max; ; d = d.AddDate(0, 0, -1) {
		val, ok := contribs[d.Format(layout)]
		if !ok {
			break // outside the dataset window
		}
		if val <= 0 {
			break // streak broken
		}
		streak++
	}
	return streak
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: ghcontrib <github-username>")
		os.Exit(1)
	}
	username := os.Args[1]
	showLabel := false

	if len(os.Args) >= 3 && os.Args[2] == "--show-label" {
		showLabel = true
	}

	fmt.Printf("GitHub Contributions for @%s\n\n", username)

	contribLevels, contributions, contribCount, err := getContributionData(username)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

	if len(contribLevels) == 0 {
		fmt.Println("No contributions found or user doesn't exist")
		os.Exit(0)
	}

	// Extract and sort dates
	dates := make([]time.Time, 0, len(contribLevels))
	for d := range contribLevels {
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
		if lvl, ok := contribLevels[d.Format("2006-01-02")]; ok {
			grid[day][week] = lvl
		} else {
			grid[day][week] = 0
		}
	}

	// Generate week month mapping
	weekMonthMapping := getWeekMonthMapping(start, weeks)

	// Print month labels
	printMonthLabels(weekMonthMapping)

	weekdays := []string{"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}

	// Print the grid with better spacing
	for row := 0; row < 7; row++ {
		// Print weekday label on first column
		fmt.Printf("%-4s", weekdays[row])

		for col := 0; col < weeks; col++ {
			fmt.Print(colorBlock(grid[row][col], showLabel))
		}
		fmt.Println()
	}

	// Print legend
	fmt.Println("\nLegend:")
	if showLabel {
		fmt.Printf("Less %s%s%s%s More\n", colorLevel1WithLabel, colorLevel2WithLabel, colorLevel3WithLabel, colorLevel4WithLabel)
	} else {
		fmt.Printf("Less %s%s%s%s More\n", colorLevel1, colorLevel2, colorLevel3, colorLevel4)
	}

	// Show date range
	fmt.Printf("\nDate range: %s to %s\n",
		dates[0].Format("Jan 2, 2006"),
		dates[len(dates)-1].Format("Jan 2, 2006"))

	// Calculate and display total contributions
	fmt.Printf("Total contributions: %d\n", contribCount)

	// Show current streak
	currentStreak := computeCurrentStreak(contribLevels)
	fmt.Printf("Current streak: %d days\n", currentStreak)

	if _, lastCount, ok := getLastDateContributions(contributions); ok {
		fmt.Printf("Last date contributions: %d\n", lastCount)
	}
}
