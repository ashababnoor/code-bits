package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"
)

const (
	githubURL = "https://github.com/users/%s/contributions"
)

type ContributionDay struct {
	Date  time.Time
	Level int
	Count int
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: github-contrib <username>")
		os.Exit(1)
	}

	username := os.Args[1]
	contributions, err := fetchContributions(username)
	if err != nil {
		fmt.Printf("Error fetching contributions: %v\n", err)
		os.Exit(1)
	}

	displayContributionsGraph(contributions, username)
}

func fetchContributions(username string) ([]ContributionDay, error) {
	url := fmt.Sprintf(githubURL, username)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP error: %s", resp.Status)
	}

	return parseContributions(resp.Body)
}

func parseContributions(body io.Reader) ([]ContributionDay, error) {
	var contributions []ContributionDay
	scanner := bufio.NewScanner(body)

	// Regex to match contribution day elements
	dayRegex := regexp.MustCompile(`data-date="(\d{4}-\d{2}-\d{2})" data-level="(\d+)"`)
	tooltipRegex := regexp.MustCompile(`(\d+) contributions? on`)

	for scanner.Scan() {
		line := scanner.Text()

		// Look for contribution day elements
		if strings.Contains(line, "ContributionCalendar-day") {
			matches := dayRegex.FindStringSubmatch(line)
			if len(matches) == 3 {
				dateStr := matches[1]
				level := matches[2]

				date, err := time.Parse("2006-01-02", dateStr)
				if err != nil {
					continue
				}

				// Default count based on level
				count := 0
				switch level {
				case "1":
					count = 1
				case "2":
					count = 4
				case "3":
					count = 8
				case "4":
					count = 12
				}

				contributions = append(contributions, ContributionDay{
					Date:  date,
					Level: parseInt(level),
					Count: count,
				})
			}
		}

		// Try to get exact count from tooltip if available
		if strings.Contains(line, "tooltip") && strings.Contains(line, "contributions") {
			matches := tooltipRegex.FindStringSubmatch(line)
			if len(matches) == 2 {
				count := parseInt(matches[1])
				if len(contributions) > 0 {
					contributions[len(contributions)-1].Count = count
				}
			}
		}
	}

	return contributions, scanner.Err()
}

func displayContributionsGraph(contributions []ContributionDay, username string) {
	if len(contributions) == 0 {
		fmt.Printf("No contributions found for user: %s\n", username)
		return
	}

	// Group contributions by week
	weeks := groupByWeek(contributions)

	fmt.Printf("GitHub Contributions for %s:\n\n", username)
	fmt.Println("Sun Mon Tue Wed Thu Fri Sat")

	for _, week := range weeks {
		for i, day := range week {
			if i > 0 {
				fmt.Print(" ")
			}
			fmt.Print(getDaySymbol(day))
		}
		fmt.Println()
	}

	fmt.Println("\nLegend:")
	fmt.Println("░ - No contributions")
	fmt.Println("░ - 1-3 contributions")
	fmt.Println("▒ - 4-7 contributions")
	fmt.Println("▓ - 8-11 contributions")
	fmt.Println("█ - 12+ contributions")
}

func groupByWeek(contributions []ContributionDay) [][]ContributionDay {
	var weeks [][]ContributionDay
	var currentWeek []ContributionDay

	// Start from the first contribution date
	if len(contributions) == 0 {
		return weeks
	}

	firstDate := contributions[0].Date
	startOfWeek := firstDate.AddDate(0, 0, -int(firstDate.Weekday()))

	// Create a map for quick lookup
	contributionMap := make(map[string]ContributionDay)
	for _, day := range contributions {
		contributionMap[day.Date.Format("2006-01-02")] = day
	}

	// Generate 52 weeks of data
	for week := 0; week < 52; week++ {
		currentWeek = nil
		for day := 0; day < 7; day++ {
			currentDate := startOfWeek.AddDate(0, 0, week*7+day)
			dateKey := currentDate.Format("2006-01-02")

			if contrib, exists := contributionMap[dateKey]; exists {
				currentWeek = append(currentWeek, contrib)
			} else {
				currentWeek = append(currentWeek, ContributionDay{
					Date:  currentDate,
					Level: 0,
					Count: 0,
				})
			}
		}
		weeks = append(weeks, currentWeek)
	}

	return weeks
}

func getDaySymbol(day ContributionDay) string {
	switch {
	case day.Count == 0:
		return "░" // Light shade - no contributions
	case day.Count <= 3:
		return "░" // Light shade - 1-3 contributions
	case day.Count <= 7:
		return "▒" // Medium shade - 4-7 contributions
	case day.Count <= 11:
		return "▓" // Dark shade - 8-11 contributions
	default:
		return "█" // Full block - 12+ contributions
	}
}

func parseInt(s string) int {
	var n int
	fmt.Sscanf(s, "%d", &n)
	return n
}
