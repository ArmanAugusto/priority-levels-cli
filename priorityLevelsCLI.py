# priorityLevelsCLI.py

import typer
from rich.console import Console
from rich.table import Table
from model import ActionItem
from database import get_all_action_items, delete_action_item, insert_action_item, complete_action_item, update_action_item


console = Console()

app = typer.Typer()


@app.command(short_help='adds an item')
def add(task: str, priority_level: str):
    typer.echo(f"adding {task}, {priority_level}")
    action_item = ActionItem(task, priority_level)
    insert_action_item(action_item)
    show()

@app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    # indices in UI begin at 1, but in database at 0
    delete_action_item(position-1)
    show()

app.command()
def update(position: int, task: str = None, priority_level: str = None):
    typer.echo(f"updating {position}")
    update_action_item(position-1, task, priority_level)
    show()

@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_action_item(position-1)
    show()

@app.command()
def show():
    tasks = get_all_action_items()
    console.print("[bold magenta]\n\n\n\t\t\t******** Priority Levels CLI ********[/bold magenta]\n")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Action Item", min_width=40)
    table.add_column("Priority Level", min_width=20, justify="right")
    table.add_column("Status", min_width=12, justify="right")

    def get_priority_level_color(priority_level):
        COLORS = {'High': 'red', 'Medium': 'yellow', 'Low': 'Blue'}
        if priority_level in COLORS:
            return COLORS[priority_level]
        return 'white'
    
    for idx, task in enumerate(tasks, start=1):
        c = get_priority_level_color(task.priority_level)
        is_done_str = "Done" if task.status == 2 else "Incomplete"
        table.add_row(str(idx), task.task, f'[{c}]{task.priority_level}[/{c}]', is_done_str)
    console.print(table)

    console.print("\n\n")

if __name__ == "__main__":
    app()
