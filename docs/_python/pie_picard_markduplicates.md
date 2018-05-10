---
title: "Usage of pie_picard_markduplicates.py"
permalink: /python/picard-markduplicates/
excerpt: "Help of using pie_picard_markduplicates.py"
last_modified_at: 2018-06-09T15:58:49-04:00
redirect_from:
  - /theme-setup/
toc: true
---

## Usage

```bash
usage: pie_picard_markduplicates.py [-h] [-tmp TMP_DIR]
                                    [-s VALIDATION_STRINGENCY]
                                    [-c COMPRESSION_LEVEL] [-ci CREATE_INDEX]
                                    [-cm CREATE_MD5_FILE] -ref
                                    {GRCm38,ncbi36,mm9,GRCh37,GRCh38,hg18,hg19,mm10}
                                    -p {default} -i INPUT_BAM -m
                                    OUTPUT_METRICS -o OUTPUT_BAM [-v] [-V]
                                    [-aso ASSUME_SORT_ORDER]
                                    [-odpd OPTICAL_DUPLICATE_PIXEL_DISTANCE]
                                    -L LOGFILE

pie_picard_markduplicates.py
    Created by Ronak H Shah on 2018-02-12
    Copyright (c) 2018 Northwell Health. All rights reserved.
    Licensed under the Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0
    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.

USAGE

optional arguments:
  -h, --help            show this help message and exit
  -tmp TMP_DIR, --tmp_dir TMP_DIR
                        path to the temporary directory
  -s VALIDATION_STRINGENCY, --validation_stringency VALIDATION_STRINGENCY
                        Validation stringency for all SAM files read by this
                        program. Setting stringency to SILENT can improve
                        performance when processing a BAM file in which
                        variable-length data (read, qualities, tags) do not
                        otherwise need to be decoded.[default=SILENT]
  -c COMPRESSION_LEVEL, --compression_level COMPRESSION_LEVEL
                        Compression level for all compressed files created
                        (e.g. BAM and GELI).[default=5]
  -ci CREATE_INDEX, --create_index CREATE_INDEX
                        Whether to create a BAM index when writing a
                        coordinate-sorted BAM file.[default=true]
  -cm CREATE_MD5_FILE, --create_md5_file CREATE_MD5_FILE
                        Whether to create an MD5 digest for any BAM or FASTQ
                        files created.[default=false]
  -ref {GRCm38,ncbi36,mm9,GRCh37,GRCh38,hg18,hg19,mm10}, --reference_sequence {GRCm38,ncbi36,mm9,GRCh37,GRCh38,hg18,hg19,mm10}
                        Reference sequence file.[required]
  -p {default}, --picard_version {default}
                        select which version of picard you will like to run
  -i INPUT_BAM, --input INPUT_BAM
                        path / name of BAM FILENAME [required]
  -m OUTPUT_METRICS, --metrics OUTPUT_METRICS
                        path to / name of the output TXT FILENAME, in which we
                        store the duplication metrics [required]
  -o OUTPUT_BAM, --output OUTPUT_BAM
                        path to / name of the output BAM FILENAME [required]
  -v, --verbose         make some noise
  -V, --version         show program's version number and exit
  -aso ASSUME_SORT_ORDER, --assume_sort_order ASSUME_SORT_ORDER
                        f not null, assume that the input file has this order
                        even if the header says otherwise. Default value:
                        null. Possible values: {unsorted, queryname,
                        coordinate, duplicate, unknown} [default=coordinate]
  -odpd OPTICAL_DUPLICATE_PIXEL_DISTANCE, --optical_duplicate_pixel_distance OPTICAL_DUPLICATE_PIXEL_DISTANCE
                        The maximum offset between two duplicate clusters in
                        order to consider them optical duplicates. The default
                        is appropriate for unpatterned versions of the
                        Illumina platform. For the patterned flowcell models,
                        2500 is moreappropriate. For other platforms and
                        models, users should experiment to find what works
                        best.[default=100]
  -L LOGFILE, --log LOGFILE
                        write debug log to FILENAME [required]
```