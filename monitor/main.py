import logging

import click

from monitor.monitor import create_monitor_tables, make_measure, cleanup
from monitor.dashboard import app


@click.group()
def cli():
    logging.basicConfig(level=logging.INFO)


@cli.command()
def dev():
    app.run_server(debug=True)


@cli.command()
def measure():
    create_monitor_tables()
    make_measure()


cli.command(cleanup)


if __name__ == '__main__':
    cli()
