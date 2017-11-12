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
@click.option('--label', '-l', is_flag=True, help="List labels", default=False)
@click.option('--milestone', '-m', is_flag=True, help='List milestones', default=False)
@click.option('--org', '-o', help="Organization to get repos from")
@click.option('--repo', '-r', help="Optionally select a single repo")
@click.pass_context
def list(ctx, label, milestone, org, repo):
    if not label and not milestone:
        click.echo("--label or --milestone required")
        return
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
        click.echo("\n * {}:\n".format(repo.name))
        if label:
            for label in repo.get_labels():
                click.echo(" - {} ({})".format(label.name, label.color))
        if milestone:
            for milestone in repo.get_milestones():
                click.echo(" - {} ({})".format(milestone.title))


@cli.command()
@click.option('--label', '-l', is_flag=True, help="Add label", default=False)
@click.option('--milestone', '-m', is_flag=True, help='Add milestone', default=False)
@click.option('--org', '-o', help="Organization")
@click.option('--repo', '-r', help="Optionally select a single repo")
@click.option('--name', '-n', help="Name of new label")
@click.option('--color', '-c', help="Color of new label")
@click.pass_context
def add(ctx, label, milestone, org, repo, name, color):
    if not label and not milestone:
        click.echo("--label or --milestone required")
        return
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
        click.echo(" * Checking {}".format(repo.name))
        if label:
            click.echo("Adding a label with name: {} and  color: {}".format(name, color))
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
        if milestone:
            click.echo("Adding a milestone with name: {}".format(name))
            milestones = {}
            for milestone in repo.get_milestones():
                milestones[milestone.title] = milestone
            if name in milestones:
                click.echo(
                    " - Found {} on {} (Dryrun: {})".format(
                        milestones[name].name, repo.name, ctx.obj['dryrun']
                    )
                )
            else:
                click.echo(
                    " - Creating {} on {} (Dryrun: {})".format(
                        name, repo.name, ctx.obj['dryrun']
                    )
                )
                if not ctx.obj['dryrun']:
                    repo.create_milestone(title=name)


@cli.command()
@click.option('--label', '-l', is_flag=True, help="Delete label", default=False)
@click.option('--milestone', '-m', is_flag=True, help='Delete milestones', default=False)
@click.option('--org', '-o', help="Organization")
@click.option('--repo', '-r', help="Optionally select a single repo")
@click.option('--name', '-n', help="Name of label or milestone to delete")
@click.pass_context
def delete(ctx, label, milestone, org, repo, name):
    if not label and not milestone:
        click.echo("--label or --milestone required")
        return
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
        click.echo(" * Checking {}".format(repo.name))
        if label:
            click.echo("Deleting label: {}".format(name))
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
        if milestone:
            click.echo("Deleting milestone: {}".format(name))
            milestones = {}
            for milestone in repo.get_milestones():
                milestones[milestone.title] = milestone
            if name in milestones:
                click.echo(
                    " - Found {} on {}, deleting (Dryrun: {})".format(
                        milestones[name].title, repo.name, ctx.obj['dryrun']
                    )
                )
                if not ctx.obj['dryrun']:
                    milestones[name].delete()


@cli.command()
@click.option('--label', '-l', is_flag=True, help="Update label", default=False)
@click.option('--milestone', '-m', is_flag=True, help='Update milestone', default=False)
@click.option('--org', '-o', help="Organization")
@click.option('--repo', '-r', help="Optionally select a single repo")
@click.option('--name', '-n', help="Name of the existing label")
@click.option('--new-name', help="New name of the label")
@click.pass_context
def update(ctx, label, milestone, org, repo, name, new_name):
    if not label and not milestone:
        click.echo("--label or --milestone required")
        return
    for repo in get_repos(ctx.obj['key'], org, repo, ctx.obj['url']):
        click.echo(" * Checking {}".format(repo.name))
        if label:
            click.echo("Updating label {}".format(name))
            labels = {}
            for label in repo.get_labels():
                labels[label.name] = label
            if name in labels:
                click.echo(
                    " - Found {} on {}, upating to {} (Dryrun: {})".format(
                        labels[name].name, repo.name, new_name, ctx.obj['dryrun']
                    )
                )
                if labels[name].name != new_name and not ctx.obj['dryrun']:
                    labels[name].edit(name=new_name, color=labels[name].color)
            else:
                click.echo("{} not found, did you mean 'add'?".format(name))
        if milestone:
            click.echo("Updating milestone with name: {}".format(name))
            milestones = {}
            for milestone in repo.get_milestones():
                milestones[milestone.title] = milestone
            if name in milestones:
                click.echo(
                    " - Found {} on {}, upating to {} (Dryrun: {})".format(
                        milestones[name].name, repo.name, new_name, ctx.obj['dryrun']
                    )
                )
            else:
                click.echo("{} not found, did you mean 'add'?".format(name))

if __name__ == "__main__":
    main(obj={})
