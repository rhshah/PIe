#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.5
# To generate again: $ pie_bwa_mem.py -go --generate_cwl_tool
# Help: $ pie_bwa_mem.py  --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['pie_bwa_mem.py']

requirements:
    InlineJavascriptRequirement: {}
    ResourceRequirement:
        ramMin: 10240
        coresMin: 2

doc: |
  pie_bwa_mem.py
      Created by Ronak H Shah on 2018-02-12
      Copyright (c) 2018 Northwell Health. All rights reserved.
      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0
      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.
  
  USAGE
  

inputs:
  
  bwa_version:
    type:
      type: enum
      symbols: ['default']
    default: 'default'
    doc: select which version of bwa you will like to run
    inputBinding:
      prefix: --bwa_version 

  reference_sequence:
    type:
      type: enum
      symbols: ['GRCm38', 'ncbi36', 'mm9', 'GRCh37', 'GRCh38', 'hg18', 'hg19', 'mm10']
    doc: select which genome should be used for alignment [required]
    inputBinding:
      prefix: --reference_sequence 

  fastq1:
    type: string

    doc: path to read FASTQ file, if pair-end path to read1 file [required]
    inputBinding:
      prefix: --fastq1 

  fastq2:
    type: ["null", string]
    doc: path to read FASTQ file, if pair-end path to read2 file
    inputBinding:
      prefix: --fastq2 

  read_group:
    type: ["null", string]
    doc: information regarding read group for SAM file within quotes [example - "'@RG\tID -1\tSM -1247014_S5\tLB -1247014_S5_L001\tPL -ILLUMINA'"]
    inputBinding:
      prefix: --read_group 

  output:
    type: string

    doc: output SAM FILENAME [required]
    inputBinding:
      prefix: --output 

  verbose:
    type: ["null", boolean]
    default: False
    doc: make some noise
    inputBinding:
      prefix: --verbose 

  cores:
    type: ["null", string]
    default: "1"
    doc: number of threads to be used to run bwa [default=1]
    inputBinding:
      prefix: --cores 

  alignment_score:
    type: ["null", string]
    default: "0"
    doc: Don't output alignment with score lower than INT. This option only affects output [default=0]
    inputBinding:
      prefix: --alignment_score 

  picard_compatibility:
    type: ["null", boolean]
    default: False
    doc: Mark shorter split hits as secondary (for Picard compatibility)
    inputBinding:
      prefix: --picard_compatibility 

  logfile:
    type: string

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:

  sam:
    type: File

    doc: output SAM FILENAME
    outputBinding:
      glob: |
        ${
          if (inputs.output)
            return inputs.output;
          return null;
        }

 log:
    type: File

    doc: write debug log to FILENAME
    outputBinding:
      glob: |
        ${
          if (inputs.logfile)
            return inputs.logfile;
          return null;
        }
