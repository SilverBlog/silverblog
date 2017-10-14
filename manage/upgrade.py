import git

current_version = 1.0
repo = git.Repo("./")
remote = repo.remote()
def upgrade_check():
    remote.fetch("--tags")
    if len(repo.tags) == 0:
        return False
    tags_num = list()
    for item in repo.tags:
        try:
            tags_num.append(float(str(item)))
        except ValueError:
            pass
    if current_version < max(tags_num):
        return True
    return False
def upgrade_pull():
    remote.pull()
