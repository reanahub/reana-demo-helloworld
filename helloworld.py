# -*- coding: utf-8 -*-

"""REANA-Demo-HelloWorld is a minimal demonstration of REANA system."""

from __future__ import absolute_import, print_function

import argparse
import errno
import os
import sys
import time


def hello(name="world", outputfile="output/output.txt", sleeptime=1.0):
    """Say 'Hello' to given name and store the greeting to a file.

    Writes the greeting character by character. An optional waiting period
    between writing of each character can be specified.

    :param name: The name of the person to be greeted.
    :param outputfile: The relative path to the file where greeting
        should be stored. Creates the file if it does not exist.
    :param sleeptime: A waiting period (in seconds) between writing
        characters of greeting.

    """
    # Influenced by http://stackoverflow.com/a/12517490

    message = "Hello " + name + "!\n"

    if not os.path.exists(os.path.dirname(outputfile)):
        try:
            os.makedirs(os.path.dirname(outputfile))
        except OSError as exc:  # guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(outputfile, "at") as f:
        for char in message:
            f.write("{}".format(char))
            f.flush()
            time.sleep(sleeptime)
    f.close()
    return


if __name__ == '__main__':
    args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name",
                        help="Name that should be greeted. \n \
                                  [default=world]",
                        default="world",
                        required=False)

    parser.add_argument("-o", "--outputfile",
                        help="Relative path to the file where greeting \
                                  should be stored. \n \
                                  [default=output/greetings.txt]",
                        default="output/greetings.txt",
                        required=False)

    parser.add_argument("-s", "--sleeptime",
                        help="Waiting period (in seconds) between \
                                  writing characters of greeting. \n \
                                  [default=1]",
                        default=1.0,
                        type=float,
                        required=False)
    parsed_args = parser.parse_args(args)

    hello(parsed_args.name, parsed_args.outputfile, parsed_args.sleeptime)
