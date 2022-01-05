import click

from apps.base import create_app
from apps.spending.models import RecordSpending, User
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


if __name__ == '__main__':
    app.run()