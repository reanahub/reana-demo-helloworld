# Tests for the expected log messages

Feature: Log messages

    As a researcher,
    I want to be able to see the log messages of my workflow execution,
    So that I can verify that the workflow ran correctly.

    Scenario: The workflow start has produced the expected messages
        When the workflow is finished
        Then the engine logs should contain "snakemake.logging | MainThread | WARNING | Building DAG of jobs..."

    Scenario: The workflow completion has produced the expected messages
        When the workflow is finished
        Then the engine logs should contain "snakemake.logging | MainThread | INFO | 2 of 2 steps (100%) done"
