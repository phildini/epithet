# -*- coding: utf-8 -*-

import click
from github import Github
from github.GithubException import RateLimitExceededException


def main():
    cli(obj={})

def get_repos(key, org, repo, url):
    if url:
        g = Github(key, base_url=url)
    else:
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
@click.option('--key', envvar='EPITHET_KEY', help="Github OAuth Token")
@click.option('--dryrun', is_flag=True, help="Don't actually change or create labels")
@click.option('--url', help="API URL - change if GitHub Enterprise")
@click.pass_context
def cli(ctx, key, dryrun, url):
    if not key:
        click.echo("You must provide a GitHub API v3 key")
        return
    ctx.obj['dryrun'] = dryrun
    ctx.obj['url'] = url
    ctx.obj['key'] = key


@cli.command()
@click.option('--org', help="Organization to get repos from")
@click.option('--repo', help="Optionally select a single repo")
@click.pass_context
def list(ctx, org, repo):
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
        click.echo("\n * {}:\n".format(repo.name))
        for label in repo.get_labels():
            click.echo(" - {} ({})".format(label.name, label.color))



@cli.command()
@click.option('--name', help="Name of new label")
@click.option('--color', help="Color of new label")
@click.option('--org', help="Organization to get repos from")
@click.option('--repo', help="Optionally select a single repo")
@click.pass_context
def add(ctx, name, color, org, repo):
    click.echo("Adding a label with name: {} and  color: {}".format(name, color))
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
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

@cli.command()
@click.option('--name', help="Name of label to delete")
@click.option('--org', help="Organization to get repos from")
@click.option('--repo', help="Optionally select a single repo")
@click.pass_context
def delete(ctx, name, org, repo):
    click.echo("Deleting label: {}".format(name))
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
        click.echo(" * Checking {}".format(repo.name))
        labels = {}
        for label in repo.get_labels():
            labels[label.name] = label
        if name in labels:
            click.echo(
                " - Found {} on {}, deleting (Dryrun: {})".format(
                    labels[name].name, repo.name, ctx.obj['dryrun']
                )
            )
            if not ctx.obj['dryrun']:
                labels[name].delete()


if __name__ == "__main__":
    main(obj={})
