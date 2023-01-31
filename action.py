#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run a command, add output it to the action output"""
import os
import sys
import shutil
import argparse
import subprocess

DEBUG_INFO = True

def run_bloaty(cmd_list):
    """Run a shell command and return the error code.

    :param cmd_list: A list of strings that make up the command to execute.
    """
    # Need to special-case a single arg, as the GitHub Action docker
    # environment sends all arguments in a single string
    if len(cmd_list) == 1:
        cmds = "bloaty {}".format(cmd_list[0])
        shell = True
    else:
        cmds = ["bloaty", *cmd_list]
        shell = False

    print("Running: {}\n".format(cmds), flush=True)
    try:
        process_output = subprocess.run(
            cmds,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as e:
        print("Error running the command:", flush=True)
        print(str(e))
        sys.exit(1)

    if process_output.returncode != 0:
        print("CompletedProcess data:")
        print(process_output)
        print("\nProcess exited with error code {}".format(process_output.returncode))
        sys.exit(process_output.returncode)

    return process_output.stdout


def add_to_gh_env_var(gh_env_var, key=None, value=None):
    """Adds a string to to a GH Action environmental variable."""
    if gh_env_var in os.environ:
        with open(os.environ[gh_env_var], 'a') as fh:
            if key:
                print("{}<<EOF".format(key), file=fh)
                print("{}".format(value), file=fh)
                print("EOF", file=fh)
            else:
                print("{}".format(value), file=fh)
    else:
        print("\nAction:WARN:", end=" ")
        print("Could not add to '{}' GH environmental variable.".format(gh_env_var))
        print(" " * 13 + "Are you sure this is running in a GH Actions environment?")


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--action-summary", action="store_true")
    action_args, bloaty_args = parser.parse_known_args()
    if DEBUG_INFO:
        print("\nAction:INFO: Action args: {}".format(action_args))
        print("Action:INFO: bloaty args:\n{}{}".format(" " * 13, bloaty_args))
        print(flush=True)

    # Run bloaty with provided arguments
    bloaty_output_bytes = run_bloaty(bloaty_args)
    bloaty_output = bloaty_output_bytes
    try:
        bloaty_output = bloaty_output_bytes.decode("utf-8")
    except Exception as e:
        print("Action:WARN: Could not decode bloaty output:\n{}\n".format(bloaty_output_bytes), flush=True)
    else:
        print(bloaty_output)

    # Add bloaty output to the action output
    if DEBUG_INFO:
        print("\nAction:INFO: Adding bloaty output to GH Action output.", flush=True)
    action_output = str(bloaty_output_bytes)[2:-1]  # ASCIIfy the byte string without the b''
    add_to_gh_env_var("GITHUB_OUTPUT", key="bloaty-output", value=action_output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
