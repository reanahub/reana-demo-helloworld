#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

requirements:
  - class: StepInputExpressionRequirement

inputs:
  name: string
  delay: int

outputs:
  result:
    type: File
    outputSource: helloworld/result

steps:
  helloworld:
    run: helloworld.tool
    in:
      name: name
      delay: delay
      outputfile:
        valueFrom: greetings.txt
    out: [result]
