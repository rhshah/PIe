#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.5
# To generate again: $ pie_mutect.py --generate_cwl_tool
# Help: $ pie_mutect.py --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['pie_mutect.py']

doc: |
  pie_mutect.py
      Created by Ronak H Shah on 2018-02-12
      Copyright (c) 2018 Northwell Health. All rights reserved.
      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0
      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.
  
  USAGE
  

inputs:
  
  compression_level:
    type: ["null", string]
    default: 5
    doc: Compression level to use for writing BAM files (0 - 9, higher is more compressed) )[default=5]
    inputBinding:
      prefix: --compression_level 

  analysis_type:
    type: string

    default: MuTect
    doc: Name of the tool to run [default - MuTect] [required]
    inputBinding:
      prefix: --analysis_type 

  create_md5_file:
    type: ["null", string]
    default: False
    doc: Whether to create an MD5 digest for any BAM or FASTQ files created.[default=false]
    inputBinding:
      prefix: --create_md5_file 

  reference_sequence:
    type:
      type: enum
      symbols: [u'GRCm38', u'ncbi36', u'mm9', u'GRCh37', u'GRCh38', u'hg18', u'hg19', u'mm10']
    doc: Reference sequence file.[required]
    inputBinding:
      prefix: --reference_sequence 

  cores:
    type: ["null", string]
    default: 1
    doc: number of cores to be used to run vardict [default=1]
    inputBinding:
      prefix: --cores 

  gatk_version:
    type:
      type: enum
      symbols: [u'default']
    doc: select which version of gatk you will like to run [required]
    inputBinding:
      prefix: --gatk_version 

  input_bam_n:
    type: string

    doc: path / name of BAM FILENAME for normal [required]
    inputBinding:
      prefix: --input_bam_n 

  input_bam_t:
    type: string

    doc: path / name of BAM FILENAME for tumor [required]
    inputBinding:
      prefix: --input_bam_t 

  output_bam:
    type: string

    doc: path to / name of the output BAM FILENAME for tumor mut sites [required]
    inputBinding:
      prefix: --output_bam 

  verbose:
    type: ["null", boolean]
    default: False
    doc: make some noise
    inputBinding:
      prefix: --verbose 

  quality_base:
    type: ["null", string]
    default: 33
    doc: Minimum base quality required to consider a base for calling [default=33]
    inputBinding:
      prefix: --quality_base 

  dbsnp:
    type: string

    doc: DBSNP .vcf to use [required]
    inputBinding:
      prefix: --dbsnp 

  intervals:
    type: string

    doc: One or more genomic intervals over which to opertate. Can be cmd line or file (including rod). [required]
    inputBinding:
      prefix: --intervals 

  coverage_file:
    type: string

    doc: full path to coverage .wig.txt file [required]
    inputBinding:
      prefix: --coverage_file 

  vcf_output:
    type: ["null", string]
    doc: File/path to output .vcf file if desired
    inputBinding:
      prefix: --vcf_output 

  cosmic:
    type: string

    doc: COSMIC sites to use in .vcf format [required]
    inputBinding:
      prefix: --cosmic 

  logfile:
    type: string

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:
    []
