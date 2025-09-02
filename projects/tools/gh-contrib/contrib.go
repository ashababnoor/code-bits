package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	"strconv"
)

// Day holds the date and contribution count
type Day struct {
	Date  string
	Count int
}

func getContributions(username string) ([]Day, error) {
	url := fmt.Sprintf("https://github.com/users/%s/contributions", username)
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", "go-github-cli")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	content := string(bodyBytes)

	// Regex to match "N contributions on Month Day, Year" or "No contributions on ..."
	re := regexp.MustCompile(`(\d+|No contributions) contributions on ([A-Za-z]+ \d{1,2}(?:st|nd|rd|th)?(?:, \d{4})?)`)
	matches := re.FindAllStringSubmatch(content, -1)

	var days []Day
	for _, m := range matches {
		var cnt int
		if m[1] == "No contributions" {
			cnt = 0
		} else {
			cnt, _ = strconv.Atoi(m[1])
		}
		days = append(days, Day{Date: m[2], Count: cnt})
	}
	return days, nil
}

func mapLevel(count int) int {
	switch {
	case count == 0:
		return 0
	case count < 5:
		return 1
	case count < 20:
		return 2
	case count < 50:
		return 3
	default:
		return 4
	}
}

func colorBlock(level int) string {
	switch level {
	case 0:
		return "\033[48;5;232m  \033[0m"
	case 1:
		return "\033[48;5;120m  \033[0m"
	case 2:
		return "\033[48;5;34m  \033[0m"
	case 3:
		return "\033[48;5;22m  \033[0m"
	case 4:
		return "\033[48;5;28m  \033[0m"
	default:
		return "\033[48;5;232m  \033[0m"
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: contrib <github-username>")
		os.Exit(1)
	}
	username := os.Args[1]

	days, err := getContributions(username)
	if err != nil {
		fmt.Println("Error fetching contributions:", err)
		os.Exit(1)
	}

	// We only have a flat list of days. To simulate the grid, we chunk by weeks:
	const daysPerWeek = 7
	var weeks [][]Day
	for i := 0; i < len(days); i += daysPerWeek {
		end := i + daysPerWeek
		if end > len(days) {
			end = len(days)
		}
		weeks = append(weeks, days[i:end])
	}

	// Render 7 rows (each row = a day-of-week)
	for row := 0; row < daysPerWeek; row++ {
		for _, week := range weeks {
			if row < len(week) {
				level := mapLevel(week[row].Count)
				fmt.Print(colorBlock(level))
			} else {
				fmt.Print("  ")
			}
		}
		fmt.Println()
	}
}
