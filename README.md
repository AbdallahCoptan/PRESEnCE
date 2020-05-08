-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

![By aibrahim](https://img.shields.io/badge/by-aibrahim-blue.svg) [![gitlab](https://img.shields.io/badge/git-gitlab-lightgray.svg)](https://gitlab.uni.lu/aibrahim/presence) [![Issues](https://img.shields.io/badge/issues-gitlab-green.svg)](https://gitlab.uni.lu/aibrahim/presence/issues)

       Time-stamp: <Fri 2018-11-30 01:07 svarrette>

                ____  ____  _____ ____  _____        ____ _____
               |  _ \|  _ \| ____/ ___|| ____|_ __  / ___| ____|
               | |_) | |_) |  _| \___ \|  _| | '_ \| |   |  _|
               |  __/|  _ <| |___ ___) | |___| | | | |___| |___
               |_|   |_| \_\_____|____/|_____|_| |_|\____|_____|

                   PeRformance Evaluation of SErvices on the Cloud

       Copyright (c) 2018 A. A.Z.A Ibrahim, S. Varrette <abdallah.ibrahim@uni.lu>

A Framework for Monitoring and Modelling the Performance Metrics of Mobile Cloud SaaS Web Services.
This repository holds the sources of the prototype implementing the PRESEnCE framework for cloud performance monitoring

## Installation / Repository Setup

This repository is hosted on [Gitlab @ Uni.lu](https://gitlab.uni.lu/aibrahim/presence).

* Git interactions with this repository (push, pull etc.) are performed over SSH using the port 8022
* To clone this repository, proceed as follows (adapt accordingly):

        $> mkdir -p ~/git/gitlab.uni.lu/aibrahim
        $> cd ~/git/gitlab.uni.lu/aibrahim
        $> git clone ssh://git@gitlab.uni.lu:8022/aibrahim/presence.git

### Pyenv / Direnv

This repository make use of [pyenv](https://github.com/pyenv/pyenv), [virtualenv](https://virtualenv.pypa.io/en/stable/) and [direnv](https://direnv.net/) to offer a [sandboxed python environment](https://varrette.gforge.uni.lu/tutorials/pyenv.html).
See the following files:

* [`.python-version`](.python-version)
* [`.python-virtualenv`](.python-virtualenv)
* [`setup-direnv.sh`](setup-direnv.sh) / `.envrc`

Ensure you have followed [this tutorial](https://varrette.gforge.uni.lu/tutorials/pyenv.html), and in particular that you have install the [global `direnvrc`](https://github.com/Falkor/falkorlib/blob/devel/templates/direnv/direnvrc).

### Post-clone configuration

**`/!\ IMPORTANT`**: Once cloned, initiate your local copy of the repository by running:

```bash
$> cd presence

# Pyenv / Direnv setup
$> direnv allow .
$> pyenv install $(head .python-version)
# [force] install virtualenv by re-entering the directory
$> cd ..
$> cd presence
# Check that current virtualenv is correct
$> echo $(basename $VIRTUAL_ENV)
```

**If** (and only if) you are in the appropriate virtualenv, you can install the missing packages and configure the repository:

```bash
$> pip install -r requirements.txt
$> make setup
```

The last command  will initiate the [Git submodules of this repository](.gitmodules) and setup the [git flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) layout for this repository.

Later on, you can upgrade the [Git submodules](.gitmodules) to the latest version by running:

    $> make upgrade

If upon pulling the repository, you end in a state where another collaborator have upgraded the Git submodules for this repository, you'll end in a dirty state (as reported by modifications within the `.submodules/` directory). In that case, just after the pull, you **have to run** the following to ensure consistency with regards the Git submodules:

    $> make update

## Issues / Feature request

You can submit bug / issues / feature request using the [`aibrahim/presence` Project Tracker](https://gitlab.uni.lu/aibrahim/presence/issues)


## Advanced Topics

### [Git-flow](https://github.com/petervanderdoes/gitflow-avh)

The Git branching model for this repository follows the guidelines of
[gitflow](http://nvie.com/posts/a-successful-git-branching-model/).
In particular, the central repository holds two main branches with an infinite lifetime:

* `production`: the *production-ready* branch
* `master`: the main branch where the latest developments interviene. This is the *default* branch you get when you clone the repository.

Thus you are more than encouraged to install the [git-flow](https://github.com/petervanderdoes/gitflow-avh) (AVH Edition, as the traditional one is no longer supported) extensions following the [installation procedures](https://github.com/petervanderdoes/gitflow-avh/wiki/Installation) to take full advantage of the proposed operations. The associated [bash completion](https://github.com/bobthecow/git-flow-completion) might interest you also.

### Releasing mechanism

The operation consisting of releasing a new version of this repository is automated by a set of tasks within the root `Makefile` and the usage of the [bumpversion](https://pypi.org/project/bumpversion/) package. See:

* [.bumpversion.cfg](.bumpversion.cfg)

In this context, a version number have the following format:

      <major>.<minor>.<patch>

where:

* `< major >` corresponds to the major version number
* `< minor >` corresponds to the minor version number
* `< patch >` corresponds to the patching version number
* (eventually) `< build >` states the build number _i.e._ the total number of commits within the `master` branch.

Example: \`1.0.0-b28\`

The current version number is stored in the files `presence/__init__.py` as well as in  [.bumpversion.cfg](.bumpversion.cfg). __/!\ NEVER MAKE ANY MANUAL CHANGES TO THIS FILE__

For more information on the version, run:

     $> make versioninfo

If a new version number such be bumped, you simply have to run:

      $> make start_bump_{major,minor,patch}

This will start the release process for you using `git-flow`, bump the version to the `rc` (release candidate) state.
Once you have finished to commit your last changes, make the release effective by running:

      $> make release

It will finish the release using `git-flow`, create the appropriate tag in the `production` branch and merge all things the way they should be.
