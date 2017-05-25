# -*- coding: utf-8 -*-

import click
from github import Github


def main():
    cli(obj={})

def get_repos(key, org, repo):
    g = Github(key)
    if org:
        g_org = g.get_organization(login=org)
    else:
        g_org = g.get_user()

    if repo:
        repos = [g_org.get_repo(repo)]
    else:
        repos = g_org.get_repos()
    return repos


@click.group()
@click.option('--dryrun', is_flag=True, help="Don't actually change or create labels")
@click.pass_context
def cli(ctx, dryrun):
    ctx.obj['dryrun'] = dryrun


@cli.command()
@click.option('--key', help="OAuth Token")
@click.option('--org', help="Organization to get repos from")
@click.option('--repo', help="Optionally select a single repo")
@click.pass_context
def list(ctx, key, org, repo):
    for repo in get_repos(key, org, repo):
        click.echo("\n * {}:\n".format(repo.name))
        for label in repo.get_labels():
            click.echo(" - {} ({})".format(label.name, label.color))


@cli.command()
@click.option('--name', help="Name of new label")
@click.option('--color', help="Color of new label")
@click.option('--key', help="OAuth Token")
@click.option('--org', help="Organization to get repos from")
@click.option('--repo', help="Optionally select a single repo")
@click.pass_context
def add(ctx, name, color, key, org, repo):
    click.echo("name: {}, color: {}".format(name, color))
    for repo in get_repos(key, org, repo):
        click.echo(" * Checking {}".format(repo.name))
        labels = {}
        for label in repo.get_labels():
            labels[label.name] = label
        if name in labels:
            click.echo(
                " - Found {} on {} (Dryrun: {})".format(
                    labels[name].name, repo.name, ctx.obj['dryrun']
                )
            )
            if labels[name].color != color and not ctx.obj['dryrun']:
                labels[name].edit(name=name, color=color)
        else:
            click.echo(
                " - Creating {} on {} (Dryrun: {})".format(
                    name, repo.name, ctx.obj['dryrun']
                )
            )
            if not ctx.obj['dryrun']:
                repo.create_label(name=name, color=color)


if __name__ == "__main__":
    main(obj={})
