import os

import bibo.internals
import click


def missing_files(data):
    for entry in data:
        file_field = entry['fields'].get('file')
        if file_field and not os.path.exists(file_field):
            yield entry['key'], file_field


def files_without_entries(data, files_dir):
    expected_files = {e['fields']['file'] for e in data if 'file' in e['fields']}
    for filename in os.listdir(files_dir):
        filepath = os.path.join(files_dir, filename)
        if filepath not in expected_files:
            yield filepath


@click.command('check', short_help='Check for mess in your files.')
@click.pass_context
def check(ctx):
    data = ctx.obj['data']
    click.echo('Missing files')
    for key, missing_file in missing_files(data):
        click.echo('{}\t{}'.format(key, missing_file))

    files_dir = bibo.internals.destination_heuristic(data)

    click.echo('Files with no entries')
    for file_without_entry in files_without_entries(data, files_dir):
        click.echo(file_without_entry)
