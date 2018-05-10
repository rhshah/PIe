#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.3-2
# To generate again: $ pie_picard_markduplicates.py -go --generate_cwl_tool
# Help: $ pie_picard_markduplicates.py  --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['pie_picard_markduplicates.py']

doc: |
  pie_picard_markduplicates.py
      Created by Ronak H Shah on 2018-02-12
      Copyright (c) 2018 Northwell Health. All rights reserved.
      Licensed under the Apache License 2.0
      http://www.apache.org/licenses/LICENSE-2.0
      Distributed on an "AS IS" basis without warranties
      or conditions of any kind, either express or implied.
  
  USAGE
  

inputs:
  
  tmp_dir:
    type: ["null", str]
    default: /scratch/
    doc: path to the temporary directory
    inputBinding:
      prefix: --tmp_dir 

  validation_stringency:
    type: ["null", str]
    default: SILENT
    doc: Validation stringency for all SAM files read by this program. Setting stringency to SILENT can improve performance when processing a BAM file in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.[default=SILENT]
    inputBinding:
      prefix: --validation_stringency 

  compression_level:
    type: ["null", str]
    default: 5
    doc: Compression level for all compressed files created (e.g. BAM and GELI).[default=5]
    inputBinding:
      prefix: --compression_level 

  create_index:
    type: ["null", str]
    default: true
    doc: Whether to create a BAM index when writing a coordinate-sorted BAM file.[default=true]
    inputBinding:
      prefix: --create_index 

  create_md5_file:
    type: ["null", str]
    default: false
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

  picard_version:
    type:
      type: enum
      symbols: [u'default']
    doc: select which version of picard you will like to run
    inputBinding:
      prefix: --picard_version 

  input_bam:
    type: str

    doc: path / name of BAM FILENAME [required]
    inputBinding:
      prefix: --input 

  output_metrics:
    type: str

    doc: path to / name of the output TXT FILENAME, in which we store the duplication metrics [required]
    inputBinding:
      prefix: --metrics 

  output_bam:
    type: str

    doc: path to / name of the output BAM FILENAME [required]
    inputBinding:
      prefix: --output 

  verbose:
    type: ["null", boolean]
    default: False
    doc: make some noise
    inputBinding:
      prefix: --verbose 

  assume_sort_order:
    type: ["null", string]
    default: coordinate
    doc: f not null, assume that the input file has this order even if the header says otherwise. Default value - null. Possible values - {unsorted, queryname, coordinate, duplicate, unknown} [default=coordinate]
    inputBinding:
      prefix: --assume_sort_order 

  optical_duplicate_pixel_distance:
    type: ["null", str]
    default: 100
    doc: The maximum offset between two duplicate clusters in order to consider them optical duplicates. The default is appropriate for unpatterned versions of the Illumina platform. For the patterned flowcell models, 2500 is moreappropriate. For other platforms and models, users should experiment to find what works best.[default=100]
    inputBinding:
      prefix: --optical_duplicate_pixel_distance 

  logfile:
    type: str

    doc: write debug log to FILENAME [required]
    inputBinding:
      prefix: --log 


outputs:

  output_metrics_out:
    type: File

    doc: path to / name of the output TXT FILENAME, in which we store the duplication metrics [required]
    outputBinding:
      glob: $(inputs.output_metrics.path)


  output_bam_out:
    type: File

    doc: path to / name of the output BAM FILENAME [required]
    outputBinding:
      glob: $(inputs.output_bam.path)

