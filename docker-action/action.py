#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run a command, add output it to the action output"""
import os
import sys
import shutil
import argparse
import subprocess

DEBUG_INFO = False

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

    return process_output


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
    # First check if we need to enable print of debug info
    global DEBUG_INFO
    if ("INPUT_ACTION-VERBOSE" in os.environ and
            os.environ["INPUT_ACTION-VERBOSE"] in ["true", "True", True, 1, "1"]):
        DEBUG_INFO = True

    # Parse the command line arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--action-summary", action="store_true")
    action_args, bloaty_args = parser.parse_known_args()
    if DEBUG_INFO:
        print("\nAction:INFO: Python script args: {}".format(action_args))
        print("Action:INFO: bloaty args:\n{}{}".format(" " * 13, bloaty_args))
        print(flush=True)

    # Run bloaty with provided arguments
    # Action can pass empty arguments, so remove them first
    bloaty_args = [arg for arg in bloaty_args if arg]
    bloaty_process_output = run_bloaty(bloaty_args)
    bloaty_output_bytes = bloaty_process_output.stdout
    try:
        bloaty_output = bloaty_output_bytes.decode("utf-8")
    except Exception as e:
        print("Action:WARN: Could not decode bloaty output:\n{}\n".format(bloaty_output_bytes), flush=True)
        return 1    # Exit with error code
    print(bloaty_output)

    # Add bloaty output to the GH Action outputs
    if DEBUG_INFO:
        print("\nAction:INFO: Adding bloaty output to GH Action output.", flush=True)
    add_to_gh_env_var("GITHUB_OUTPUT", key="bloaty-output", value=bloaty_output)
    # ASCIIfy the byte string without the b''
    encoded_output = str(bloaty_output_bytes)[2:-1]
    add_to_gh_env_var("GITHUB_OUTPUT", key="bloaty-output-encoded", value=encoded_output)

    # Process any arguments specific to this script
    if action_args.action_summary or ("INPUT_OUTPUT-TO-SUMMARY" in os.environ and
            os.environ["INPUT_OUTPUT-TO-SUMMARY"] in ["true", "True", True, 1, "1"]):
        if DEBUG_INFO:
            print("\nAction:INFO: Adding bloaty output to GH Action workflow summary.", flush=True)
            print("             Action arg output-to-summary={}".format(os.environ["INPUT_OUTPUT-TO-SUMMARY"]))
        summary_title = os.environ.get("INPUT_SUMMARY-TITLE", default="bloaty output")
        add_to_gh_env_var(
            "GITHUB_STEP_SUMMARY",
            value="## {}\nFrom command: `{}`\n```\n{}\n```\n\n".format(
                summary_title, bloaty_process_output.args, bloaty_output
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
