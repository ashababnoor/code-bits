package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/fatih/color"
)

type Contribution struct {
	Date  time.Time
	Count int
	Level int // 0-4 based on count
}

func main() {
	username := flag.String("user", "", "GitHub username")
	flag.Parse()

	if *username == "" {
		log.Fatal("Please provide a GitHub username with -user flag")
	}

	contributions, err := fetchContributions(*username)
	if err != nil {
		log.Fatal(err)
	}

	displayGraph(contributions, *username)
}

func fetchContributions(username string) ([]Contribution, error) {
	url := fmt.Sprintf("https://github.com/users/%s/contributions", username)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("failed to fetch contributions: %s", resp.Status)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, err
	}

	var contributions []Contribution

	// Find the contribution calendar
	doc.Find(".ContributionCalendar-day").Each(func(i int, s *goquery.Selection) {
		data, _ := s.Attr("data-date")
		levelStr, _ := s.Attr("data-level")

		if data == "" {
			return
		}

		date, err := time.Parse("2006-01-02", data)
		if err != nil {
			return
		}

		level, _ := strconv.Atoi(levelStr)

		// For count, since data-count is empty, use level as approximate count
		count := level

		contributions = append(contributions, Contribution{
			Date:  date,
			Count: count,
			Level: level,
		})
	})

	return contributions, nil
}

func displayGraph(contributions []Contribution, username string) {
	if len(contributions) == 0 {
		fmt.Println("No contributions found.")
		return
	}

	// Display the graph
	// For simplicity, display last 52 weeks
	current := time.Now().UTC()
	start := current.AddDate(0, 0, -52*7)

	// Get weekday names
	weekdays := []string{"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}

	// Print header
	fmt.Printf("GitHub Contributions for %s\n", username)
	fmt.Println()

	// Print weekdays
	for _, wd := range weekdays {
		fmt.Printf("%s ", wd)
	}
	fmt.Println()

	// Find the starting weekday
	startWeekday := int(start.Weekday())
	if startWeekday == 0 {
		startWeekday = 7 // Sunday is 0, but we want 7
	}
	startWeekday-- // Adjust for Monday start

	// Print the graph
	day := time.Date(start.Year(), start.Month(), start.Day(), 0, 0, 0, 0, time.UTC)
	currentMidnight := time.Date(current.Year(), current.Month(), current.Day(), 0, 0, 0, 0, time.UTC)
	for day.Before(currentMidnight) {
		weekday := int(day.Weekday())
		if weekday == 0 {
			weekday = 7
		}
		weekday--

		if weekday == 0 {
			// New week
			fmt.Println()
		}

		// Find contribution for this day
		found := false
		for _, c := range contributions {
			if c.Date.Equal(day) {
				printContribution(c)
				found = true
				break
			}
		}
		if !found {
			printContribution(Contribution{Count: 0, Level: 0})
		}

		day = day.AddDate(0, 0, 1)
	}
	fmt.Println()
}

func printContribution(c Contribution) {
	var col *color.Color
	switch c.Level {
	case 0:
		col = color.New(color.FgWhite)
	case 1:
		col = color.New(color.FgGreen)
	case 2:
		col = color.New(color.FgGreen).Add(color.Bold)
	case 3:
		col = color.New(color.FgYellow).Add(color.Bold)
	case 4:
		col = color.New(color.FgRed).Add(color.Bold)
	default:
		col = color.New(color.FgWhite)
	}

	col.Print("■ ")
}
