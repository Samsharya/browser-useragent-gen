# User Agent Generator

A lightweight tool to generate, filter, and export browser user-agent profiles. Standard library only—no external dependencies required.





---

## Installation

Clone the repository and ensure Python 3.x is available on your path:

```bash
git clone https://github.com/username/repository.name.git
cd repository.name
```

---

## Quick Start / Running Methods

### Interactive Bash Shell
Run the shell runner for interactive selection:
```bash
chmod +x ua.sh
./ua.sh
```

Launch the interactive Python-based terminal runner:
```bash
python3 run.py
```

### Direct CLI Commands
Use `ua.py` directly to generate output on standard output or write to files:

- **List available profiles:**
  ```bash
  python3 ua.py list
  ```

- **Generate 5 random user agents:**
  ```bash
  python3 ua.py random -n 5
  ```

- **Filter by browser and export to JSON:**
  ```bash
  python3 ua.py random --browser chrome --count 3 --format json --output chrome_agents.json
  ```

- **Generate targeted combination:**
  ```bash
  python3 ua.py generate --browser firefox --os linux --device desktop --count 2 --format csv -o firefox_linux.csv
  ```

---

## Command-Line Syntax

```bash
python3 ua.py {random|generate|list} [OPTIONS]
```

### Subcommands

#### 1. `random`
Selects profiles at random based on optional filters.

```bash
python3 ua.py random [--browser BROWSER] [--os OS] [--device DEVICE] [--count COUNT] [--format FORMAT] [--output OUTPUT] [--seed SEED]
```

#### 2. `generate`
Generates profiles matching explicit parameters.

```bash
python3 ua.py generate --browser BROWSER --os OS [--device DEVICE] [--version VERSION] [--count COUNT] [--format FORMAT] [--output OUTPUT] [--seed SEED]
```

#### 3. `list`
Prints available profiles and metadata to stdout.

```bash
python3 ua.py list
```


### Uses:

* Web scraping and anti-bot evasion
* Multi-browser and cross-platform compatibility testing
* Traffic log generation and parser testing
* Reproducible QA test automation
* Platform and device environment simulation

## Features

- Curated profiles spanning Chrome, Firefox, Edge, Safari, and Opera across Windows, macOS, Linux, Android, and iOS.
- Interactive CLI scripts (`ua.sh` and `run.py`) and direct command-line execution (`ua.py`).
- Reproducible random selection via custom seeds.
- Export options: Plaintext (`TXT`), formatted `JSON`, or `CSV`.

---

## Available Options

| Option | Command | Description | Accepted Values |
| :--- | :--- | :--- | :--- |
| `--browser` | `random`, `generate` | Filter by browser type | `chrome`, `firefox`, `edge`, `safari`, `opera` |
| `--os` | `random`, `generate` | Filter by OS | `windows`, `macos`, `linux`, `android`, `ios` |
| `--device` | `random`, `generate` | Filter by device category | `desktop`, `mobile`, `tablet` |
| `--count`, `-n` | `random`, `generate` | Number of items to generate | Positive integer (default: `1`) |
| `--format` | `random`, `generate` | Output format | `txt`, `json`, `csv` (default: `txt`) |
| `--output`, `-o` | `random`, `generate` | Output path | File path |
| `--seed` | `random`, `generate` | Integer seed for deterministic generation | Integer |

---

## File Structure

```text
.
├── exporter.py    # Formatter and file output handler
├── run.py         # Python interactive menu interface
├── ua.py          # Main CLI tool and profile definitions
└── ua.sh          # Bash wrapper script
```