---
title: "Usage of pie_bwa_mem.py"
permalink: /python/bwa-mem/
excerpt: "Help of using pie_bwa_mem.py"
last_modified_at: 2018-06-09T15:58:49-04:00
redirect_from:
  - /theme-setup/
toc: true
---

## Usage

```bash
usage: pie_bwa_mem.py [-h] -b {default} -g
                      {GRCm38,ncbi36,mm9,GRCh37,GRCh38,hg18,hg19,mm10} -f1
                      FASTQ1 [-f2 FASTQ2] [-R READ_GROUP] -o OUTPUT [-v] [-V]
                      [-t THREADS] [-T ALIGNMENT_SCORE] [-M] -L LOGFILE

pie_bwa_mem.py
    Created by Ronak H Shah on 2018-02-12
    Copyright (c) 2018 Northwell Health. All rights reserved.
    Licensed under the Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0
    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.

USAGE

arguments:
  -h, --help            show this help message and exit
  -b {default}, --bwa_version {default}
                        select which version of bwa you will like to run
  -g {GRCm38,ncbi36,mm9,GRCh37,GRCh38,hg18,hg19,mm10}, --genome {GRCm38,ncbi36,mm9,GRCh37,GRCh38,hg18,hg19,mm10}
                        select which genome should be used for alignment
                        [required]
  -f1 FASTQ1, --fastq1 FASTQ1
                        path to read FASTQ file, if pair-end path to read1
                        file [required]
  -f2 FASTQ2, --fastq2 FASTQ2
                        path to read FASTQ file, if pair-end path to read2
                        file
  -R READ_GROUP, --read_group READ_GROUP
                        information regarding read group for SAM file within
                        quotes [example: "'@RG\tID:1\tSM:1247014_S5\tLB:124701
                        4_S5_L001\tPL:ILLUMINA'"]
  -o OUTPUT, --output OUTPUT
                        output SAM FILENAME [required]
  -v, --verbose         make some noise
  -V, --version         show program's version number and exit
  -t THREADS, --threads THREADS
                        number of threads to be used to run bwa [default=1]
  -T ALIGNMENT_SCORE, --alignment_score ALIGNMENT_SCORE
                        Don’t output alignment with score lower than INT.
                        This option only affects output [default=0]
  -M, --picard_compatibility
                        Mark shorter split hits as secondary (for Picard
                        compatibility)
  -L LOGFILE, --log LOGFILE
                        write debug log to FILENAME [required]

```

