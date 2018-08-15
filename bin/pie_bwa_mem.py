#!/usr/bin/env python
# encoding: utf-8
"""
pie_bwa_mem.py

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
        "pie_bwa_mem: coloredlogs is not installed, please install it if you wish to see color in logs on standard out."
    )
    pass

# initialize global logger
LOG = None

# meta information for the file
__all__ = []
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = '2018-02-12'
__updated__ = '2018-02-15'


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
        "--bwa_version",
        choices=pie.util.programs['cutadapt'].keys(),
        required=True,
        dest="bwa_version",
        help="select which version of bwa you will like to run")
    parser.add_argument(
        "-ref",
        "--reference_sequence",
        choices=pie.util.genomes.keys(),
        dest="reference_sequence",
        required=True,
        help="select which genome should be used for alignment [required]")
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
        help="path to read FASTQ file, if pair-end path to read2 file")
    parser.add_argument(
        "-R",
        "--read_group",
        dest="read_group",
        type=str,
        help="information regarding read group for SAM file within quotes \
        [example: \"\'@RG\\tID:1\\tSM:1247014_S5\\tLB:1247014_S5_L001\\tPL:ILLUMINA\'\"]")
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        required=True,
        help="output SAM FILENAME  [required]")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="make some noise")
    parser.add_argument(
        "-V", "--version", action="version", version=program_version_message)
    parser.add_argument(
        "-c",
        "--cores",
        dest="cores",
        default=1,
        help="number of threads to be used to run bwa [default=1]")
    parser.add_argument(
        "-al",
        "--alignment_score",
        dest="alignment_score",
        default=0,
        help=
        "Don't output alignment with score lower than INT. This option only affects output [default=0]")
    parser.add_argument(
        "-M",
        "--picard_compatibility",
        dest="picard_compatibility",
        action="store_true",
        help="Mark shorter split hits as secondary (for Picard compatibility)")
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
    bwa = pie.util.programs['cutadapt'][args.bwa_version]
    cmd = cmd + bwa + " mem"
    if(args.cores):
        cores = " -t " + str(args.cores)
        cmd = cmd + cores
    if(args.alignment_score):
        alignment_score = " -T " + str(args.alignment_score)
        cmd = cmd + alignment_score
    if(args.read_group):
        read_group = " -R " + args.read_group
        cmd = cmd + read_group
    if(args.picard_compatibility):
        picard_compatibility = " -M "
        cmd = cmd + picard_compatibility
    if(args.output):
        output = " -o " + args.output
        cmd = cmd + output
    fasta = pie.util.genomes[args.reference_sequence]['bwa_fasta']
    fastq1 = args.fastq1
    cmd = cmd + " " + fasta + " " + fastq1
    
    if(args.fastq2):
        fastq2 = args.fastq2
        cmd = cmd + " " + fastq2

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
    proc = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    stdout,stderr = proc.communicate()
    if(stdout):
        LOG.critical(stdout) # this is excpetion for bwa as stderr comes to stdout
    if(stderr):
        LOG.info(stderr) # this is  excpetion for bwa as stderr comes to stdout
    retcode = proc.returncode
    if (retcode >= 0):
        end_time = time.time()
        totaltime = str(timedelta(seconds=end_time - start_time))
        if (verbose):
            LOG.info("finished running bwa,please find output in %s", args.output)
            LOG.info("duration: %s", totaltime)
    else:
        if (verbose):
            LOG.critical(
                "either bwa mem is still running or its errored out with returncode:%d",
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
        fh = logging.FileHandler(logfile, mode='a')
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
