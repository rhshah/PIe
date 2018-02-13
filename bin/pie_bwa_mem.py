#!/usr/bin/env python
# encoding: utf-8
"""
pie_bwa_mem.py

Created by Ronak Shah on February 13, 2018.
Copyright (c) 2018 Northwell Health. All rights reserved.
"""
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
    parser.add_argument("-g", "--genome", choices=pie.util.genomes.keys(), dest="genome",  required=True, help="select which genome should be used for alignment [required]")
    parser.add_argument("-f1", "--fastq1", dest="fastq1", required=True, help="path to read FASTQ file, if pair-end path to read1 file [required]")
    parser.add_argument("-f2", "--fastq2", dest="fastq2", help="path to read FASTQ file, if pair-end path to read2 file")
    parser.add_argument("-R", "--read_group", dest="read_group", required=True, help="information regarding read group for SAM file [required]")
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
    bwa = pie.util.programs['bwa']
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
        LOG.info("pie_bwa_mem: all the input parameters look good for running bwa mem")
        LOG.info("pie_bwa_mem: process id:%s,date:%s", myPid, today)
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
    
    args = shlex.split(cmd)
    proc = Popen(args)
    proc.wait()
    retcode = proc.returncode
    if(retcode >= 0):
        end_time = time.time()
        totaltime = str(timedelta(seconds=end_time - start_time))
        if(verbose):
            LOG.info("pie_bwa_mem: finished running bwa,please find output in %s",output)
            LOG.info("pie_bwa_mem duration: %s", totaltime)
    else:
        if(verbose):
            LOG.critical("pie_bwa_mem: either bwa mem is still running or its errored out with returncode:%d",retcode)
    return 0       

def setlogging(logfile=None):
    consolelevel = logging.DEBUG
    logger = logging.getLogger(__name__)
    logger.setLevel(consolelevel)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(consolelevel)
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    
    # create file handler which logs error messages
    if logfile:
        filelevel = logging.ERROR
        fh = logging.FileHandler(logfile)
        fh.setLevel(filelevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    #test logging
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    
    return logger

if __name__ == '__main__':
    start_time = time.time()  
    status = main()
    end_time = time.time()
    LOG.info("Elapsed time was %g seconds" % (end_time - start_time))
    sys.exit(status)
