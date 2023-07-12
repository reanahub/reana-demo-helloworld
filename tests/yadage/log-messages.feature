# Tests for the expected log messages

Feature: Log messages

    As a researcher,
    I want to be able to see the log messages of my workflow execution,
    So that I can verify that the workflow ran correctly.

    Scenario: The workflow start has produced the expected messages
        When the workflow is finished
        Then the engine logs should contain "yadage.creators | MainThread | INFO | initializing workflow"
        And the engine logs should contain "yadage.wflowview | MainThread | INFO | added </init:0|defined|unknown>"
        And the engine logs should contain "yadage.wflowview | MainThread | INFO | added </helloworld:0|defined|unknown>"

    Scenario: The workflow completion has produced the expected messages
        When the workflow is finished
        Then the engine logs should contain "adage | MainThread | INFO | workflow completed successfully."
        And the engine logs should contain "adage | MainThread | INFO | execution valid. (in terms of execution order)"
