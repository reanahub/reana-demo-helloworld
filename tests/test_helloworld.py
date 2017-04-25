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

"""REANA-Demo-HelloWorld tests."""

from reana_demo_helloworld import hello, main


def test_version():
    """Test version import."""
    from reana_demo_helloworld import __version__
    assert __version__


def test_hello(tmpdir):
    """Test greeting and saving of greeting to an existing file."""
    tmpfile = tmpdir.mkdir("test_folder").join("hello.txt")
    hello("TEST", str(tmpfile), 0.2)
    assert tmpfile.read() == "Hello, TEST!\n"
    assert len(tmpdir.listdir()) == 1
    return


def test_hello_create_outputdir(tmpdir):
    """Test creation of an outputfolder when it doesn't exist."""
    tmpfile = tmpdir.mkdir("test_folder")
    hello("TEST", str(tmpfile) + "/newdir/hello.txt", 0.2)
    assert tmpfile.join("/newdir/hello.txt").read() == "Hello, TEST!\n"
    return


def test_main(tmpdir):
    """Test parameter handling of main function."""
    tmpfile = tmpdir.mkdir("test_folder").join("main.txt")
    main(['--name', 'MAIN',
          '--outputfile', str(tmpfile),
          '--sleeptimer', '0.2'])
    assert tmpfile.read() == "Hello, MAIN!\n"
    assert len(tmpdir.listdir()) == 1
    return
