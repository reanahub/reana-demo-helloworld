cwlVersion: v1.0
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull:
      reanahub/reana-demo-helloworld

inputs:
  name: string
  delay: int
  outputfile: string

baseCommand: /bin/sh

arguments:
  - prefix: -c
    valueFrom: |
      cd /code;
      python helloworld.py --name "$(inputs.name)" --sleeptime $(inputs.delay) --outputfile $(runtime.outdir)/$(inputs.outputfile)

outputs:
  result:
    type: File
    outputBinding:
      glob: $(inputs.outputfile)