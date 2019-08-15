=====
Usage
=====

These docs are a little lacking at the moment, and we'd love to see them
improved!

You can use the epithet commands without a key, but you might quickly run into
rate limiting issues. Get a personal token from Github_ and pass it into the
``--key`` option, or set the ``EPITHET_KEY`` environment variable to solve this.

To use Epithet in a project::

    $ epithet

    Usage: epithet [OPTIONS] COMMAND [ARGS]...

    Options:
      --key TEXT  Github OAuth Token
      --dryrun    Don't actually change or create labels
      --url TEXT  API URL - change if GitHub Enterprise
      --help      Show this message and exit.

    Commands:
      add
      delete
      list

    $ epithet add --help

    Usage: epithet add [OPTIONS]

    Options:
      -l, --label       Add label
      -m, --milestone   Add milestone
      -o, --org TEXT    Organization
      -r, --repo TEXT   Optionally select a single repo
      -n, --name TEXT   Name of new label
      -c, --color TEXT  Color of new label
      --help            Show this message and exit.

    $ epithet list --help
    Usage: epithet list [OPTIONS]

    Options:
      -l, --label      List labels
      -m, --milestone  List milestones
      -o, --org TEXT   Organization to get repos from
      -r, --repo TEXT  Optionally select a single repo
      --help           Show this message and exit.

    $ epithet delete --help
    Usage: epithet delete [OPTIONS]

    Options:
      -l, --label      Delete label
      -m, --milestone  Delete milestones
      -o, --org TEXT   Organization
      -r, --repo TEXT  Optionally select a single repo
      -n, --name TEXT  Name of label or milestone to delete
      --help           Show this message and exit.

    $ epithet update --help
    Usage: epithet update [OPTIONS]

    Options:
      -l, --label      Update label
      -m, --milestone  Update milestone
      -o, --org TEXT   Organization
      -r, --repo TEXT  Optionally select a single repo
      -n, --name TEXT  Name of the existing label
      --new-name TEXT  New name of the label
      --help           Show this message and exit.

.. _Github: https://github.com/settings/tokens
