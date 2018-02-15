#!/usr/bin/env python
# encoding: utf-8
"""
pie_cutadapt.py

Created by Ronak Shah on February 13, 2018.
Copyright (c) 2018 Northwell Health. All rights reserved.
"""

#import required modules for the script
from __future__ import print_function
import os
import sys
import logging
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from subprocess import Popen, PIPE
import time
from datetime import date, timedelta
import pie

try:
    import coloredlogs
except ImportError:
    print(
        "pie_cutadapt: coloredlogs is not installed, please install it if you wish to see color in logs on standard out."
    )
    pass

# initialize global logger
LOG = None

# meta information for the file
__all__ = []
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = '2018-02-14'
__updated__ = '2018-02-14'


# process the given arguments from the command line
def process_command_line(argv):
    # get the global log variable
    global LOG
    # processing to see if args are given
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # more meta infromation generation
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s
    Created by Ronak H Shah on %s
    Copyright (c) 2018 Northwell Health. All rights reserved.
    Licensed under the Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0
    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))
    parser = ArgumentParser(
        description=program_license,
        formatter_class=RawDescriptionHelpFormatter)
    # define options here:
    parser.add_argument(
        "-b",
        "--cutadapt_version",
        choices=pie.util.programs['bwa'].keys(),
        required=True,
        dest="cutadpat_version",
        help="select which version of cutadapt you will like to run")
    parser.add_argument(
        "-ff",
        "--file_format",
        dest="file_format",
        help=
        "Input file format; can be either 'fasta', 'fastq' or \
        'sra-fastq'. Ignored when reading csfasta/qual files. \
        [default=auto-detect from file name extension.]")
    parser.add_argument(
        "-oml",
        "--overlap_minimum_length",
        dest="overlap_minimum_length",
        default=3,
        help="Require MINLENGTH overlap between read and adapter for \
        an adapter to be found. [default=3]")
    parser.add_argument(
        "-f1",
        "--fastq1",
        dest="fastq1",
        required=True,
        help=
        "path to read FASTQ file, if pair-end path to read1 file [required]")
    parser.add_argument(
        "-f2",
        "--fastq2",
        dest="fastq2",
        required=True,
        help=
        "path to read FASTQ file, if pair-end path to read2 file [required]")
    parser.add_argument(
        "-of1",
        "--out_fastq1",
        dest="out_fastq1",
        required=True,
        help="output FASTQ for read1  [required]")
    parser.add_argument(
        "-of2",
        "--out_fastq2",
        dest="out_fastq2",
        required=True,
        help="output FASTQ for read2  [required]")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="make some noise")
    parser.add_argument(
        "-c",
        "--cores",
        dest="cores",
        default=1,
        help="number of cores to be used to run cutadapt [default=1]")
    parser.add_argument(
        "-V", "--version", action="version", version=program_version_message)
    parser.add_argument(
        "-ml",
        "--minimum_length",
        dest="minimum_length",
        default=20,
        help="Discard reads shorter than LENGTH. [default=20]")
    parser.add_argument(
        "-qb",
        "--quality_base",
        dest="quality_base",
        default=33,
        help=
        "Assume that quality values in FASTQ are encoded as ascii(quality + QUALITY_BASE). \
        This needs to be set to 64 for some old Illumina FASTQ files. [default=33]"
    )
    parser.add_argument(
        "-e",
        "--error_rate",
        dest="error_rate",
        default=0.1,
        help=
        "Maximum allowed error rate (no. of errors divided by \
        Tthe length of the matching region). [default=0.1]"
    )
    parser.add_argument(
        "-a",
        "--read1_3prime",
        dest="read1_3prime",
        help="3' adapter to be removed from first read in a pair")
    parser.add_argument(
        "-A",
        "--read2_3prime",
        dest="read2_3prime",
        help="3' adapter to be removed from second read in a pair")
    parser.add_argument(
        "-g",
        "--read1_5prime",
        dest="read1_5prime",
        help="5' adapter to be removed from first read in a pair")
    parser.add_argument(
        "-G",
        "--read2_5prime",
        dest="read2_5prime",
        help="5' adapter to be removed from second read in a pair")
    parser.add_argument(
        "-b",
        "--read1_35prime",
        dest="read1_35prime",
        help="3' or 5' adapter to be removed from first read in a pair")
    parser.add_argument(
        "-B",
        "--read2_35prime",
        dest="read2_35prime",
        help="3' or 5' adapter to be removed from second read in a pair")
    parser.add_argument(
        "-pf",
        " --pair_filter",
        dest="picard_compatibility",
        choices=['any', 'both'],
        default="any",
        help=
        "Which of the reads in a paired-end read have to match the filtering criterion \
        in order for the pair to be filtered. [default=any]"
    )
    parser.add_argument(
        "-L",
        "--log",
        dest="logfile",
        required=True,
        help="write debug log to FILENAME [required]")
    args = parser.parse_args()

    # set up logging
    LOG = setlogging(args.logfile, program_name)

    return args


# assigns value for each args, makes a command and runs it on the local machine
def main(argv=None):
    args = process_command_line(argv)
    cmd = ""
    cutadapt = pie.util.programs['cutadapt'][args.bwa_version]
    cmd = cmd + cutadapt
    if(args.read1_3prime):
        read1_3prime = " -a " + args.read1_3prime
        cmd = cmd + read1_3prime 
    if(args.read2_3prime):
        read2_3prime = " -A " + args.read2_3prime
        cmd = cmd + read2_3prime
    if(args.read1_5prime):
        read1_5prime = " -g " + args.read1_5prime
        cmd = cmd + read1_5prime
    if(args.read2_5prime):
        read2_5prime = " -G " + args.read2_5prime
        cmd = cmd + read2_5prime
    if(args.read1_35prime):
        read1_35prime = " -b " + args.read1_5prime
        cmd = cmd + read1_35prime
    if(args.read2_35prime):
        read2_35prime = " -B " + args.read2_5prime
        cmd = cmd + read2_35prime
    if(args.file_format):
        file_format = " -f " + args.file_format
        cmd = cmd + file_format
    if(args.error_rate):
        errorr_rate = " -e " + args.error_rate
        cmd = cmd + errorr_rate
    if(args.minimum_length):
        minimum_length = " -m " + args.minimum_length
        cmd = cmd + minimum_length
    if(args.overlap_minimum_length):
        overlap_minimum_length = " -O " + args.overlap_minimum_length
        cmd = cmd + overlap_minimum_length
    if(args.quality_base):
        quality_base = " --quality_base " + args.quality_base
        cmd = cmd + quality_base
    if(args.cores):
        cores = " -j " + args.cores
        cmd = cmd + cores
    if(args.pair_filter):
        pair_filter = " --pair-filter " + args.pair_filter
        cmd = cmd + pair_filter
    
    ofastq1 = " -o " + args.out_fastq1
    ofastq2 = " -p " + args.out_fastq2
    fastq1 = args.fastq1
    fastq2 = args.fastq2
    
    # final command
    cmd = cmd + ofastq1 + ofastq2 + fastq1 + " " + fastq2

    verbose = args.verbose
    myPid = os.getpid()
    day = date.today()
    today = day.isoformat()
    start_time = time.time()
    if (verbose):
        LOG.info("all the input parameters look good for running bwa mem")
        LOG.info("process id:%s,date:%s", myPid, today)

    LOG.info("command being run \n %s", cmd)
    # setup the command to run
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()
    if (stdout):
        LOG.critical(
            stdout)  # this is excpetion for bwa as stderr comes to stdout
    if (stderr):
        LOG.info(
            stderr)  # this is  excpetion for bwa as stderr comes to stdout
    retcode = proc.returncode
    if (retcode >= 0):
        end_time = time.time()
        totaltime = str(timedelta(seconds=end_time - start_time))
        if (verbose):
            LOG.info("finished running cutadapt,please find output in %s,%s", ofastq1,ofastq2)
            LOG.info("duration: %s", totaltime)
    else:
        if (verbose):
            LOG.critical(
                "either cutadapt is still running or its errored out with returncode:%d",
                retcode)
        return 1

    return 0


def setlogging(logfile=None, logger_name=None):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        fmt='%(asctime)s, %(name)s[%(process)d] %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        coloredlogs.install(
            fmt=
            '%(asctime)s, %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            level='DEBUG',
            logger=logger)
    except NameError:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass
    if logfile:
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


if __name__ == '__main__':
    start_time = time.time()
    status = main()
    end_time = time.time()
    totaltime = str(timedelta(seconds=end_time - start_time))
    LOG.info("Elapsed time was %s", totaltime)
    sys.exit(status)
