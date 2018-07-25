#!/usr/bin/env python
# encoding: utf-8
"""
pie_vardict.py

Created by Ronak Shah on April 12, 2018.
Copyright (C) 2018 Northwell Helth. All right reserved
"""

#import required modules for the script

from __future__ import print_function
import os
import sys
import logging
import shlex, shutil, stat
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
        "pie_vardict: coloredlogs is not installed, please install it if you wish to see color in logs on standard out."
    )
    pass
	
# initialize global logger
LOG = None

# meta information for the file
__all__ = []
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__date__ = '2018-02-12'
__updated__ = '2018-04-15'



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
'''  % (program_shortdesc, str(__date__))
    parser = ArgumentParser(
        description=program_license,
        formatter_class=RawDescriptionHelpFormatter)
# define options here:
    parser.add_argument(
        "-vv",
        "--vardict_version",
        choices=pie.util.programs['vardict'].keys(),
        required=True,
        dest="vardict_version",
        help="select which version of vardict you will like to run [required]")
    parser.add_argument(
	"-nID",
	"--normalID",
	dest="nID",
	required=True,
	help="Name for normal sample [required]")
    parser.add_argument(
	"-tID", 
	"--tumorID",
	dest="tID", 
	required=True, 
	help="Name for tumor sample [required]")
    parser.add_argument(
	"-pID", 
	"--patientID", 
	dest="patientID", 
	required=True, 
	help="Id of the Patient for which the VarDict has to be ran [required]")
    parser.add_argument(
	"-ref", 
	"--reference_sequence",  
	dest="reference_sequence",
	choices=pie.util.genomes.keys(), 
	required=True,  
	help="Full Path to the reference fasta [Required]")
    parser.add_argument(
    	"-tr",
	"--targetRegion",
	dest="targetRegion",
	required=True,
	help="Full path to bedfile for target region [required]")
    parser.add_argument(
        "-mq",
        "--mapq",
        dest="MAPQ",
	default=20,
        required=True,
        help="reads with mapping quality less than INT will be filtered and ignored [default=20][required]")
    parser.add_argument(
	"-in",
	"--input_bam_n",
	dest="input_bam_n",
	required=True,
	help="Full Path to normal bam file [required]")
    parser.add_argument(
	"-it",
	"--input_bam_t",
	dest="input_bam_t",
	required=True,
	help="path / name of tumor BAM FILENAME [required]")
    parser.add_argument(
	"-o",
	"--output",
	dest="output_bam",
	required=True,
	help="path to / name of the output BAM FILENAME [required]")
    parser.add_argument(
	"-vd", 
	"--vardictExe",
	dest="vardict", 
	required=True, 
	help="Full Path to the VarDict Java executables. [required]")
    parser.add_argument(
	"-tss", 
	"--testSomaticScript",
	dest="testSomatic", 
	required=True,  
	help="Full Path to the VarDict's testSomatic.R script [required]")
    parser.add_argument(
	"-v2v", 
	"--var2vcf",
	dest="var2vcf", 
	required=True,
	help="Full Path to the VarDict's var2vcf_somatic.pl script [required]")
    parser.add_argument(
	"-q", 
	"--queue", 
	dest="queue", 
	help="Name of the SGE queue")
    parser.add_argument(
        "-c",
        "--cores",
        dest="cores",
	default=10,
        help="number of cores to be used to run vardict [default=10]")
    parser.add_argument(
	"-qb", 
	"--quality_base",
	dest="quality_base", 
	required=True, 
	default=20, 
	help="BASE Quality Threshold. [default=20][required]")
    parser.add_argument(
	"-maf", 
	"--minimumAlternateFrequnecy", 
	dest="MAF", 
	required=True, 
	default=0.01, 
	help="Minimum Alternate Allele Frequency [default=0.01] [required]")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="make some noise")
    parser.add_argument(
        "-V", "--version", action="version", version=program_version_message)
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
		

def ProcessArgs(args):
    if(args.verbose):
	print ("I am curretly processing the arguments.\n")
    tumorBam = os.path.basename(args.input_bam_t).rstrip('.bam')
    outvcf = tumorBam + ".vardict.detailed.TN.matched.vcf"
    SampleDirName = args.patientID
    staticDir = "VarDictAnalysis"
    AnalysisDir = os.path.join(args.output_bam, staticDir)
    SampleAnalysisDir = os.path.join(AnalysisDir, SampleDirName)
    try:
        os.mkdir(AnalysisDir)
    except OSError:
        if(args.verbose):
            print ("Dir:", AnalysisDir, " exists thus we wont be making it\n")
    if os.path.isdir(SampleAnalysisDir):
            if(args.verbose):
                print ("Dir:", SampleAnalysisDir, " exists and we wont run the analysis\n")
            vardicttag = 0
    else:
        os.makedirs(SampleAnalysisDir)
        vardicttag = 1
    if(args.verbose):
        print ("I am done processing the arguments.\n")   
    
    return (outvcf)

		
# assigns value for each args, makes a command and runs it on the local machine
def main(argv=None):

    args = process_command_line(argv)
    (vcfoutName) = ProcessArgs(args)
    vcfOutPath = os.path.join(args.output_bam, vcfoutName)
    verbose = args.verbose
    day = date.today()
    today = day.isoformat()
    today = today.replace("-", "")
    myPid = os.getpid()


    cmd = ""
    vardict = pie.util.programs['vardict'][args.vardict_version]
    cmd = cmd + vardict
    if (args.cores):
	cores = " -th " + str(args.cores)
	cmd = cmd + cores
    if (args.reference_sequence):
	ref = " -G " + args.reference_sequence
	cmd = cmd + ref
    if (args.tID):
	tID = " -N " + args.tID
	cmd = cmd + tID
    if (args.input_bam_t and args.input_bam_n):
	bam = " -b " + args.input_bam_t + "|" + args.input_bam_n
	cmd = cmd + bam	
    if (args.MAPQ):
        MAPQ = " -Q " + str(args.MAPQ)
        cmd = cmd + MAPQ		
    if (args.quality_base):
        BASEQ = " -q " + str(args.quality_base)
        cmd = cmd + BASEQ
    if (args.MAF):
        MAF = " -f " + str(args.MAF)
        cmd = cmd + MAF
    cmd = cmd + " -C -z 1 -c 1 -S 2 -E 3 -x 2000 -X 5 "
    if (args.testSomatic and args.var2vcf and args.targetRegion):
	bed_pl_R = args. targetRegion + "|" + args.testSomatic +"|"+ args.var2vcf
	cmd = cmd + bed_pl_R
    if (args.tID and args.nID):
	IDs = " -N " + args.tID + "|"+ args.nID
	cmd = cmd + IDs
    cmd = cmd + MAF

    print("\n \n  The following cmd was created: \n" + cmd)

    if (verbose):
        LOG.info("all the input parameters look good for running vardict")
        LOG.info("process id:%s,date:%s", myPid, today)
	
	LOG.info("command being run \n %s", cmd)  

    # setup the command to run
    cl_args = shlex.split(cmd)
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    proc.wait()
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
                "finished running vardict,please find output in %s",
                args.output_bam)
            LOG.info("duration: %s", totaltime)
    else:
        if (verbose):
            LOG.critical(
                "vardict still running or its errored out with returncode:%d",
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
