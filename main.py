import fire
from github import Github, Label


class Epithet(object):

    def __init__(self, key, repo=None, org=None):
        self._g = Github(key)
        if org:
            g_org = self._g.get_organization(login=org)
        else:
            g_org = self._g.get_user()

        if repo:
            self._repos = [g_org.get_repo(repo)]
        else:
            self._repos = g_org.get_repos()

    def list_labels(self):
        for repo in self._repos:
            print("{}labels:\n".format(repo.name))
            for label in repo.get_labels():
                print("- {} ({})".format(label.name, label.color))

    def add_label(self, name, color):
        print("name: {}, color: {}".format(name, color))
        for repo in self._repos:
            print("Checking {}".format(repo.name))
            labels = {}
            for label in repo.get_labels():
                labels[label.name] = label
            if name in labels:
                print("Found {} on {}".format(labels[name].name, repo.name))
                if labels[name].color != color:
                    labels[name].edit(name=name, color=color)
            else:
                print("Creating {} on {}".format(name, repo.name))
                repo.create_label(name=name, color=color)


if __name__ == '__main__':
    fire.Fire(Epithet)
