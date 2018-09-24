===============================
 REANA example - "hello world"
===============================

.. image:: https://img.shields.io/travis/reanahub/reana-demo-helloworld.svg
   :target: https://travis-ci.org/reanahub/reana-demo-helloworld

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/reanahub/reana?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/github/license/reanahub/reana-demo-helloworld.svg
   :target: https://github.com/reanahub/reana-demo-helloworld/blob/master/COPYING

About
=====

This repository provides a simple "hello world" application example for `REANA
<http://www.reanahub.io/>`_ reusable research data analysis plaftorm. The example
generates greetings for persons specified in an input file.

Analysis structure
==================

Making a research data analysis reproducible basically means to provide
"runnable recipes" addressing (1) where is the input data, (2) what software was
used to analyse the data, (3) which computing environments were used to run the
software and (4) which computational workflow steps were taken to run the
analysis. This will permit to instantiate the analysis on the computational
cloud and run the analysis to obtain (5) output results.

1. Input dataset
----------------

The input file is a text file containing person names:

.. code-block:: console

    $ cat inputs/names.txt
    Jane Doe
    Joe Bloggs

2. Analysis code
----------------

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
    Hello Jane Doe!
    Hello Joe Bloggs!

3. Compute environment
----------------------

In order to be able to rerun the analysis even several years in the future, we
need to "encapsulate the current compute environment", for example to freeze the
Jupyter notebook version and the notebook kernel that our analysis was using. We
shall achieve this by preparing a `Docker <https://www.docker.com/>`_ container
image for our analysis steps.

For example:

.. code-block:: console

    $ cat environments/python/Dockerfile
    FROM python:2.7

Since we don't need any additional Python packages for this simple example to
work, we can directly rely on the ``python`` image from the Docker Hub. The
trailing ``:2.7`` makes sure we are using Python 2.7.

4. Analysis workflow
====================

This analysis is very simple because it consists basically of running only the
Python executable which will produce a text file.

The workflow can be represented as follows:

.. code-block:: console

                START
                |
                |
                V
    +-------------------------------+
    |                               | <-- inputfile=inputs/names.txt
    |    $ python helloworld.py ... | <-- sleeptime=2
    +-------------------------------+
                |
                | otuputfile=outputs/greetings.txt
                V
                STOP


Note that you can also use `CWL <http://www.commonwl.org/v1.0/>`_ or `Yadage
<https://github.com/diana-hep/yadage>`_ workflow specifications:

- `Yadage workflow definition <workflow/yadage/workflow.yaml>`_
- `CWL workflow definition <workflow/cwl/helloworld.cwl>`_

5. Output results
-----------------

The example produces a file greeting all names included in the
`names.txt <inputs/names.txt>`_ file.

.. code-block:: text

     Hello Jane Doe!
     Hello Joe Bloggs!

Local testing
=============

*Optional*

If you would like to test the analysis locally (i.e. outside of the REANA
platform), you can proceed as follows.


Using pure Docker:

.. code-block:: console

    $ rm -rf outputs && mkdir outputs
    $ docker run -i -t  --rm \
                -v `pwd`/code:/code \
                -v `pwd`/inputs:/inputs \
                -v `pwd`/outputs:/outputs \
                python:2.7 \
             python /code/helloworld.py --sleeptime 0
    $ tail -1 outputs/greetings.txt
    Hello Joe Bloggs!

In case you are using Yadage workflow specification:

.. code-block:: console

    $ mkdir -p yadage-local-run/yadage-inputs
    $ cd yadage-local-run
    $ cp -a ../code ../inputs yadage-inputs
    $ yadage-run . ../workflow/yadage/workflow.yaml -p sleeptime=2
            -p inputfile=inputs/names.txt
            -p helloworld=code/helloworld.py
            -d initdir=`pwd`/yadage-inputs
    $ cat helloworld/greetings.txt
    Hello Jane Doe!
    Hello Joe Bloggs!

Using CWL workflow specification:

.. code-block:: console

    $ mkdir cwl-local-run
    $ cd cwl-local-run
    $ cp ../code/* ../inputs/* ../workflow/cwl/helloworld-job.yml .
    $ cwltool --quiet --outdir="../outputs"
            ../workflow/cwl/helloworld.cwl helloworld-job.yml
    $ cat outputs/greetings.txt
    Hello Jane Doe!
    Hello Joe Bloggs!

Running the example on REANA cloud
==================================

We are now ready to run this example and on the `REANA <http://www.reana.io/>`_
cloud.

First we need to create a `reana.yaml <reana.yaml>`_ file describing the
structure of our analysis with its inputs, the code, the runtime environment,
the computational workflow steps and the expected outputs:

.. code-block:: yaml

    version: 0.3.0
    inputs:
    files:
        - code/helloworld.py
        - inputs/names.txt
    parameters:
        sleeptime: 2
        inputfile: inputs/names.txt
        helloworld: code/helloworld.py
        outputfile: outputs/greetings.txt
    outputs:
    files:
    - outputs/greetings.txt
    workflow:
    type: serial
    specification:
        steps:
        - environment: 'python:2.7'
            commands:
            - |
              echo "Running ${helloworld}."
              python "${helloworld}" --sleeptime ${sleeptime} \
                                     --inputfile "${inputfile}" \
                                     --outputfile "${outputfile}"

In case you are using CWL or Yadage workflow specifications:

- `reana.yaml using CWL <reana-cwl.yaml>`_
- `reana.yaml using Yadage <reana-yadage.yaml>`_

We proceed by installing the REANA command-line client:

.. code-block:: console

    $ mkvirtualenv reana-client
    $ pip install reana-client

We should now connect the client to the remote REANA cloud where the analysis
will run. We do this by setting the ``REANA_SERVER_URL`` environment variable
and ``REANA_ACCESS_TOKEN`` with a valid access token:

.. code-block:: console

    $ export REANA_SERVER_URL=https://reana.cern.ch/
    $ export REANA_ACCESS_TOKEN=<ACCESS_TOKEN>

Note that if you `run REANA cluster locally
<http://reana-cluster.readthedocs.io/en/latest/gettingstarted.html#deploy-reana-cluster-locally>`_
on your laptop, you would do:

.. code-block:: console

    $ eval $(reana-cluster env --all)

Let us test the client-to-server connection:

.. code-block:: console

    $ reana-client ping
    Connected to https://reana.cern.ch - Server is running.

We proceed to create a new workflow instance:

.. code-block:: console

    $ reana-client create
    workflow.1
    $ export REANA_WORKON=workflow.1

We can now seed the analysis workspace with our input data file and our
Python program:

.. code-block:: console

    $ reana-client upload ./inputs ./code
    File inputs/names.txt was successfully uploaded.
    File code/helloworld.py was successfully uploaded.
    $ reana-client list
    NAME                 SIZE   LAST-MODIFIED
    inputs/names.txt     18     2018-08-06 13:59:59.312452+00:00
    code/helloworld.py   2905   2018-08-06 13:58:21.134586+00:00


We can now start the workflow execution:

.. code-block:: console

    $ reana-client start
    workflow.1 has been started.

After several minutes the workflow should be successfully finished. Let us query
its status:

.. code-block:: console

    $ reana-client status
    NAME       RUN_NUMBER   CREATED               STATUS    PROGRESS
    workflow   1            2018-08-06T13:37:27   finished  1/1

We can list the output files:

.. code-block:: console

    $ reana-client list
    NAME                    SIZE   LAST-MODIFIED
    outputs/greetings.txt   32     2018-08-06 14:01:02.712452+00:00
    code/helloworld.py      2905   2018-08-06 13:58:21.134586+00:00
    inputs/names.txt        18     2018-08-06 13:59:59.312452+00:00

We finish by downloading the generated file:

.. code-block:: console

    $ reana-client download outputs/greetings.txt
    File outputs/greetings.txt downloaded to /home/reana/reanahub/reana-demo-helloworld.
    $ cat outputs/greetings.txt
    Hello Jane Doe!
    Hello Joe Bloggs!

Contributors
============

The list of contributors in alphabetical order:

- `Anton Khodak <https://orcid.org/0000-0003-3263-4553>`_ <anton.khodak@ukr.net>
- `Diego Rodriguez <https://orcid.org/0000-0003-0649-2002>`_ <diego.rodriguez@cern.ch>
- `Dinos Kousidis <https://orcid.org/0000-0002-4914-4289>`_ <dinos.kousidis@cern.ch>
- `Harri Hirvonsalo <https://orcid.org/0000-0002-5503-510X>`_ <harri.hirvonsalo@cern.ch>
- `Tibor Simko <https://orcid.org/0000-0001-7202-5803>`_ <tibor.simko@cern.ch>