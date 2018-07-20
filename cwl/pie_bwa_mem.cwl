#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.5
# To generate again: $ bwa_test.py --generate_cwl_tool
# Help: $ bwa_test.py --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['pie_bwa_mem.py']

doc: |
  pie_bwa_mem.py
      Created by Ronak H Shah on 2018-02-14
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
      symbols: [u'default']
    doc: select which version of bwa you will like to run
    inputBinding:
      prefix: --bwa_version 

  fastq1:
    type: string

    doc: path to read FASTQ file, if pair-end path to read1 file [required]
    inputBinding:
      prefix: --fastq1 

  fastq2:
    type: string

    doc: path to read FASTQ file, if pair-end path to read2 file [required]
    inputBinding:
      prefix: --fastq2 

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
    default: 1
    doc: number of cores to be used to run bwa [default=1]
    inputBinding:
      prefix: --cores 

  picard_compatibility:
    type: ["null", boolean]
    default: False
    doc: Mark shorter split hits as secondary (for Picard compatibility)
    inputBinding:
      prefix: --picard_compatibility 

  alignment_score:
    type: string

    default: 0
    doc: Don't output alignment with score lower than INT. This option only affects outpur [default=0]
    inputBinding:
      prefix: --alignment_score 

  reference_sequence:
    type:
      type: enum
      symbols: [u'GRCm38', u'ncbi36', u'mm9', u'GRCh37', u'GRCh38', u'hg18', u'hg19', u'mm10']
    doc: Select which Reference sequence file should be used for alignment.[required]
    inputBinding:
      prefix: --reference_sequence 

  read_group:
    type: ["null", string]
    doc: information regarding read group for SAM file within quotes [example - "'@RG\tID -1\tSM -1247014_S5\tLB -1247014_S5_L001\tPL -ILLUMINA'"]
    inputBinding:
      prefix: --read_group 

  logfile:
    type: string

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:
    []
