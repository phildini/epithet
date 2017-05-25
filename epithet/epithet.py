# -*- coding: utf-8 -*-

import click
from github import Github


def main():
    cli(obj={})


@click.group()
@click.option('--key', help="OAuth Token")
@click.option('--org', help="Organization to get repos from")
@click.option('--repo', help="Optionally select a single repo")
@click.pass_context
def cli(ctx, key, org, repo):
    g = Github(key)
    if org:
        g_org = g.get_organization(login=org)
    else:
        g_org = g.get_user()

    if repo:
        repos = [g_org.get_repo(repo)]
    else:
        repos = g_org.get_repos()
    ctx.obj['repos'] = repos


@cli.command()
@click.pass_context
def list(ctx):
    for repo in ctx.obj['repos']:
        click.echo("{}labels:\n".format(repo.name))
        for label in repo.get_labels():
            click.echo("- {} ({})".format(label.name, label.color))


@cli.command()
@click.pass_context
def add(ctx, name, color):
    click.echo("name: {}, color: {}".format(name, color))
    for repo in ctx.obj['repos']:
        click.echo("Checking {}".format(repo.name))
        labels = {}
        for label in repo.get_labels():
            labels[label.name] = label
        if name in labels:
            click.echo("Found {} on {}".format(labels[name].name, repo.name))
            if labels[name].color != color:
                labels[name].edit(name=name, color=color)
        else:
            click.echo("Creating {} on {}".format(name, repo.name))
            repo.create_label(name=name, color=color)


if __name__ == "__main__":
    main(obj={})
