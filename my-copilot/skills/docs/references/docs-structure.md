## Standard Documentation Structure

### Minimal (all projects)
```
docs/
├── README.md              # What is this? How to use it?
└── getting-started.md     # Setup, install, run
```

### Standard (most projects)
```
docs/
├── README.md
├── architecture.md        # System design, data flow
├── getting-started.md     # Setup & development
└── api-reference.md       # API endpoints / public API
```

### Extended (complex projects)
```
docs/
├── README.md
├── architecture.md
├── getting-started.md
├── api-reference.md
├── deployment-guide.md    # CI/CD, hosting, environments
├── code-standards.md      # Conventions, patterns
└── contributing.md        # How to contribute
```

### Template: README.md
```markdown
# {Project Name}

{One-line description}

## Features
- Feature 1
- Feature 2

## Quick Start
\`\`\`bash
# Install
{install command}

# Run
{run command}
\`\`\`

## Documentation
- [Architecture](docs/architecture.md)
- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api-reference.md)

## License
{License type}
```

### Template: architecture.md
```markdown
# Architecture

## Overview
{High-level system description}

## Components
{Component diagram or list}

## Data Flow
{How data moves through the system}

## Key Decisions
{Important architectural decisions and rationale}
```
