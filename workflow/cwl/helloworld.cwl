#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  helloworld: File
  inputfile: File
  sleeptime: int
  outputfile:
    type: string
    default: outputs/greetings.txt

outputs:
  result:
    type: File
    outputSource: first/result

steps:
  first:
    run: helloworld.tool
    in:
      helloworld: helloworld

      inputfile: inputfile
      sleeptime: sleeptime
      outputfile: outputfile
    out: [result]
