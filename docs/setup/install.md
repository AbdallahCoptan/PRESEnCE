
This repository is hosted on [Gitlab @ Uni.lu](https://gitlab.uni.lu/aibrahim/presence).

* Git interactions with this repository (push, pull etc.) are performed over SSH using the port 8022
* To clone this repository, proceed as follows (adapt accordingly):

        $> mkdir -p ~/git/gitlab.uni.lu/aibrahim
        $> cd ~/git/gitlab.uni.lu/aibrahim
        $> git clone ssh://git@gitlab.uni.lu:8022/aibrahim/presence.git


**`/!\ IMPORTANT`**: Once cloned, initiate your local copy of the repository by running:

    $> cd falkorlib::bootstrap
    $> rake setup

This will initiate the [Git submodules of this repository](.gitmodules) and setup the [git flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) layout for this repository.

Later on, you can upgrade the [Git submodules](.gitmodules) to the latest version by running:

    $> rake git:submodules:upgrade

If upon pulling the repository, you end in a state where another collaborator have upgraded the Git submodules for this repository, you'll end in a dirty state (as reported by modifications within the `.submodules/` directory). In that case, just after the pull, you **have to run** the following to ensure consistency with regards the Git submodules:

    $> rake git:submodules:update
