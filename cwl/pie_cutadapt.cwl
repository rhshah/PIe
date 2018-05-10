#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.3-2
# To generate again: $ pie_cutadapt.py -go --generate_cwl_tool
# Help: $ pie_cutadapt.py  --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['pie_cutadapt.py']

doc: |
  pie_cutadapt.py
      Created by Ronak H Shah on 2018-02-14
      Copyright (c) 2018 Northwell Health. All rights reserved.
      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0
      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.
  
  USAGE
  

inputs:
  
  cutadapt_version:
    type:
      type: enum
      symbols: [u'default']
    doc: select which version of cutadapt you will like to run
    inputBinding:
      prefix: --cutadapt_version 

  file_format:
    type: ["null", str]
    doc: Input file format; can be either 'fasta', 'fastq' or 'sra-fastq'. Ignored when reading csfasta/qual files. [default=auto-detect from file name extension.]
    inputBinding:
      prefix: --file_format 

  overlap_minimum_length:
    type: ["null", str]
    default: 3
    doc: Require MINLENGTH overlap between read and adapter for an adapter to be found. [default=3]
    inputBinding:
      prefix: --overlap_minimum_length 

  fastq1:
    type: str

    doc: path to read FASTQ file, if pair-end path to read1 file [required]
    inputBinding:
      prefix: --fastq1 

  fastq2:
    type: str

    doc: path to read FASTQ file, if pair-end path to read2 file [required]
    inputBinding:
      prefix: --fastq2 

  out_fastq1:
    type: str

    doc: output FASTQ for read1 [required]
    inputBinding:
      prefix: --out_fastq1 

  out_fastq2:
    type: str

    doc: output FASTQ for read2 [required]
    inputBinding:
      prefix: --out_fastq2 

  verbose:
    type: ["null", boolean]
    default: False
    doc: make some noise
    inputBinding:
      prefix: --verbose 

  cores:
    type: ["null", str]
    default: 1
    doc: number of cores to be used to run cutadapt [default=1]
    inputBinding:
      prefix: --cores 

  minimum_length:
    type: ["null", str]
    default: 20
    doc: Discard reads shorter than LENGTH. [default=20]
    inputBinding:
      prefix: --minimum_length 

  quality_base:
    type: ["null", str]
    default: 33
    doc: Assume that quality values in FASTQ are encoded as ascii(quality + QUALITY_BASE). This needs to be set to 64 for some old Illumina FASTQ files. [default=33]
    inputBinding:
      prefix: --quality_base 

  error_rate:
    type: ["null", str]
    default: 0.1
    doc: Maximum allowed error rate (no. of errors divided by Tthe length of the matching region). [default=0.1]
    inputBinding:
      prefix: --error_rate 

  read1_3prime:
    type: ["null", string]
    doc: 3' adapter to be removed from first read in a pair
    inputBinding:
      prefix: --read1_3prime 

  read2_3prime:
    type: ["null", string]
    doc: 3' adapter to be removed from second read in a pair
    inputBinding:
      prefix: --read2_3prime 

  read1_5prime:
    type: ["null", string]
    doc: 5' adapter to be removed from first read in a pair
    inputBinding:
      prefix: --read1_5prime 

  read2_5prime:
    type: ["null", string]
    doc: 5' adapter to be removed from second read in a pair
    inputBinding:
      prefix: --read2_5prime 

  read1_35prime:
    type: ["null", string]
    doc: 3' or 5' adapter to be removed from first read in a pair
    inputBinding:
      prefix: --read1_35prime 

  read2_35prime:
    type: ["null", string]
    doc: 3' or 5' adapter to be removed from second read in a pair
    inputBinding:
      prefix: --read2_35prime 

  pair_filter:
    type:
    - "null"
    - type: enum
      symbols: ['any', 'both']
    default: any
    doc: Which of the reads in a paired-end read have to match the filtering criterion in order for the pair to be filtered. [default=any]
    inputBinding:
      prefix: --pair_filter 

  logfile:
    type: str

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:
    []
