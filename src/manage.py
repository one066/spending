import click

from apps.base import create_app
from extension.mysql_client import db
from apps.back_end.models import RecordSpending

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


# if __name__ == '__main__':
#     cli()
if __name__ == '__main__':
    app.run()