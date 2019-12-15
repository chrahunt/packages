import click

from .commands import list_wheel_files, update_db


@click.group()
def cli():
    pass


cli.add_command(update_db.command)
cli.add_command(list_wheel_files.command)


@cli.command("get-wheel-file-info")
def get_wheel_file_info():
    link = (
        "https://files.pythonhosted.org/packages/00/b6/"
        "9cfa56b4081ad13874b0c6f96af8ce16cfbc1cb06bedf8e9164ce5551ec1/"
        "pip-19.3.1-py2.py3-none-any.whl"
    )
    client = MongoClient()
    db = client.trash
    result = list(db.projects.aggregate(wheelfile_pipeline))
