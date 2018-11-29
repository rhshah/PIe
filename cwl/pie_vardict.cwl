#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.5
# To generate again: $ pie_vardict.py -go --generate_cwl_tool
# Help: $ pie_vardict.py  --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['pie_vardict.py']

requirements:
    InlineJavascriptRequirement: {}
    ResourceRequirement:
        ramMin: 10240
        coresMin: 2


doc: |
  pie_vardict.py
      Created by Ronak H Shah on 2018-02-12
      Copyright (c) 2018 Northwell Health. All rights reserved.
      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0
      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.
  
  USAGE
  

inputs:
  
  vardict_version:
    type:
      type: enum
      symbols: [u'default']
    doc: select which version of vardict you will like to run [required]
    inputBinding:
      prefix: --vardict_version 

  nID:
    type: string

    doc: Name for normal sample [required]
    inputBinding:
      prefix: --normalID 

  tID:
    type: string

    doc: Name for tumor sample [required]
    inputBinding:
      prefix: --tumorID 

  patientID:
    type: string

    doc: Id of the Patient for which the VarDict has to be ran [required]
    inputBinding:
      prefix: --patientID 

  reference_sequence:
    type:
      type: enum
      symbols: [u'GRCm38', u'ncbi36', u'mm9', u'GRCh37', u'GRCh38', u'hg18', u'hg19', u'mm10']
    doc: Full Path to the reference fasta [Required]
    inputBinding:
      prefix: --reference_sequence 

  targetRegion:
    type: string

    doc: Full path to bedfile for target region [required]
    inputBinding:
      prefix: --targetRegion 

  MAPQ:
    type: string

    default: 20
    doc: reads with mapping quality less than INT will be filtered and ignored [default=20][required]
    inputBinding:
      prefix: --mapq 

  input_bam_n:
    type: string

    doc: Full Path to normal bam file [required]
    inputBinding:
      prefix: --input_bam_n 

  input_bam_t:
    type: string

    doc: path / name of tumor BAM FILENAME [required]
    inputBinding:
      prefix: --input_bam_t 

  output_bam:
    type: string

    doc: path to / name of the output BAM FILENAME [required]
    inputBinding:
      prefix: --output 

  vardict:
    type: string

    doc: Full Path to the VarDict Java executables. [required]
    inputBinding:
      prefix: --vardictExe 

  testSomatic:
    type: string

    doc: Full Path to the VarDict's testSomatic.R script [required]
    inputBinding:
      prefix: --testSomaticScript 

  var2vcf:
    type: string

    doc: Full Path to the VarDict's var2vcf_somatic.pl script [required]
    inputBinding:
      prefix: --var2vcf 

  queue:
    type: ["null", string]
    doc: Name of the SGE queue
    inputBinding:
      prefix: --queue 

  cores:
    type: ["null", string]
    default: 10
    doc: number of cores to be used to run vardict [default=10]
    inputBinding:
      prefix: --cores 

  quality_base:
    type: string

    default: 20
    doc: BASE Quality Threshold. [default=20][required]
    inputBinding:
      prefix: --quality_base 

  MAF:
    type: string

    default: 0.01
    doc: Minimum Alternate Allele Frequency [default=0.01] [required]
    inputBinding:
      prefix: --minimumAlternateFrequnecy 

  verbose:
    type: ["null", boolean]
    default: False
    doc: make some noise
    inputBinding:
      prefix: --verbose 

  logfile:
    type: string

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:

  output_bam_out:
    type: File

    doc: path to / name of the output BAM FILENAME [required]
    outputBinding:
      glob: $(inputs.output_bam.path)
