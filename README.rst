====================================
 REANA demo example - "hello world"
====================================

About
=====

This repository provides a simple "hello world" application example for `REANA
<http://reanahub.io/>`_ reusable research data analysis plaftorm.

Code
====

A simple "hello world" Python code for illustration:

- `helloworld.py <helloworld.py>`_

The program takes several optional arguments such as the name of the person to
greet and an optional sleeptime period and produces an output file with the
greeting:

.. code-block:: console

   $ python helloworld.py --name Jane --sleeptime 0
   $ cat output/greetings.txt
   Hello Jane!

Containerisation
================

In order to be able to rerun the code even several years in the future, we need
to "encapsulate the current environment" for example to freeze the Python
version the code is using. We shall achieve this by preparing a `Docker
<https://www.docker.com/>`_ container image for the program:

- `Dockerfile <Dockerfile>`_

For example:

.. code-block:: console

    $ cat Dockerfile
    FROM python:2.7-alpine
    ADD . /code
    WORKDIR /code
    CMD ["python", "helloworld.py", \
         "--name", "John Doe", \
         "--outputfile", "output/greetings.txt", \
         "--sleeptime", "1"]

We build the container image:

.. code-block:: console

    $ docker build -t helloworld .

and test whether it works locally:

.. code-block:: console

    $ docker run -v `pwd`:/code -i -t --rm helloworld python helloworld.py --name Jim --sleeptime 1
    $ tail -1 output/greetings.txt
    Hello Jim!

and publish it on the Docker Hub:

.. code-block:: console

    $ docker push helloworld

Workflow
========

The hello world example is simple enough in that it does not require any complex
workflow steps to run. It consists of running a single command only.
Nevertheless, we shall demonstrate on how one could use the `Yadage
<https://github.com/diana-hep/yadage>`_ workflow engine to represent the hello
world application and its input and output arguments in a structured YAML
manner:

- `helloworld.yaml <helloworld.yaml>`_

For example:

.. code-block:: console

   $ cat helloworld.yaml
   stages:
     - name: helloworld
       dependencies: [init]
       scheduler:
         scheduler_type: 'singlestep-stage'
         parameters:
           name: {stages: init, output: name, unwrap: True}
           delay: {stages: init, output: delay, unwrap: True}
           outputfile: '{workdir}/greetings.txt'
         step:
           process:
             process_type: 'string-interpolated-cmd'
             cmd: 'python helloworld.py --name "{name}" --sleeptime {delay} --outputfile "{outputfile}"'
           publisher:
             publisher_type: 'frompar-pub'
             outputmap:
               outputfile: outputfile
           environment:
             environment_type: 'docker-encapsulated'
             image: 'reanahub/reana-demo-helloworld'

This provides a fully described "hello world" application that can be run on the
REANA cloud.

Run the example on REANA cloud
==============================

We can now install the REANA client and submit the hello world example to run on
some particular REANA cloud instance:

.. code-block:: console

   $ pip install reana-client
   $ export REANA_SERVER_URL=https://reana.cern.ch
   $ reana-client run helloworld.yaml
   [INFO] Starting helloworld...
   [...]
   [INFO] Done. You can see the results in the `output/` directory.

**FIXME** The ``reana-client`` package is a not-yet-released work-in-progress.
Until it is available, you can use ``reana run helloworld`` on the REANA server
side, following the `REANA getting started
<http://reana.readthedocs.io/en/latest/gettingstarted.html>`_ documentation.
