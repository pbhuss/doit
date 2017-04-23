import datetime

import click

import db


@click.group()
def main():
    pass


@click.command()
@click.argument('name', type=str)#, help='Task title.')
@click.option('-d', '--description', type=str, help='Task description.')
@click.option('-D', '--due-date', nargs=3, type=int, help='Task due date (year, month, day).')
def add(name, description, due_date):
    due_date = datetime.date(*due_date) if due_date else None
    db.insert_task(name, description, due_date)
    click.echo(f'added {name}')


@click.command()
@click.argument('idx', type=int, required=True)
def remove(idx):
    deleted_task = db.delete_task(idx)
    if not deleted_task:
        click.echo('No such task!')
    else:
        click.echo(f'removed "{deleted_task[0]}"')


DEFAULT_PAGE_SIZE = 10


@click.command()
@click.argument('page', default=0)
@click.option('-s', '--size', default=DEFAULT_PAGE_SIZE, type=int, help=f'Page size (default {DEFAULT_PAGE_SIZE})')
def list(page, size):
    total_pages = db.get_page_count(size)
    if page >= total_pages:
        click.echo('No such page!')
        return
    click.echo(f'Page {page + 1} of {total_pages}\n')
    for idx, task in enumerate(db.list_tasks(page, size), start=page * size):
        name, description, due_date = task
        click.echo(f'[{idx}] {name}')
        if description:
            click.echo(f'    {description}')
        if due_date:
            click.echo(f'    (due {due_date})')


main.add_command(add)
main.add_command(remove)
main.add_command(list)
