import logging
import multiprocessing

def build_genome_index( genome_file, index_dir, **kwargs ):
    """
        Usage: snapr index <input.fa> <output-dir> [<options>]
        Options:
        -s               Seed size (default: 20)
        -h               Hash table slack (default: 0.3)
        -hg19            Use pre-computed table bias for hg19, which results in better speed, balance, and memory footprint but may not work for other references.
        -Ofactor         This parameter is deprecated and will be ignored.
        -tMaxThreads      Specify the maximum number of threads to use. Default is the number of cores.
        -B<chars>     Specify characters to use as chromosome name terminators in the FASTA header line; these characters and anything after are
               not part of the chromosome name.  You must specify all characters on a single -B switch.  So, for example, with -B_|,
               the FASTA header line '>chr1|Chromosome 1' would generate a chromosome named 'chr1'.  There's a separate flag for
               indicating that a space is a terminator.
        -bSpace       Indicates that the space character is a terminator for chromosome names (see -B above).  This may be used in addition
               to other terminators specified by -B.  -B and -bSpace are case sensitive.
        -pPadding         Specify the number of Ns to put as padding between chromosomes.  This must be as large as the largest
                   edit distance you'll ever use, and there's a performance advantage to have it be bigger than any
                   read you'll process.  Default is 500
        -HHistogramFile   Build a histogram of seed popularity.  This is just for information, it's not used by SNAP.
        -exact            Compute hash table sizes exactly.  This will slow down index build, but may be necessary in some cases
        -keysize          The number of bytes to use for the hash table key.  Larger values increase SNAP's memory footprint, but allow larger seeds.  Default: 4
        -large            Build a larger index that's a little faster, particualrly for runs with quick/inaccurate parameters.  Increases index size by
                   about 30%, depending on the other index parameters and the contents of the reference genome

    """
    print _gi_command( genome_file, index_dir, **kwargs)

def _gi_command( genome_file, index_dir, **kwargs ):
    command = "snapr index %s %s " % (genome_file, index_dir)
    for key, value in kwargs.iteritems():
        if value:
            command = "%s -%s%s" % (command, key, value)
        else:
            command = "%s -%s" % (command, key )
    return command


def build_transcriptome_index( annotation_file, genome_file, transcriptome_dir, **kwargs ):
    """
        Usage: snapr transcriptome <input.gtf> <input.fa> <output-dir> [<options>]
        Options:
        -s               Seed size (default: 20)
        -h               Hash table slack (default: 0.3)
        -hg19            Use pre-computed table bias for hg19, which results in better speed, balance, and memory footprint but may not work for other references.
        -Ofactor         This parameter is deprecated and will be ignored.
        -tMaxThreads      Specify the maximum number of threads to use. Default is the number of cores.
        -B<chars>     Specify characters to use as chromosome name terminators in the FASTA header line; these characters and anything after are
               not part of the chromosome name.  You must specify all characters on a single -B switch.  So, for example, with -B_|,
               the FASTA header line '>chr1|Chromosome 1' would generate a chromosome named 'chr1'.  There's a separate flag for
               indicating that a space is a terminator.
        -bSpace       Indicates that the space character is a terminator for chromosome names (see -B above).  This may be used in addition
               to other terminators specified by -B.  -B and -bSpace are case sensitive.
        -pPadding         Specify the number of Ns to put as padding between chromosomes.  This must be as large as the largest
                   edit distance you'll ever use, and there's a performance advantage to have it be bigger than any
                   read you'll process.  Default is 500
        -HHistogramFile   Build a histogram of seed popularity.  This is just for information, it's not used by SNAP.
        -exact            Compute hash table sizes exactly.  This will slow down index build, but may be necessary in some cases
        -keysize          The number of bytes to use for the hash table key.  Larger values increase SNAP's memory footprint, but allow larger seeds.  Default: 4
        -large            Build a larger index that's a little faster, particualrly for runs with quick/inaccurate parameters.  Increases index size by
                   about 30%, depending on the other index parameters and the contents of the reference genome

    """
    print _ti_command( annotation_file, genome_file, transcriptome_dir, **kwargs )


def _ti_command( annotation_file, genome_file, transcriptome_dir, **kwargs ):
    command = "snapr transcriptome %s %s %s" %  ( annotation_file, genome_file, transcriptome_dir)
    for key, value in kwargs.iteritems():
        if value:
            command = "%s -%s%s" % (command, key, value)
        else:
            command = "%s -%s" % (command, key )
    return command

def _align_command( read_type, index_dir, transcript_dir, annotation, read_file, out_file , sort=False):
    command = "snapr %s %s %s %s %s -o %s" % ( read_type, 
            index_dir, 
            transcript_dir, 
            annotation, 
            read_file, 
            out_file )
    if sort:
        command += " -so"
    return command

if __name__ == "__main__":
    print "Subprocesses test"
    kwargs = {'switch':'Value',
            'switch2': None,
            
            }
    print "Transcriptome Index builder"
    build_transcriptome_index("annotation_file", "genome_file", "test_index_dir", **kwargs)
    print 
    print "Genome Index builder"
    build_genome_index("annotation_file",  "test_index_dir", **kwargs)

    print _align_command( "single", "index-dir", "transcriptome-dir", "annotation", "read_file", "out_file" )
