'''

Created on 07/31/2014
@Ronak Shah

'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import sys
import time
import os.path
import stat
from subprocess import Popen,PIPE
import shlex
import shutil
from datetime import date, timedelta
import logging
import pie

try:
    import coloredlogs
except ImportError:
    print(
        "pie_pindel: coloredlogs is not installed, please install it if you wish to see color in logs on standard out."
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
	description='Run Pindel for Long Indels & MNPS (32bp-350bp)', 
	usage='%(prog)s [options]')
    parser.add_argument(
	"-i", 
	"--pindelConfig", 
	dest="config", 
	required=True, 
	help="Full path to the pindel configuration [required]") 
    parser.add_argument(
	"-pID", 
	"--patientID", 
	dest="patientID", 
	required=True, 
	help="Id of the Patient for which the bam files are to be realigned [required]")
    parser.add_argument(
	"-v", 
	"--verbose", 
	action="store_true", 
	dest="verbose",  
	help="make lots of noise")
    parser.add_argument(
	"-c", 
	"--cores",  
	dest="cores", 
	required=True, 
	default=5, 
	help="Number of cores to be used to run Pindel [default=5] [required]")
    parser.add_argument(
	"-ref", 
	"--reference_sequence",  
	dest="reference_sequence", 
	choices=pie.util.genomes.keys(),
	required=True, 
	help="Full Path to the reference file with the bwa index. [required]")
    parser.add_argument(
	"-pd", 
	"--pindelExe",
	dest="PINDEL", 
	required=True,  
	help="Full Path to the Pindel executables. [required]")
    parser.add_argument(
	"-chr", 
	"--chromosomes", 
	dest="chr", 
	required=True, 
	default="ALL", 
	help="Which chr/fragment Pindel will process reads for one chromosome each time. ChrName must be the same as in reference sequence and in read file. [required]")
    parser.add_argument(
	"-q", 
	"--queue",  
	dest="queue",   
	help="Name of the SGE queue (all.q or clin.q)")
    parser.add_argument(
	"-o", 
	"--output_bam", 
	dest="output_bam", 
	required=True, 
	help="Full Path to the output dir. [required]")
    parser.add_argument(
	"-op", 
	"--outPrefix", 
	dest="outprefix", 
	required=True,  
	help="Id of the Tumor bam file which will be used as the prefix for Pindel output files [required]")
   # parser.add_argument("-tr", "--targetRegion", action="store", dest="targetRegion", required=True, metavar='/somepath/targetRegion.bed', help="Full Path to bedfile for target region.")
    parser.add_argument(
        "-L",
        "--log",
        dest="logfile",
        required=True,
        help="write debug log to FILENAME [required]")

    args = parser.parse_args()
    LOG = setlogging(args.logfile, program_name)
    return args   
   




def ProcessArgs(args):
    if(args.verbose):
        print "I am currently processing the arguments.\n"
    tumorBam = '' 
    with open(args.config, 'r') as filecontent:
        for line in filecontent:
            if(args.patientID not in line):
                continue
            else:
                data = line.rstrip('\n').split('\t')
                tumorBam = os.path.basename(data[0]).rstrip('.bam')
                break
    outvcf = tumorBam + ".pindel.detailed.TN.matched.vcf"
    SampleDirName = args.patientID
    staticDir = "PindelAnalysis"
    AnalysisDir = os.path.join(args.output_bam, staticDir)
    SampleAnalysisDir = os.path.join(AnalysisDir, SampleDirName)
    #pindeltag=0
    try:
        os.mkdir(AnalysisDir)
    except OSError:
        if(args.verbose):
            print "Dir:", AnalysisDir, " exists thus we wont be making it\n"
    if os.path.isdir(SampleAnalysisDir):
            if(args.verbose):
                print "Dir:", SampleAnalysisDir, " exists and we wont run the analysis\n"
            #pindeltag = 0
    else:
        os.makedirs(SampleAnalysisDir)
        #pindeltag = 1
    if(args.verbose):
        print "I am done processing the arguments.\n"   
    
    return(outvcf)


def main(argv=None):
    
    args=process_command_line(argv)
    day = date.today()
    today = day.isoformat()
    today = today.replace("-", "")
    myPid = os.getpid()
    pindel = os.path.join(args.PINDEL, "pindel")
    pindel2vcf = os.path.join(args.PINDEL, "pindel2vcf")
    (vcfoutName) = ProcessArgs(args)
    vcfOutPath = os.path.join(args.output_bam, vcfoutName)
    p2v_cmd = ''
 
    # myPid = str(myPid)
    if(args.verbose):
        print "I am running Pindel for ", args.patientID, " using SGE/LSF"
    
    # Setting Job for SGE   
    if (args.PINDEL):
	pindel = os.path.join(args.PINDEL, "pindel")
	cmd = pindel
    if (args.config):
	config =  " -i " + args.config
	cmd = cmd + config
    if (args.reference_sequence):
	ref = " -f " + args.reference_sequence 
	cmd = cmd + ref
    if (args.chr):
	chromosome = " -c " + args.chr 
	cmd = cmd + chromosome
    if (args.outprefix):
	outpre = " -o " + args.outprefix 
	cmd = cmd + outpre
   
    cmd = cmd + " -r false -t false -I false"
        # print "CMD==>",cmd,"\n"   

    print "Cluster_CMD==>", cmd , "\n"
    cl_args = shlex.split(cmd)
    proc = Popen(cl_args, shell=True, stdout=PIPE, stderr=PIPE)
    proc.wait()
    retcode = proc.returncode
    if(retcode >= 0):
        if(args.verbose):
            print "I have finished running Pindel for ", args.patientID, " using SGE/LSF"
        if(os.path.isfile(vcfOutPath)):
            retcode = 1
        else:
            p2v_cmd = pindel2vcf
	    if (args.outprefix):
		outpre = " --pindel_output_root " + args.outprefix
		p2v_cmd = p2v_cmd + outpre
	    if (args.reference_sequence):
		ref= " --reference " + args.reference_sequence
		p2v_cmd = p2v_cmd + ref
	    p2v_cmd = p2v_cmd +  " --reference_date " + today + " --vcf " + vcfOutPath + " -b true --gatk_compatible "         
           
            print ("P2V cmd: " + p2v_cmd)
	    print ("\n \n The followng cmd has been run: " + cmd + p2v_cmd)
            p2v_args = shlex.split(p2v_cmd)
            proc = Popen(p2v_args, shell=True, stdout=PIPE, stderr=PIPE)
            proc.wait()
            retcode = proc.returncode
        if(retcode >= 0):
            if(args.verbose):
                print "Converted Pindel Output to VCF\n"
        else:
            if(args.verbose):
                    print "Pindel2Vcf is either still running or it errored out with return code", retcode, "\n"        
    else:
        if(args.verbose):
            print "Pindel is either still running or it errored out with return code", retcode, "\n"    


               
    
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
