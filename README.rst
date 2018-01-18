====================================
 REANA demo example - "hello world"
====================================

.. image:: https://img.shields.io/travis/reanahub/reana-demo-helloworld.svg
   :target: https://travis-ci.org/reanahub/reana-demo-helloworld

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/reanahub/reana?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/github/license/reanahub/reana-demo-helloworld.svg
   :target: https://github.com/reanahub/reana-demo-helloworld/blob/master/COPYING

About
=====

This repository provides a simple "hello world" application example for `REANA
<http://reanahub.io/>`_ reusable research data analysis plaftorm. The example
generates greetings for persons specified in an input file.

Making a research data analysis reproducible means to provide "runnable recipes"
addressing (1) where the input datasets are, (2) what software was used to
analyse the data, (3) which computing environment was used to run the software,
and (4) which workflow steps were taken to run the analysis.

1. Input dataset
================

The input file is a text file containing person names:

.. code-block:: console

   $ cat inputs/names.txt
   John Doe
   Jane Doe

2. Analysis code
================

A simple "hello world" Python code for illustration:

- `helloworld.py <code/helloworld.py>`_

The program takes an input file with the names of the persons to greet and an
optional sleeptime period and produces an output file with the greetings:

.. code-block:: console

   $ python code/helloworld.py \
       --inputfile inputs/names.txt
       --outputfile outputs/greetings.txt
       --sleeptime 0
   $ cat outputs/greetings.txt
   Hello John Doe!
   Hello Jane Doe!

3. Compute environment
======================

In order to be able to rerun the code even several years in the future, we need
to "encapsulate the current environment", for example to freeze the Python
version the code is using. We shall achieve this by preparing a `Docker
<https://www.docker.com/>`_ container image for the program.

For example:

.. code-block:: console

    $ cat environment/Dockerfile
    FROM python:2.7

Since we don't need any additional Python packages for this simple example to
work, we can directly rely on ``python`` image from Docker Hub. The trailing
``:2.7`` makes sue we are using Python 2.7.

Let us test whether everything works well locally in our containerised
environment. Note how we mount our local directories ``inputs``, ``code`` and
``outputs`` into the containerised environment:

.. code-block:: console

    $ rm -rf outputs && mkdir outputs
    $ docker run -i -t  --rm \
                -v `pwd`/code:/code \
                -v `pwd`/inputs:/inputs \
                -v `pwd`/outputs:/outputs \
                python:2.7 \
             python /code/helloworld.py --sleeptime 0
    $ tail -1 outputs/greetings.txt
    Hello Jane Doe!

4. Analysis workflow
====================

The hello world example is simple enough in that it does not require any complex
workflow steps to run. It consists of running a single command only.
Nevertheless, we shall demonstrate on how one could use the `Yadage
<https://github.com/diana-hep/yadage>`_ workflow engine to represent the hello
world application and its input and output arguments in a structured YAML
manner.

- `workflow.yaml <workflow/yadage/workflow.yaml>`_

**FIXME**

REANA file
==========

Putting all together, we can describe our example hello world application, its
runtime environment, the inputs, the code, the workflow and its outputs by means
of the following REANA file:

.. code-block:: yaml

    version: 0.1.0
    metadata:
      - authors:
        - Harri Hirvonsalo <hjhsalo@gmail.com>
        - Diego Rodriguez <diego.rodriguez@cern.ch>
        - Tibor Simko <tibor.simko@cern.ch>
      - title: Hello world - A simple reusable analysis example
      - date: 18 January 2017
      - repository: https://github.com/reanahub/reana-demo-helloworld/
    code:
      - files:
        - code/helloworld.py
    inputs:
      - files:
        - inputs/names.txt
      - parameters:
        - sleeptime: 2
    outputs:
      - files:
        - outputs/greetings.txt
    environments:
      - type: docker
        image: python:2.7
    workflow:
      - type: yadage
        file: workflow/yadage/workflow.yaml

This completes the full description of our simple "hello world" application that
can be run on the REANA cloud.

Run the example on REANA cloud
==============================

We can now install the REANA client and submit the hello world example to run on
some particular REANA cloud instance:

**FIXME**
