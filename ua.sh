
#!/usr/bin/env bash

# Browser UA Generator
# Terminal interface for ua.py

set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: Python was not found."
    exit 1
fi

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

pause() {
    echo
    read -r -p "Press Enter to continue..." _
}

header() {
    clear
    echo -e "${CYAN}"
    echo "  __  __   ___   ____   _____ _   _ _____ ____"
    echo "  \ \/ /  / _ \ / ___| | ____| \ | | ____|  _ \\"
    echo "   \  /  | | | | |  _  |  _| |  \| |  _| | |_) |"
    echo "   /  \  | |_| | |_| | | |___| |\  | |___|  _ <"
    echo "  /_/\_\  \___/ \____| |_____|_| \_|_____|_| \_\\"
    echo -e "${RESET}"
    echo -e "  ${WHITE}Browser User-Agent Generator${RESET}"
    echo "  ------------------------------------------"
    echo
}

run_command() {
    echo
    "$PYTHON" ua.py "$@"
    status=$?

    if [ "$status" -eq 0 ]; then
        echo -e "${GREEN}Done.${RESET}"
    else
        echo -e "${RED}Command failed.${RESET}"
    fi

    pause
}

ask_count() {
    read -r -p "Number of user agents: " COUNT

    if [[ ! "$COUNT" =~ ^[1-9][0-9]*$ ]]; then
        echo -e "${RED}Enter a positive whole number.${RESET}"
        return 1
    fi

    return 0
}

ask_seed() {
    read -r -p "Random seed (leave blank for random): " SEED

    if [[ -n "$SEED" && ! "$SEED" =~ ^-?[0-9]+$ ]]; then
        echo -e "${RED}Seed must be an integer.${RESET}"
        return 1
    fi

    return 0
}

choose_format() {
    echo
    echo "  1) TXT"
    echo "  2) JSON"
    echo "  3) CSV"
    echo "  4) All formats"
    echo

    read -r -p "Choose format: " FORMAT_CHOICE

    case "$FORMAT_CHOICE" in
        1) FORMAT="txt" ;;
        2) FORMAT="json" ;;
        3) FORMAT="csv" ;;
        4) FORMAT="all" ;;
        *)
            echo -e "${RED}Invalid format.${RESET}"
            return 1
            ;;
    esac

    return 0
}

export_results() {
    local mode="$1"
    shift
    local args=("$@")
    local seed_value

    if ! choose_format; then
        pause
        return
    fi

    if [[ "$FORMAT" == "all" ]]; then
        # Use the same seed so all exports contain matching profiles.
        if ! ask_seed; then
            pause
            return
        fi

        if [[ -z "$SEED" ]]; then
            seed_value="$(date +%s%N 2>/dev/null || date +%s)"
        else
            seed_value="$SEED"
        fi

        run_command "$mode" "${args[@]}" \
            --seed "$seed_value" --format txt --output agents.txt

        run_command "$mode" "${args[@]}" \
            --seed "$seed_value" --format json --output agents.json

        run_command "$mode" "${args[@]}" \
            --seed "$seed_value" --format csv --output agents.csv
    else
        local ext="$FORMAT"
        run_command "$mode" "${args[@]}" \
            --format "$ext" --output "agents.$ext"
    fi
}

random_menu() {
    header
    echo -e "${WHITE}Random generation${RESET}"
    echo

    if ! ask_count; then
        pause
        return
    fi

    echo
    echo "Browser filter:"
    echo "  1) Any browser"
    echo "  2) Chrome"
    echo "  3) Firefox"
    echo "  4) Edge"
    echo "  5) Safari"
    echo "  6) Opera"
    read -r -p "Choose browser [1]: " choice

    local args=(--count "$COUNT")

    case "${choice:-1}" in
        1|"") ;;
        2) args+=(--browser chrome) ;;
        3) args+=(--browser firefox) ;;
        4) args+=(--browser edge) ;;
        5) args+=(--browser safari) ;;
        6) args+=(--browser opera) ;;
        *)
            echo -e "${RED}Invalid selection.${RESET}"
            pause
            return
            ;;
    esac

    export_results random "${args[@]}"
}

selected_menu() {
    header
    echo -e "${WHITE}Generate selected profile${RESET}"
    echo

    echo "Browser:"
    echo "  1) Chrome"
    echo "  2) Firefox"
    echo "  3) Edge"
    echo "  4) Safari"
    echo "  5) Opera"
    read -r -p "Choose browser: " BROWSER_CHOICE

    case "$BROWSER_CHOICE" in
        1) BROWSER=chrome ;;
        2) BROWSER=firefox ;;
        3) BROWSER=edge ;;
        4) BROWSER=safari ;;
        5) BROWSER=opera ;;
        *)
            echo -e "${RED}Invalid browser.${RESET}"
            pause
            return
            ;;
    esac

    echo
    echo "Operating system:"
    echo "  1) Windows"
    echo "  2) macOS"
    echo "  3) Linux"
    echo "  4) Android"
    echo "  5) iOS"
    read -r -p "Choose OS: " OS_CHOICE

    case "$OS_CHOICE" in
        1) OS=windows ;;
        2) OS=macos ;;
        3) OS=linux ;;
        4) OS=android ;;
        5) OS=ios ;;
        *)
            echo -e "${RED}Invalid operating system.${RESET}"
            pause
            return
            ;;
    esac

    echo
    echo "Device:"
    echo "  1) Use any matching device"
    echo "  2) Desktop"
    echo "  3) Mobile"
    echo "  4) Tablet"
    read -r -p "Choose device [1]: " DEVICE_CHOICE

    local args=(--browser "$BROWSER" --os "$OS")

    case "${DEVICE_CHOICE:-1}" in
        1|"") ;;
        2) args+=(--device desktop) ;;
        3) args+=(--device mobile) ;;
        4) args+=(--device tablet) ;;
        *)
            echo -e "${RED}Invalid device.${RESET}"
            pause
            return
            ;;
    esac

    if ! ask_count; then
        pause
        return
    fi

    args+=(--count "$COUNT")
    export_results generate "${args[@]}"
}

main_menu() {
    while true; do
        header
        echo "  1) Generate random user agents"
        echo "  2) Generate selected profiles"
        echo "  3) List available profiles"
        echo "  4) Exit"
        echo

        read -r -p "Select an option: " OPTION

        case "$OPTION" in
            1) random_menu ;;
            2) selected_menu ;;
            3)
                header
                "$PYTHON" ua.py list
                pause
                ;;
            4)
                echo "Goodbye."
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option.${RESET}"
                pause
                ;;
        esac
    done
}

main_menu
