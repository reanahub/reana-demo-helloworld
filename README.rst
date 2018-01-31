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

    $ cat environments/python/Dockerfile
    FROM python:2.7

Since we don't need any additional Python packages for this simple example to
work, we can directly rely on the ``python`` image from the Docker Hub. The
trailing ``:2.7`` makes sure we are using Python 2.7.

4. Analysis workflow
====================

The hello world example is simple enough in that it does not require any complex
workflow steps to run. It consists of running a single command only.
Nevertheless, we shall demonstrate on how one could use the `Yadage
<https://github.com/diana-hep/yadage>`_ workflow engine to represent the hello
world application and its input and output arguments in a structured YAML
manner:

- `workflow.yaml <workflow/yadage/workflow.yaml>`_

.. code-block:: yaml

    stages:
      - name: helloworld
        dependencies: [init]
        scheduler:
          scheduler_type: 'singlestep-stage'
          parameters:
            sleeptime: {stages: init, output: sleeptime, unwrap: True}
            inputfile: {stages: init, output: inputfile, unwrap: true}
            helloworld: {stages: init, output: helloworld, unwrap: true}
            outputfile: '{workdir}/greetings.txt'
          step:
            process:
              process_type: 'string-interpolated-cmd'
              cmd: 'python "{helloworld}" --sleeptime {sleeptime} --inputfile "{inputfile}" --outputfile "{outputfile}"'
            publisher:
              publisher_type: 'frompar-pub'
              outputmap:
                outputfile: outputfile
            environment:
              environment_type: 'docker-encapsulated'
              image: 'python'
              imagetag: '2.7'

Please see the Yadage documentation for more details.

Local testing with Docker
=========================

Let us test whether everything works well locally in our containerised
environment. We shall use Docker locally. Note how we mount our local
directories ``inputs``, ``code`` and ``outputs`` into the containerised
environment:

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

Local testing with Yadage
=========================

Let us test whether the Yadage workflow engine execution works locally as well.

Since Yadage accepts only one input directory as parameter, we are going to
create a wrapper directory called ``yadage-inputs`` which will contain both
``inputs`` and ``code`` directory content:

.. code-block:: console

   $ mkdir -p yadage-local-run/yadage-inputs
   $ cd yadage-local-run
   $ cp -a ../code ../inputs yadage-inputs

We can now run Yadage locally as follows:

.. code-block:: console

   $ yadage-run . ../workflow/yadage/workflow.yaml -p sleeptime=2 -p inputfile=inputs/names.txt -p helloworld=code/helloworld.py -d initdir=`pwd`/yadage-inputs
   2018-01-26 10:47:22,521 - yadage.steering_object - INFO - initializing workflow with {u'inputfile': '/Users/rodrigdi/reana/reana-demo-helloworld/yadage-local-run/yadage-inputs/inputs/names.txt', u'helloworld': '/Users/rodrigdi/reana/reana-demo-helloworld/yadage-local-run/yadage-inputs/code/helloworld.py', u'sleeptime': 2}
   2018-01-26 10:47:22,521 - yadage.steering_api - INFO - running yadage workflow ../workflow/yadage/workflow.yaml on backend <yadage.backends.packtivitybackend.PacktivityBackend object at 0x109408ed0>
   2018-01-26 10:47:22,522 - adage.pollingexec - INFO - preparing adage coroutine.
   2018-01-26 10:47:22,522 - adage - INFO - starting state loop.
   2018-01-26 10:47:22,756 - adage.node - INFO - node ready <YadageNode init SUCCESS lifetime: 0:00:00.187837  runtime: 0:00:00.021882 (id: 21169211508d8d3d10a3571e6b1b3c387c09a4b1) has result: True>
   2018-01-26 10:47:22,807 - packtivity_logger_helloworld.step - INFO - prepare pull
   2018-01-26 10:47:25,199 - packtivity_logger_helloworld.step - INFO - running job
   2018-01-26 10:48:31,142 - adage.node - INFO - node ready <YadageNode helloworld SUCCESS lifetime: 0:01:08.409374  runtime: 0:01:08.385001 (id: 26cfa292f4e1fe9fc7f0dbef834e222ddcafb021) has result: True>
   2018-01-26 10:48:31,144 - adage.controllerutils - INFO - no nodes can be run anymore and no rules are applicable
   2018-01-26 10:48:31,144 - adage.pollingexec - INFO - exiting main polling coroutine
   2018-01-26 10:48:31,144 - adage - INFO - adage state loop done.
   2018-01-26 10:48:31,145 - adage - INFO - execution valid. (in terms of execution order)
   2018-01-26 10:48:31,145 - adage.controllerutils - INFO - no nodes can be run anymore and no rules are applicable
   2018-01-26 10:48:31,145 - adage - INFO - workflow completed successfully.

Let us check if the output corresponds to the expected value. Since Yadage
cannot be configured yet to write output to a specific directory, we should look
for the directory with the name we have given to the workflow root step, which
is ``helloworld`` in our case. Indeed:

.. code-block:: console

   $ cat helloworld/greetings.txt
   Hello John Doe!
   Hello Jane Doe!

Create REANA file
=================

Putting all together, we can now describe our example hello world application,
its runtime environment, the inputs, the code, the workflow and its outputs by
means of the following REANA specification file:

.. code-block:: yaml

    version: 0.1.0
    metadata:
      authors:
      - Harri Hirvonsalo <hjhsalo@gmail.com>
      - Diego Rodriguez <diego.rodriguez@cern.ch>
      - Tibor Simko <tibor.simko@cern.ch>
      title: Hello world - A simple reusable analysis example
      date: 18 January 2017
      repository: https://github.com/reanahub/reana-demo-helloworld/
    code:
      files:
      - code/helloworld.py
    inputs:
      files:
        - inputs/names.txt
      parameters:
        sleeptime: 2
        inputfile: inputs/names.txt
        helloworld: code/helloworld.py
    outputs:
      files:
      - outputs/greetings.txt
    environments:
      - type: docker
        image: python:2.7
    workflow:
      type: yadage
      file: workflow/yadage/workflow.yaml

This fully describes our "hello world" application in a way that can be run on
the REANA cloud.

Run the example on REANA cloud
==============================

We can now install the REANA client and submit the hello world example to run on
some particular REANA cloud instance. We start by installing the client:

.. code-block:: console

   $ mkvirtualenv reana-client -p /usr/bin/python2.7
   $ pip install reana-client

and connect to the REANA cloud instance where we will run this example:

.. code-block:: console

   $ export REANA_SERVER_URL=http://192.168.99.100:31201
   $ reana-client ping
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Connecting to http://192.168.99.100:31201
   [INFO] Server is running.

We can now initialise workflow and upload input data and code:

.. code-block:: console

   $ reana-client workflow create -f reana.yaml
   [INFO] Validating REANA specification file: /Users/rodrigdi/reana/reana-demo-helloworld/reana.yaml
   [INFO] Connecting to http://192.168.99.100:31201
   {u'message': u'Workflow workspace created', u'workflow_id': u'57c917c8-d979-481e-ae4c-8d8b9ffb2d10'}
   $ reana-client workflow status --workflow 57c917c8-d979-481e-ae4c-8d8b9ffb2d10
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow "afbbf6d1-a129-4e4f-ab8a-b8df325351d2" selected
   Name       |UUID                                |User                                |Organization|Status
   -----------|------------------------------------|------------------------------------|------------|-------
   lucid_kirch|57c917c8-d979-481e-ae4c-8d8b9ffb2d10|00000000-0000-0000-0000-000000000000|default     |created
   $ export REANA_WORKON="57c917c8-d979-481e-ae4c-8d8b9ffb2d10"
   $ reana-client code upload helloworld.py
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow "57c917c8-d979-481e-ae4c-8d8b9ffb2d10" selected
   Uploading helloworld.py ...
   File helloworld.py was successfully uploaded.
   $ reana-client code list
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   Name         |Size|Last-Modified
   -------------|----|--------------------------------
   helloworld.py|2905|2018-01-25 16:34:59.448513+00:00
   $ reana-client inputs upload names.txt
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow "57c917c8-d979-481e-ae4c-8d8b9ffb2d10" selected
   Uploading names.txt ...
   File names.txt was successfully uploaded.
   $ reana-client inputs list
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   Name     |Size|Last-Modified
   ---------|----|--------------------------------
   names.txt|18  |2018-01-25 16:34:21.888813+00:00

Start workflow execution and enquire about its running status:

.. code-block:: console

   $ reana-client workflow start
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow `57c917c8-d979-481e-ae4c-8d8b9ffb2d10` selected
   Workflow `57c917c8-d979-481e-ae4c-8d8b9ffb2d10` has been started.
   [INFO] Connecting to http://192.168.99.100:31201
   {u'status': u'running', u'organization': u'default', u'message': u'Workflow successfully launched', u'user': u'00000000-0000-0000-0000-000000000000', u'workflow_id': u'57c917c8-d979-481e-ae4c-8d8b9ffb2d10'}
   Workflow `57c917c8-d979-481e-ae4c-8d8b9ffb2d10` has been started.
   $ reana-client workflow status
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow "afbbf6d1-a129-4e4f-ab8a-b8df325351d2" selected
   Name       |UUID                                |User                                |Organization|Status
   -----------|------------------------------------|------------------------------------|------------|-------
   lucid_kirch|57c917c8-d979-481e-ae4c-8d8b9ffb2d10|00000000-0000-0000-0000-000000000000|default     |running

After the workflow execution successfully finished, we can retrieve its output:

.. code-block:: console

   $ reana-client workflow status
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow "afbbf6d1-a129-4e4f-ab8a-b8df325351d2" selected
   Name       |UUID                                |User                                |Organization|Status
   -----------|------------------------------------|------------------------------------|------------|-------
   lucid_kirch|57c917c8-d979-481e-ae4c-8d8b9ffb2d10|00000000-0000-0000-0000-000000000000|default     |finished
   $ reana-client outputs list --workflow 57c917c8-d979-481e-ae4c-8d8b9ffb2d10
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] Workflow "57c917c8-d979-481e-ae4c-8d8b9ffb2d10" selected
   Name                                 |Size|Last-Modified
   -------------------------------------|----|--------------------------------
   helloworld/greetings.txt             |32  |2018-01-25 16:36:00.582813+00:00
   _yadage/yadage_snapshot_backend.json |590 |2018-01-25 16:36:00.582813+00:00
   _yadage/yadage_snapshot_workflow.json|7668|2018-01-25 16:36:00.582813+00:00
   _yadage/yadage_template.json         |1070|2018-01-25 16:36:00.582813+00:00
   $ reana-client outputs download helloworld/greetings.txt
   [INFO] REANA Server URL ($REANA_SERVER_URL) is: http://192.168.99.100:31201
   [INFO] helloworld/greetings.txt binary file downloaded ... writing to ./outputs/
   File helloworld/greetings.txt downloaded to ./outputs/
   $ cat outputs/helloworld/greetings.txt
   Hello John Doe!
   Hello Jane Doe!

Thank you for using `REANA <http://reanahub.io/>`_ reusable analysis platform.
