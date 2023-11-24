# Code Bits

Random code bits that I've written for various purposes that don't deserve their own repo.  
Once a project gets too big they will be moved to their own repository.

**Repository Structure**
```
.
├── data-science
│   └── natural-language-processing
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
│       ├── bigquery-schema-comparer *
│       ├── bigquery-to-redis-ingestor
│       ├── json-to-markdown-converter *
│       ├── mysql-postgres-etl
│       ├── py-utils
│       ├── string-cleaner
│       └── svg-to-jpg-converter
├── shell-scripts
└── simulations
```

*Note:* Marked with `*` indicates moved to or being maintained in different repository

Generated directory tree using the following command
```bash
tree -L 3 -I venv -d
```