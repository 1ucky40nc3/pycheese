# -*- coding: utf-8 -*-
"""Run tests.

This module executes tools to test the package.
Theese tools involve pytest (a test-runner), 
bandit (a security linter from PyCQA).

Example:
    Run this file from the command line:

        $ python tests.py

Todo:
    * Integrate more tools for testing
    * Create configuration files
"""


import os


def main():
    os.system("pytest")
    os.system("bandit -r ./pycheese")


if __name__ == "__main__":
    main()

