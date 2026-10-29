"""CLI shell prototype."""


import sys
from datetime import datetime, timezone
from getpass import getuser
from socket import gethostname

from src.vfs import VFS


def get_prompt(vfs: VFS | None) -> str:
    """Return prompt based on OS username and hostname."""
    username = getuser()
    hostname = gethostname()
    cur_dir = vfs.pwd if vfs else "/"
    return f"{username}@{hostname}:{cur_dir} >  "


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


def run_command(tokens: list[str], vfs: VFS | None) -> bool:
    """Execute built-in commands, return False to exit."""
    if not tokens:
        return True

    cmd, *args = tokens

    match cmd:
        case "exit":
            return False
        case "ls":
            if vfs:
                items = vfs.ls()
                if items:
                    print(" ".join(items))
            else:
                print("emulator: VFS not loaded")
        case "cd":
            if vfs:
                target = args[0] if args else "/"
                vfs.cd(target)
            else:
                print("emulator: VFS not loaded")
        case "date":
            print(datetime.now(timezone.utc).astimezone().strftime("%a %b %d %H:%M:%S %Y"))
        case _:
            print(f"emulator: command {cmd} not found")

    return True


def run_script(script_path: str, vfs: VFS | None) -> None:
    """execute scripts"""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()

                if not clean_line or clean_line.startswith("#"):
                    continue
                print(f"{get_prompt(vfs)}{clean_line}")

                try:
                    tokens = parse_line(clean_line)

                except ValueError:
                    print(f"emulator: parse error: {ValueError}")
                    continue

                if not run_command(tokens, vfs):
                    break

    except FileNotFoundError:
        print(f"emulator: script not found: {script_path}")


def repl(vfs: VFS | None) -> None:
    """Run interactive REPL loop."""
    while True:
        try:
            raw_input = input(get_prompt(vfs))
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

        if not run_command(tokens, vfs):
            break


def print_config_box(vfs_path: str | None, script_path: str | None) -> None:
    """Print emu config in ASCII box"""
    title = "Emulator configuration"
    line_vfs = f"VFS path: {vfs_path}"
    line_script = f"Script path: {script_path}"

    width = max(len(title), len(line_vfs), len(line_script))

    print("┌" + "─" * (width + 2) + "┐")
    print("│ " + title.center(width) + " │")
    print("├" + "─" * (width + 2) + "┤")
    print("│ " + line_vfs.ljust(width) + " │")
    print("│ " + line_script.ljust(width) + " │")
    print("└" + "─" * (width + 2) + "┘")


def main() -> None:
    """Application entry point."""
    vfs_path = None
    script_path = None

    args = sys.argv[1:]
    i = 0

    while i < len(args):
        if args[i] in ("--vfs", "-v") and i + 1 < len(args):
            vfs_path = args[i + 1]
            i += 2
        elif args[i] in ("--script", "-sc") and i + 1 < len(args):
            script_path = args[i + 1]
            i += 2
        else:
            i += 1

    print_config_box(vfs_path, script_path)

    vfs = VFS(vfs_path) if vfs_path else None

    if script_path:
        run_script(script_path, vfs)
    else:
        repl(vfs)


if __name__ == "__main__":
    main()
