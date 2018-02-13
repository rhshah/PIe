#!/usr/bin/env python
# encoding: utf-8
"""
pie_bwa_mem.py

Created by Ronak Shah on February 13, 2018.
Copyright (c) 2018 Northwell Health. All rights reserved.
"""
from __future__ import print_function
import os
import sys
import logging
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from subprocess import Popen
import shlex
import time
from datetime import date, timedelta
import pie

try:
    import coloredlogs
except ImportError:
    print("pie_bwa_mem: coloredlogs is not installed, please install it if you wish to see color in logs on standard out.")
    pass

LOG = None

__all__ = []
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = '2018-02-12'
__updated__ = '2018-02-12'

def process_command_line(argv):

    global LOG
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
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
    parser.add_argument("-b", "--bwa_version", choices=pie.util.programs['bwa'].keys(),dest="bwa_version", help="select which version of bwa you will like to run")
    parser.add_argument("-g", "--genome", choices=pie.util.genomes.keys(), dest="genome",  required=True, help="select which genome should be used for alignment [required]")
    parser.add_argument("-f1", "--fastq1", dest="fastq1", required=True, help="path to read FASTQ file, if pair-end path to read1 file [required]")
    parser.add_argument("-f2", "--fastq2", dest="fastq2", help="path to read FASTQ file, if pair-end path to read2 file")
    parser.add_argument("-R", "--read_group", dest="read_group", type=str, required=True, help="information regarding read group for SAM file [required]")
    parser.add_argument("-o" ,"--output", dest="output", required=True, help="output SAM FILENAME  [required]")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="make some noise")
    parser.add_argument("-V", "--version", action="version", version=program_version_message)
    parser.add_argument("-t", "--threads", dest="threads", required=True, help="number of threads to be used to run bwa [required]")
    parser.add_argument("-T", "--alignment_score", dest="alignment_score", default=0, help="Don’t output alignment with score lower than INT. This option only affects output [default=0]")
    parser.add_argument("-M", "--picard_compatibility", dest="picard_compatibility", action="store_true" ,help="Mark shorter split hits as secondary (for Picard compatibility)")
    parser.add_argument("-L", "--log", dest="logfile", required=True, help="write debug log to FILENAME [required]")
    args = parser.parse_args()

    # set up logging
    if args.verbose:
        LOG = setlogging(args.logfile)
        
    return args

def main(argv=None):
    args = process_command_line(argv)
    bwa = pie.util.programs['bwa'][args.bwa_version]
    fasta = pie.util.genomes[args.genome]['bwa_fasta']
    fastq1 = args.fastq1
    fastq2 = args.fastq2
    output = args.output
    threads = args.threads
    alignment_score = args.alignment_score
    read_group = args.read_group
    verbose = args.verbose
    myPid = os.getpid()
    day = date.today()
    today = day.isoformat()
    start_time = time.time()
    if(verbose):
        LOG.info("all the input parameters look good for running bwa mem")
        LOG.info("process id:%s,date:%s", myPid, today)
    if(fastq2):
        if(args.picard_compatibility):
            cmd = bwa + " mem " + "-t " + threads + " -T " + alignment_score + " -R " + read_group + " -o " + output + " -M " + fasta + " " + fastq1  + " " + fastq2
        else:
            cmd = bwa + " mem " + "-t " + threads + " -T " + alignment_score + " -R " + read_group + " -o " + output + " " + fasta + " " + fastq1  + " " + fastq2 
    else:
        if(args.picard_compatibility):
            cmd = bwa + " mem " + "-t " + threads + " -T " + alignment_score + " -R " + read_group + " -o " + output + " -M " + fasta + " " + fastq1
        else:
            cmd = bwa + " mem " + "-t " + threads + " -T " + alignment_score + " -R " + read_group + " -o " + output + " " + fasta + " " + fastq1
    
    LOG.info("command being run \n %s",cmd)
    
    args = shlex.split(cmd)
    proc = Popen(args)
    proc.wait()
    retcode = proc.returncode
    if(retcode >= 0):
        end_time = time.time()
        totaltime = str(timedelta(seconds=end_time - start_time))
        if(verbose):
            LOG.info("finished running bwa,please find output in %s",output)
            LOG.info("duration: %s", totaltime)
    else:
        if(verbose):
            LOG.critical("either bwa mem is still running or its errored out with returncode:%d",retcode) 
    
    return 0       

def setlogging(logfile=None):
    logger = logging.getLogger("pie_bwa_mem")
    formatter = logging.Formatter(fmt='%(asctime)s, %(name)s[%(process)d] %(levelname)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        coloredlogs.install(fmt='%(asctime)s, %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',level='DEBUG', logger=logger)
    except NameError:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch) 
        pass
    if logfile:
        fh = logging.FileHandler(logfile,mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

if __name__ == '__main__':
    start_time = time.time()  
    status = main()
    end_time = time.time()
    LOG.info("Elapsed time was %g seconds" % (end_time - start_time))
    sys.exit(status)
