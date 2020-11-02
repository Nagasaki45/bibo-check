import os

import bibo.internals
import click


def missing_files_gen(data):
    for entry in data:
        file_field = entry['fields'].get('file')
        if file_field and not os.path.exists(file_field):
            yield entry['key'], file_field


def files_with_no_entries_gen(data, files_dir):
    expected_files = {e['fields']['file'] for e in data if 'file' in e['fields']}
    for filename in os.listdir(files_dir):
        filepath = os.path.join(files_dir, filename)
        if filepath not in expected_files:
            yield filepath


@click.command('check', short_help='Check for mess in your files.')
@click.pass_context
def check(ctx):
    data = ctx.obj['data']
    missing_files = list(missing_files_gen(data))
    if missing_files:
        click.secho('Missing files', fg='red')
        for key, missing_file in missing_files:
            click.echo('{}\t{}'.format(key, missing_file))

    files_dir = bibo.internals.destination_heuristic(data)

    files_with_no_entries = list(files_with_no_entries_gen(data, files_dir))
    if files_with_no_entries:
        click.secho('Files with no entries', fg='red')
        for file_with_no_entry in files_with_no_entries:
            click.echo(file_with_no_entry)
