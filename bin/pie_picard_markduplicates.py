#!/usr/bin/env python
# encoding: utf-8
"""
pie_picard_markduplicates.py

Created by Ronak Shah on April 12, 2018.
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
try:
    import coloredlogs
except ImportError:
    print(
        "pie_picard_markduplicates: coloredlogs is not installed, please install it if you wish to see color in logs on standard out."
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
    from pie.util import programs, picard_std_args
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
        "-p",
        "--picard_version",
        choices=programs['picard'].keys(),
        required=True,
        dest="picard_version",
        help="select which version of bwa you will like to run")
    parser.add_argument(
        "-i",
        "--input",
        dest="input_bam",
        required=True,
        help="path / name of BAM FILENAME [required]")
    parser.add_argument(
        "-m",
        "--metrics",
        dest="output_metrics",
        required=True,
        help=
        "path to / name of the output TXT FILENAME, in which we store the duplication metrics [required]"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_bam",
        required=True,
        help="path to / name of the output BAM FILENAME  [required]")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="make some noise")
    parser.add_argument(
        "-V", "--version", action="version", version=program_version_message)
    parser.add_argument(
        "-aso",
        "--assume_sort_order",
        dest="assume_sort_order",
        default="coordinate",
        type=str,
        help=
        "f not null, assume that the input file has this order even if the header says otherwise. Default value: null. Possible values: {unsorted, queryname, coordinate, duplicate, unknown} [default=coordinate]"
    )
    parser.add_argument(
        "-odpd",
        "--optical_duplicate_pixel_distance",
        dest="optical_duplicate_pixel_distance",
        default=100,
        help=
        "The maximum offset between two duplicate clusters in order to consider them optical duplicates. The default is appropriate for unpatterned versions of the Illumina platform. For the patterned flowcell models, 2500 is moreappropriate. For other platforms and models, users should experiment to find what works best.[default=100]"
    )
    parser.add_argument(
        "-L",
        "--log",
        dest="logfile",
        required=True,
        help="write debug log to FILENAME [required]")
    #Add additional standard arguments
    parser = picard_std_args(parser)
    args = parser.parse_args()

    # set up logging
    LOG = setlogging(args.logfile, program_name)

    return args


# assigns value for each args, makes a command and runs it on the local machine
def main(argv=None):
    from pie.util import programs,genomes
    args = process_command_line(argv)
    cmd = ""
    picard = programs['picard'][args.picard_version]
    cmd = cmd + picard + " MarkDuplicates"
    if (args.input_bam):
        input_bam = " I=" + str(args.input_bam)
        cmd = cmd + input_bam
    if (args.output_metrics):
        output_metrics = " M=" + str(args.output_metrics)
        cmd = cmd + output_metrics
    if (args.output_bam):
        output_bam = " O=" + args.output_bam
        cmd = cmd + output_bam
    if (args.reference_sequence):
        reference_sequence = " R=" + genomes[args.reference_sequence]['bwa_fasta']
        cmd = cmd + reference_sequence
    if (args.optical_duplicate_pixel_distance):
        optical_duplicate_pixel_distance = " OPTICAL_DUPLICATE_PIXEL_DISTANCE=" + args.optical_duplicate_pixel_distance
        cmd = cmd + optical_duplicate_pixel_distance
    if (args.assume_sort_order):
        assume_sort_order = " ASSUME_SORT_ORDER=" + args.assume_sort_order
        cmd = cmd + assume_sort_order
    if (args.tmp_dir):
        tmp_dir = " TMP_DIR=" + args.tmp_dir
        cmd = cmd + tmp_dir
    if (args.create_index):
        create_index = " CREATE_INDEX=" + args.create_index
        cmd = cmd + create_index
    if (args.validation_stringency):
        validation_stringency = " VALIDATION_STRINGENCY=" + args.validation_stringency
        cmd = cmd + validation_stringency
    if (args.create_md5_file):
        create_md5_file = " CREATE_MD5_FILE=" + args.create_md5_file
        cmd = cmd + create_md5_file
    if (args.compression_level):
        compression_level = " COMPRESSION_LEVEL=" + args.compression_level
        cmd = cmd + compression_level

    verbose = args.verbose
    myPid = os.getpid()
    day = date.today()
    today = day.isoformat()
    start_time = time.time()
    if (verbose):
        LOG.info(
            "all the input parameters look good for running picard markduplicates"
        )
        LOG.info("process id:%s,date:%s", myPid, today)

    LOG.info("command being run \n %s", cmd)
    # setup the command to run
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()
    if (stdout):
        LOG.info(stdout)
    if (stderr):
        LOG.critical(stderr)
    retcode = proc.returncode
    if (retcode >= 0):
        end_time = time.time()
        totaltime = str(timedelta(seconds=end_time - start_time))
        if (verbose):
            LOG.info(
                "finished running picard for markduplicates,please find output in %s",
                output_bam)
            LOG.info("duration: %s", totaltime)
    else:
        if (verbose):
            LOG.critical(
                "either picard for markduplicates is still running or its errored out with returncode:%d",
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
