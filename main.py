import asyncio
import time
from telethon import TelegramClient
from telethon.tl.types import (
    UserStatusOnline,
    UserStatusOffline,
    UserStatusRecently,
    UserStatusLastWeek,
    UserStatusLastMonth,
)
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.align import Align

# Вставь сюда свои данные API:
api_id = 1234567          # Твой api_id
api_hash = "your_api_hash_here"  # Твой api_hash

console = Console()
LOGFILE = "user_status.log"

telegram_logo = r"""
____               _     _      _                     _   _ 
|  _ \__   _____  | |   (_) ___| |__  _ __   ___  ___| |_(_)
| | | \ \ / / _ \ | |   | |/ __| '_ \| '_ \ / _ \/ __| __| |
| |_| |\ V /  __/ | |___| | (__| | | | | | | (_) \__ \ |_| |
|____/  \_/ \___| |_____|_|\___|_| |_|_| |_|\___/|___/\__|_|

 ___| | ___ (_) | ____ _                                    
/ __| |/ _ \| | |/ / _` |                                   
\__ \ |  __/| |   < (_| |                                   
|___/_|\___|/ |_|\_\__,_|         by @Dve_lichnosti                          
          |__/                                              
"""

logo_text = Text(telegram_logo, style="bold cyan")
panel = Panel(logo_text, title="[bold blue]Telegram[/bold blue]", border_style="bright_blue")

def format_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours} ч {minutes} мин {sec} сек"
    elif minutes > 0:
        return f"{minutes} мин {sec} сек"
    else:
        return f"{sec} сек"

def log(message: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")

async def track(username):
    await client.start()
    console.print(panel)
    console.print(f"Отслеживаем пользователя: [bold green]@{username}[/bold green]\n")
    log(f"Старт отслеживания @{username}")

    was_online = None
    online_since = None
    offline_since = None

    with Live(console=console, refresh_per_second=4) as live:
        try:
            while True:
                try:
                    user = await client.get_entity(username)
                    status = user.status
                    now = time.strftime("%H:%M:%S")

                    if isinstance(status, UserStatusOnline):
                        if was_online is not True:
                            was_online = True
                            online_since = time.time()
                            if offline_since is not None:
                                offline_duration = int(time.time() - offline_since)
                                offline_str = f" Был офлайн {format_duration(offline_duration)}."
                            else:
                                offline_str = ""
                            offline_since = None
                        online_duration = int(time.time() - online_since) if online_since else 0
                        status_str = f"[{now}] @{username} [bold green]ONLINE[/bold green] | В сети уже {format_duration(online_duration)}.{offline_str}"

                    elif isinstance(status, UserStatusOffline):
                        if was_online is not False:
                            was_online = False
                            offline_since = time.time()
                            if online_since is not None:
                                online_duration = int(time.time() - online_since)
                                online_str = f" Был онлайн {format_duration(online_duration)}."
                            else:
                                online_str = ""
                            online_since = None
                        offline_duration = int(time.time() - offline_since) if offline_since else 0
                        status_str = f"[{now}] @{username} [bold red]OFFLINE[/bold red] | Вне сети уже {format_duration(offline_duration)}.{online_str}"

                    elif isinstance(status, UserStatusRecently):
                        was_online = False
                        online_since = None
                        offline_since = None
                        status_str = f"[{now}] @{username} [yellow]OFFLINE (был недавно)[/yellow]"

                    elif isinstance(status, UserStatusLastWeek):
                        was_online = False
                        online_since = None
                        offline_since = None
                        status_str = f"[{now}] @{username} [yellow]OFFLINE (был больше недели назад)[/yellow]"

                    elif isinstance(status, UserStatusLastMonth):
                        was_online = False
                        online_since = None
                        offline_since = None
                        status_str = f"[{now}] @{username} [yellow]OFFLINE (был больше месяца назад)[/yellow]"

                    else:
                        status_str = f"[{now}] @{username} статус неизвестен или скрыт"

                    live.update(Align.center(status_str))

                    if was_online and online_since:
                        if (time.time() - online_since) < 3 or int(time.time()) % 60 == 0:
                            log(status_str)
                    elif was_online is False and offline_since:
                        if (time.time() - offline_since) < 3 or int(time.time()) % 60 == 0:
                            log(status_str)

                except Exception as e:
                    live.update(f"[bold red]\nОшибка:[/bold red] {e}")
                    log(f"Ошибка: {e}")
                    break

                await asyncio.sleep(3)

        except KeyboardInterrupt:
            live.update("\n[bold yellow]Отслеживание прервано пользователем.[/bold yellow]")
            log("Отслеживание прервано пользователем.")

if __name__ == "__main__":
    console.print(panel)
    username = console.input("[bold cyan]Введите username Telegram (без @):[/bold cyan] ").strip()
    if not username:
        console.print("[bold red]Ошибка: username не введён[/bold red]")
        exit(1)
    client = TelegramClient("session", api_id, api_hash)
    with client:
        client.loop.run_until_complete(track(username))
