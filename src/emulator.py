"""CLI shell prototype."""

from getpass import getuser
from os import getcwd
from socket import gethostname


def get_prompt() -> str:
    """Return prompt based on OS username and hostname."""
    username = getuser()
    hostname = gethostname()
    cur_dir = getcwd()
    return f"{username}@{hostname}:{cur_dir}> "


def parse_line(line: str) -> list[str]:
    """Parse input string manually, preserving quoted arguments."""
    tokens = []
    current_token = []
    in_quotes = False
    quote_char = ""

    for char in line:
        if in_quotes:
            if char == quote_char:
                in_quotes = False
                quote_char = ""
            else:
                current_token.append(char)
        else:
            if char in ("'", '"'):
                in_quotes = True
                quote_char = char
            elif char.isspace():
                if current_token:
                    tokens.append("".join(current_token))
                    current_token = []
            else:
                current_token.append(char)

    if in_quotes:
        raise ValueError("No closing quotation")

    if current_token:
        tokens.append("".join(current_token))

    return tokens


def run_command(tokens: list[str]) -> bool:
    """Execute built-in commands, return False to exit."""
    if not tokens:
        return True

    cmd, *args = tokens

    match cmd:
        case "exit":
            return False
        case "ls":
            print(f"Command {cmd} executed with args: {args}")
        case "cd":
            print(f"Command {cmd} executed with args: {args}")
        case _:
            print(f"emulator: command {cmd} not found")

    return True


def repl() -> None:
    """Run interactive REPL loop."""
    while True:
        try:
            raw_input = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw_input.strip():
            continue

        try:
            tokens = parse_line(raw_input.strip())
        except ValueError as err:
            print(f"emulator: parse error: {err}")
            continue

        if not run_command(tokens):
            break


def main() -> None:
    """Application entry point."""
    repl()


if __name__ == "__main__":
    main()
