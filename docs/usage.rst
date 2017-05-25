=====
Usage
=====

These docs are a little lacking at the moment, and we'd love to see them
improved!

To use Epithet in a project::

    $ epithet

    Usage: epithet [OPTIONS] COMMAND [ARGS]...

    Options:
      --dryrun  Don't actually change or create labels
      --help    Show this message and exit.

    Commands:
      add
      list

    $ epithet add --help
    Usage: epithet add [OPTIONS]

    Options:
      --name TEXT   Name of new label
      --color TEXT  Color of new label
      --key TEXT    OAuth Token
      --org TEXT    Organization to get repos from
      --repo TEXT   Optionally select a single repo
      --help        Show this message and exit.
