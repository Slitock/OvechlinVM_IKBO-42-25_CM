# CLI shell protoripe

import getpass
import socket
import os


# return promt based on OS username and hostname
def get_promt() -> str:
    username = getpass.getuser()
    hostname = socket.gethostname()
    cur_dir = os.getcwd()
    return f"{username}@{hostname}:{cur_dir}> "


# input parser
def parse_line(line: str) -> list[str]:
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


# executing commads, return False to exit
def run_commands(tokens: list[str]) -> bool:
    if not tokens:
        return True

    cmd, args = tokens[0], tokens[1:]

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


# run interface
def repl() -> None:
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
    repl()


if __name__ == "__main__":
    main()
