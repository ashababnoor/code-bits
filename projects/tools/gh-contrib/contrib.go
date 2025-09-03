package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"

	"golang.org/x/net/html"
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

	// Print some sample entries
	for date, lvl := range contribs {
		fmt.Printf("%s => level %d\n", date, lvl)
	}
}
