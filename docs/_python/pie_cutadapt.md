---
title: "Usage of pie_cutadapt.py"
permalink: /python/cutadapt/
excerpt: "Help of using pie_cutadpat.py"
last_modified_at: 2018-06-09T15:58:49-04:00
redirect_from:
  - /theme-setup/
toc: true
---

## Usage

```bash

usage: pie_cutadapt.py [-h] -cv {default} [-ff FILE_FORMAT]
                       [-oml OVERLAP_MINIMUM_LENGTH] -f1 FASTQ1 -f2 FASTQ2
                       -of1 OUT_FASTQ1 -of2 OUT_FASTQ2 [-v] [-c CORES] [-V]
                       [-ml MINIMUM_LENGTH] [-qb QUALITY_BASE] [-e ERROR_RATE]
                       [-a READ1_3PRIME] [-A READ2_3PRIME] [-g READ1_5PRIME]
                       [-G READ2_5PRIME] [-b READ1_35PRIME] [-B READ2_35PRIME]
                       [-pf {any,both}] -L LOGFILE

pie_cutadapt.py
    Created by Ronak H Shah on 2018-02-14
    Copyright (c) 2018 Northwell Health. All rights reserved.
    Licensed under the Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0
    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.

USAGE

optional arguments:
  -h, --help            show this help message and exit
  -cv {default}, --cutadapt_version {default}
                        select which version of cutadapt you will like to run
  -ff FILE_FORMAT, --file_format FILE_FORMAT
                        Input file format; can be either 'fasta', 'fastq' or
                        'sra-fastq'. Ignored when reading csfasta/qual files.
                        [default=auto-detect from file name extension.]
  -oml OVERLAP_MINIMUM_LENGTH, --overlap_minimum_length OVERLAP_MINIMUM_LENGTH
                        Require MINLENGTH overlap between read and adapter for
                        an adapter to be found. [default=3]
  -f1 FASTQ1, --fastq1 FASTQ1
                        path to read FASTQ file, if pair-end path to read1
                        file [required]
  -f2 FASTQ2, --fastq2 FASTQ2
                        path to read FASTQ file, if pair-end path to read2
                        file [required]
  -of1 OUT_FASTQ1, --out_fastq1 OUT_FASTQ1
                        output FASTQ for read1 [required]
  -of2 OUT_FASTQ2, --out_fastq2 OUT_FASTQ2
                        output FASTQ for read2 [required]
  -v, --verbose         make some noise
  -c CORES, --cores CORES
                        number of cores to be used to run cutadapt [default=1]
  -V, --version         show program's version number and exit
  -ml MINIMUM_LENGTH, --minimum_length MINIMUM_LENGTH
                        Discard reads shorter than LENGTH. [default=20]
  -qb QUALITY_BASE, --quality_base QUALITY_BASE
                        Assume that quality values in FASTQ are encoded as
                        ascii(quality + QUALITY_BASE). This needs to be set to
                        64 for some old Illumina FASTQ files. [default=33]
  -e ERROR_RATE, --error_rate ERROR_RATE
                        Maximum allowed error rate (no. of errors divided by
                        Tthe length of the matching region). [default=0.1]
  -a READ1_3PRIME, --read1_3prime READ1_3PRIME
                        3' adapter to be removed from first read in a pair
  -A READ2_3PRIME, --read2_3prime READ2_3PRIME
                        3' adapter to be removed from second read in a pair
  -g READ1_5PRIME, --read1_5prime READ1_5PRIME
                        5' adapter to be removed from first read in a pair
  -G READ2_5PRIME, --read2_5prime READ2_5PRIME
                        5' adapter to be removed from second read in a pair
  -b READ1_35PRIME, --read1_35prime READ1_35PRIME
                        3' or 5' adapter to be removed from first read in a
                        pair
  -B READ2_35PRIME, --read2_35prime READ2_35PRIME
                        3' or 5' adapter to be removed from second read in a
                        pair
  -pf {any,both}, --pair_filter {any,both}
                        Which of the reads in a paired-end read have to match
                        the filtering criterion in order for the pair to be
                        filtered. [default=any]
  -L LOGFILE, --log LOGFILE
                        write debug log to FILENAME [required]

```