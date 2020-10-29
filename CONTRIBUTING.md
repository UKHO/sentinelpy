# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/UKHO/sentinelpy/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

## Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

## Write Documentation

sentinelpy could always use more documentation, whether as part of the
official sentinelpy docs, in docstrings, or even on the web in blog posts,
articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/UKHO/sentinelpy/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

# Get Started!

Ready to contribute? Here's how to set up `sentinelpy` for local development.

1. [Make sure Poetry is installed](https://python-poetry.org/docs/#installation)
2. Fork the `sentinelpy` repo on GitHub.
3. Clone your fork locally:
    ```
    $ git clone git@github.com:your_name_here/sentinelpy.git
    ```
4. Install your local copy into a virtual environment. Refer to the README for instructions on how to do this.
5. Create a branch for local development:
    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the checks and tests, including testing other Python versions with tox:
    ```shell script
    make lint
    make test
    make test-all # runs tox
    ```

7. Commit your changes and push your branch to GitHub:
    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```
8. Submit a pull request through the GitHub website.

# Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. Check and make sure that the tests pass for all supported Python versions.

# Tips

To run a subset of tests:
```
$ pytest tests.test_sentinelpy
```

To view test coverage as a html report:
```shell script
make coverage
```

# Deploying

A reminder for the maintainers on how to deploy. Make sure all your changes are committed and merged into master (including an entry in HISTORY.md). Then create a tag:
```shell script
git tag $(poetry version | awk '{print $2}')
git push $(poetry version | awk '{print $2}')
```
GitHub Actions will then verify the tag matches the version in the commit, create a GitHub release and finally deploy to PyPI.
