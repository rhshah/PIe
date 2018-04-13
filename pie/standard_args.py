#!/usr/bin/env python
# encoding: utf-8
"""
standard_args.py

Created by Ronak Shah on April 12, 2018.
Copyright (c) 2018 Northwell Health. All rights reserved.
"""
#Picard Standard Arguments
def picard_std_args(parser):
    #from util import genomes
    parser.add_argument(
        "-tmp",
        "--tmp_dir",
        dest="tmp_dir",
        default="/scratch/",
        help="path to the temporary directory")
    parser.add_argument(
        "-s",
        "--validation_stringency",
        dest="validation_stringency",
        default="SILENT",
        help=
        "Validation stringency for all SAM files read by this program. Setting stringency to SILENT can improve performance when processing a BAM file in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.[default=SILENT]"
    )
    parser.add_argument(
        "-c",
        "--compression_level",
        dest="compression_level",
        default="5",
        help=
        "Compression level for all compressed files created (e.g. BAM and GELI).[default=5]"
    )
    parser.add_argument(
        "-ci",
        "--create_index",
        dest="create_index",
        default="true",
        help=
        "Whether to create a BAM index when writing a coordinate-sorted BAM file.[default=true]"
    )
    parser.add_argument(
        "-cm",
        "--create_md5_file",
        dest="create_md5_file",
        default="false",
        help=
        "Whether to create an MD5 digest for any BAM or FASTQ files created.[default=false]"
    )
    parser.add_argument(
        "-ref",
        "--reference_sequence",
        dest="reference_sequence",
        #choices=genomes.keys(),
        required=True,
        help="Reference sequence file.[required]")
    return (parser)