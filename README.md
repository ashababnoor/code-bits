# Code Bits

Random code bits that I've written for various purposes that don't deserve their own repo.  
Once a project gets too big they will be moved to their own repository.

### Repository Structure
```
.
├── experiments
│   ├── django
│   │   ├── django-poll-app
│   │   └── google-api-demo
│   ├── postgres
│   │   └── postgres-python-client
│   ├── redis
│   │   └── redis-python-client
│   └── sass
│       └── sass-portfolio
├── projects
│   ├── apps
│   │   └── binary-calculator
│   ├── games
│   │   ├── connect-four
│   │   └── math-quiz
│   └── tools
│       ├── data-tools *
│       ├── emailer
│       ├── etl-tools *
│       ├── map-route-visualizer
│       ├── py-utils
│       ├── string-cleaner
│       └── svg-to-jpg-converter
├── shell-scripts
└── simulations
```

*Note:* Marked with `*` indicates moved to or being maintained in a different repository


### Moved Projects
| Project      |  Repository                                                         |
|:-------------|:--------------------------------------------------------------------|
| `data-tools` | [ashababnoor/data-tools](https://github.com/ashababnoor/data-tools) |
| `etl-tools`  | [ashababnoor/data-tools](https://github.com/ashababnoor/etl-tools)  |


### Extra
Generated directory tree using the following command
```bash
tree -L 3 -I venv -d
```