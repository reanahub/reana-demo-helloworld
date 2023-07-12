# Tests for the presence of the expected workflow files

Feature: Workspace files

    As a researcher,
    I want to make sure that the workspace produces expected files,
    so that I can be sure that the workflow outputs are correct.

    Scenario: The workspace contains the expected input files
        When the workflow is finished
        Then the workspace should include "code/helloworld.py"
        And the workspace should include "data/names.txt"

    Scenario: The code used to generate the plot is correct
        When the workflow is finished
        Then the file "code/helloworld.py" should contain "message = "Hello " + name + "!\n""

    Scenario: The people are correctly greeted
        When the workflow is finished
        Then the workspace should contain "results/greetings.txt"
        And the size of the file "results/greetings.txt" should be between 30B and 40B
        And the file "results/greetings.txt" should contain "Hello Jane Doe!"
        And the file "results/greetings.txt" should contain "Hello Joe Bloggs!"

    Scenario: The total workspace size remains within reasonable limits
        When the workflow is finished
        Then the workspace size should be less than 50MiB
