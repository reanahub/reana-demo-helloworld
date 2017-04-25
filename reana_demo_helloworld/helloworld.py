# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

"""REANA-Demo-HelloWorld is a minimal demonstration of REANA system."""

from __future__ import absolute_import, print_function

import argparse
import errno
import os
import sys
import time


def main(args=None):
    """Launch main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name",
                        help="Name that should be greeted. \n \
                              Defaults to 'World'.",
                        default="World",
                        required=False)

    parser.add_argument("-o", "--outputfile",
                        help="Relative path to the file where greeting \
                              should be stored. \n \
                              Defaults to 'output/output.txt'.",
                        default="output/output.txt",
                        required=False)

    parser.add_argument("-s", "--sleeptimer",
                        help="Waiting period (in seconds) taken between \
                              writing of each character of greeting. \
                              Defaults to '1.0' (seconds).",
                        default=1.0,
                        type=float,
                        required=False)
    parsed_args = parser.parse_args(args)

    hello(parsed_args.name, parsed_args.outputfile, parsed_args.sleeptimer)

    return


def hello(name="World", outputfile="output/output.txt", sleeptimer=1.0):
    """Greeter function of REANA-Demo-HelloWorld.

    Says 'Hello' to given name and stores the greeting to a file
    by writing the greeting character by character.
    An optional waiting period taken between writing of each character
    can be defined.

    .. note:: Parameter values will be overwritten by capitalized,
        identical named environment values namespace with
        'REANA_DEMO_' prefix.
        (e.g. REANA_DEMO_NAME, REANA_DEMO_OUTPUTFILE, REANA_DEMO_SLEEPTIMER)

    :param name: Name that should be greeted.
    :param outputfile: Relative path to the file where greeting
        should be stored. Creates the path and file if they don't exist.
    :param sleeptimer: Waiting period (in seconds) taken between writing
        of each character of greeting.

    """
    # Influenced by http://stackoverflow.com/a/12517490

    filename = os.environ.get("REANA_DEMO_OUTPUTFILE", outputfile)
    greet = "Hello, " + os.environ.get("REANA_DEMO_NAME", name) + "!\n"
    sleep = os.environ.get("REANA_DEMO_SLEEPTIMER", sleeptimer)

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "at") as f:
        for char in greet:
            f.write("{}".format(char))
            f.flush()
            time.sleep(sleep)
    f.close()
    return


if __name__ == "__main__":
    main()
