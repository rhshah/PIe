#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.5
# To generate again: $ pie_pindel.py -go --generate_cwl_tool
# Help: $ pie_pindel.py  --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['pie_pindel.py']

requirements:
    InlineJavascriptRequirement: {}
    ResourceRequirement:
        ramMin: 10240
        coresMin: 2


doc: |
  Run Pindel for Long Indels & MNPS (32bp-350bp)

inputs:
  
  config:
    type: string

    doc: Full path to the pindel configuration [required]
    inputBinding:
      prefix: --pindelConfig 

  patientID:
    type: string

    doc: Id of the Patient for which the bam files are to be realigned [required]
    inputBinding:
      prefix: --patientID 

  verbose:
    type: ["null", boolean]
    default: False
    doc: make lots of noise
    inputBinding:
      prefix: --verbose 

  cores:
    type: string

    default: 5
    doc: Number of cores to be used to run Pindel [default=5] [required]
    inputBinding:
      prefix: --cores 

  reference_sequence:
    type:
      type: enum
      symbols: [u'GRCm38', u'ncbi36', u'mm9', u'GRCh37', u'GRCh38', u'hg18', u'hg19', u'mm10']
    doc: Full Path to the reference file with the bwa index. [required]
    inputBinding:
      prefix: --reference_sequence 

  PINDEL:
    type: string

    doc: Full Path to the Pindel executables. [required]
    inputBinding:
      prefix: --pindelExe 

  chr:
    type: string

    default: ALL
    doc: Which chr/fragment Pindel will process reads for one chromosome each time. ChrName must be the same as in reference sequence and in read file. [required]
    inputBinding:
      prefix: --chromosomes 

  queue:
    type: ["null", string]
    doc: Name of the SGE queue (all.q or clin.q)
    inputBinding:
      prefix: --queue 

  output_bam:
    type: string

    doc: Full Path to the output dir. [required]
    inputBinding:
      prefix: --output_bam 

  outprefix:
    type: string

    doc: Id of the Tumor bam file which will be used as the prefix for Pindel output files [required]
    inputBinding:
      prefix: --outPrefix 

  logfile:
    type: string

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:

  output_files:
    type: File

    doc: Pindel output files
    outputBinding:
      glob: $(inputs.outprefix)
