import click
import pandas as pd


def carriage_returns(df):
    for index, row in df.iterrows():
        for column, field in row.iteritems():
            try:
                if "\r\n" in field:
                    return index, column, field
            except TypeError:
                continue


def unnamed_columns(df):
    bad_columns = [key for key in df.keys() if "Unnamed" in key]
    return len(bad_columns)


def zero_count_columns(df):
    return [key for key in df.keys() if df[key].count() == 0]


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def main(filename):
    df = pd.read_csv(filename)
    for column in zero_count_columns(df):
        click.echo(f"Warning: Column '{column}' has no items in it")
    if unnamed := unnamed_columns(df):
        click.echo(f"Warning: found {unnamed} columns that are Unnamed")
    if carriage_field := carriage_returns(df):
        index, column, field = carriage_field
        click.echo((
           f"Warning: found carriage returns at index {index}"
           f" of column '{column}':")
        )
        click.echo(f"         '{field[:50]}'")
