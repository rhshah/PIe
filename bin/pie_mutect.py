#!/usr/bin/env python
# encoding: utf-8
"""
pie_mutect.py

Created by Ronak Shah on May 08, 2018.
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
        "pie_mutect: coloredlogs is not installed, please install it if you wish to see color in logs on standard out."
    )
    pass
import pie

# initialize global logger
LOG = None

# meta information for the file
__all__ = []
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = '2018-02-12'
__updated__ = '2018-04-15'

def gatk_std_args(parser):
    
    parser.add_argument(
	"-cp",
	"--compression_level",
	dest="compression_level",
	default=5,
	help="Compression level to use for writing BAM files (0 - 9, higher is more compressed) )[default=5]"
	)
    parser.add_argument(
	"-T",
	"--analysis_type",
	default="MuTect",
	dest="analysis_type",
	required=True,
	help="Name of the tool to run [default: MuTect] [required]"
	)
    parser.add_argument(
        "-cm",
        "--create_md5_file",
        dest="create_md5_file",
        default=False,
        help=
        "Whether to create an MD5 digest for any BAM or FASTQ files created.[default=false]"
    	)
    parser.add_argument(
        "-ref",
        "--reference_sequence",
        dest="reference_sequence",
        choices=pie.util.genomes.keys(),
        required=True,
        help="Reference sequence file.[required]")
    parser.add_argument(
	"-c",
	"--cores",
	dest="cores",
	default=1,
	help="number of cores to be used to run vardict [default=1]")	

    return (parser)

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
    parser = gatk_std_args(parser)
    # define options here:

    parser.add_argument(
        "-g",
        "--gatk_version",
        choices=pie.util.programs['gatk'].keys(),
        required=False,
        default="default",
        dest="gatk_version",
        help="select which version of gatk you will like to run [required]")
    parser.add_argument(
        "-in",
        "--input_bam_n",
        dest="input_bam_n",
        required=True,
        help="path / name of BAM FILENAME for normal [required]")
    parser.add_argument(
        "-it",
        "--input_bam_t",
        dest="input_bam_t",
        required=True,
        help="path / name of BAM FILENAME for tumor [required]")
    parser.add_argument(
        "-o",
        "--output_bam",
        dest="output_bam",
        required=True,
        help="path to / name of the output BAM FILENAME for tumor mut sites [required]")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="make some noise")
    parser.add_argument(
        "-V", "--version", action="version", version=program_version_message)
    parser.add_argument(
        "-bq",
        "--quality_base",
        dest="quality_base",
        default=33,
        help= "Minimum base quality required to consider a base for calling [default=33]"
    	)
    parser.add_argument(
	"-snp",
	"--dbsnp",
	dest="dbsnp",
	required=True,
	help="DBSNP .vcf to use [required]" 
	)
    parser.add_argument(
	"-int",
	"--intervals",
	dest="intervals",
	required=True,
	help="One or more genomic intervals over which to opertate. Can be cmd line or file (including rod). [required]")
    parser.add_argument(
	"-cf",
	"--coverage_file",
	dest="coverage_file",
	required=True,
	help="full path to coverage .wig.txt file [required]")
    parser.add_argument(
	"-vcf",
	"--vcf_output",
	dest="vcf_output",
	help="File/path to output .vcf file if desired")
    parser.add_argument(
	"-C",
	"--cosmic",
	dest="cosmic",
	required=True,
	help="COSMIC sites to use in .vcf format [required]"
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
    gatk = pie.util.programs['gatk'][args.gatk_version]
    cmd = cmd + gatk
    if (args.analysis_type):
	analysis_type = " --analysis_type " + args.analysis_type
	cmd = cmd + analysis_type
    if (args.input_bam_t):
        input_bam_t = " --input_file:tumor " + args.input_bam_t
        cmd = cmd + input_bam_t
    if (args.input_bam_n):
	input_bam_n = " --input_file:normal " + args.input_bam_n
	cmd = cmd + input_bam_n
    if (args.output_bam):
        output_bam = " --out " + args.output_bam
        cmd = cmd + output_bam
    if (args.reference_sequence):
        reference_sequence = " --reference_sequence " + args.reference_sequence
        cmd = cmd + reference_sequence
    if (args.cores):
	cores = " -nt " + str(args.cores)
	cmd = cmd + cores
    if (args.create_md5_file):
        create_md5_file = " --generate_md5 " + args.create_md5_file
        cmd = cmd + create_md5_file
    if (args.compression_level):
        compression_level = " -compress " + str(args.compression_level)
        cmd = cmd + compression_level
    if(args.quality_base):
	quality_base = " --quality_base " + str(args.quality_base)
        cmd = cmd + quality_base
    if(args.cosmic):
	cosmic = " --cosmic " + args.cosmic
	cmd = cmd + cosmic
    if(args.dbsnp):
	dbsnp = " --dbsnp " + args.dbsnp
	cmd = cmd + dbsnp
    if (args.coverage_file):
        coverage_file = " --coverage_file " + args.coverage_file
        cmd = cmd + coverage_file
    if (args.intervals):
        intervals = " --intervals " + args.intervals
        cmd = cmd + intervals
    if (args.vcf_output):
	vcf_output = " -vcf " + args.vcf_output
	cmd = cmd + vcf_output

    verbose = args.verbose
    myPid = os.getpid()
    day = date.today()
    today = day.isoformat()
    start_time = time.time()
    if (verbose):
        LOG.info(
            "all the input parameters look good for running GATK mutect"
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
                "finished running GATK for mutect,please find output in %s",
                args.output_bam)
            LOG.info("duration: %s", totaltime)
    else:
        if (verbose):
            LOG.critical(
                "either GATK for mutect is still running or its errored out with returncode:%d",
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
