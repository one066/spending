import uuid
from pprint import pprint

import click

from apps.base import create_app
from apps.spending.models.user import User
from extension.mysql_client import db

app = create_app()


@click.group()
def cli():
    pass


@cli.command('create_db')
def create_db():
    click.echo('----->    start create mysql db     <-----')
    with app.app_context():
        db.create_all()
    click.echo('----->    create mysql db success    <-----')


@cli.command('add_user')
@click.option('--name', '-n', required=True, help='user name')
@click.option('--password', '-p', required=True, help='user password')
@click.option('--email', '-e', required=True, help='user email')
def add_user(name, password, email):
    click.echo('----->         start add user       <-----')
    with app.app_context():
        User.add_user(uuid.uuid4().hex, name, password, email)
    click.echo('----->    start add user success    <-----')


@cli.command('show_user')
def show_user():
    click.echo('----->         start search user       <-----')
    with app.app_context():
        pprint(User.show_users())


if __name__ == '__main__':
    cli()
