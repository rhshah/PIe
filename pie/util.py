import json
import logging
import os
import sys

RESOURCE_FILE = os.getenv('PIE_RESOURCE_CONFIG', "pie_resources.json")
JSON_CONFIG = json.load(open(RESOURCE_FILE))
programs = JSON_CONFIG['programs']
genomes = JSON_CONFIG['genomes']
chr1_fingerprints = JSON_CONFIG['chr1_fingerprints']
keys = JSON_CONFIG['keys']
targets = JSON_CONFIG['targets']
config = JSON_CONFIG['config']
FORMAT = '%(asctime)-15s %(funcName)-8s %(levelname)s %(message)s'
OUT_HANDLAR = logging.StreamHandler(sys.stdout)
OUT_HANDLAR.setFormatter(logging.Formatter(FORMAT))
OUT_HANDLAR.setLevel(logging.INFO)
LOGGER = logging.getLogger('pie')
LOGGER.addHandler(OUT_HANDLAR)
LOGGER.setLevel(logging.INFO)


def picard_std_args(parser):
    parser.add_arguments(
        "-tmp",
        "--tmp_dir",
        dest="tmp_dir",
        default="/scratch/",
        help="path to the temporary directory")
    parser.add_arguments(
        "-s",
        "--validation_stringency",
        dest="validation_stringency",
        default="SILENT",
        help=
        "Validation stringency for all SAM files read by this program. Setting stringency to SILENT can improve performance when processing a BAM file in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.[default=SILENT]"
    )
    parser.add_arguments(
        "-c",
        "--compression_level",
        dest="compression_level",
        default="5",
        help=
        "Compression level for all compressed files created (e.g. BAM and GELI).[default=5]"
    )
    parser.add_arguments(
        "-ci",
        "--create_index",
        dest="create_index",
        default="true",
        help=
        "Whether to create a BAM index when writing a coordinate-sorted BAM file.[default=true]"
    )
    parser.add_arguments(
        "-cm",
        "--create_md5_file",
        dest="create_md5_file",
        default="false",
        help=
        "Whether to create an MD5 digest for any BAM or FASTQ files created.[default=false]"
    )
    parser.add_arguments(
        "-ref",
        "--reference_sequence",
        dest="reference_sequence",
        choices=genomes.keys(),
        require=True,
        help="Reference sequence file.[required]")
    return (parser)
