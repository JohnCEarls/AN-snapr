import logging
import multiprocessing
import boto.utils
import json

class SNAPr:
    def __init__(self, directories, init_q):
        self._name = None
        self.directories = directories
        self.init_q = init_q
        self.logger = logging.getLogger( self.name )
        self.logger.info("Initializing: directories<%s> init_q<%s>" % (
            json.dumps(directories), init_q) )

    @property
    def name( self ):
        if self._name is None:
           self._name = self._generate_name()
        else:
           return self._name

    def _generate_name( self ):
        """
        Create a unique name for this process
        """
        md =  boto.utils.get_instance_metadata()
        pid = str( multiprocessing.current_process().pid )
        name_patt = "ansnapr.server.SNAPr-%s-%s"
        return name_patt % (md['instance-id'], pid )

    def run(self):
        self.logger.info("entering main loop (run())")


        self.logger.info("exitting main loop (run())")

    def terminate_response(self):
        self.logger.info("Sending response to master server")
        #TODO

def build_genome_index( dna_file, index_dir, **kwargs ):
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
SNAP exited with exit code 1 from line 112 of file SNAPLib/GenomeIndex.cpp

    """
    command = "snapr index %s %s " % (dna_file, index_dir)
    for key, value in kwargs.iteritems():
        if value:
            command = "%s -%s%s" (command, key, value)
        else:
            command = "%s -%s" (command, key )


def build_transcriptome_index( dna_file, index_dir, **kwargs ):
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
SNAP exited with exit code 1 from line 112 of file SNAPLib/GenomeIndex.cpp

    """
    command = "snapr transcriptome %s %s "
    for key, value in kwargs.iteritems():
        if value:
            command = "%s -%s%s" (command, key, value)
        else:
            command = "%s -%s" (command, key )





def main():
    from ansnapr.utils import debug
    import masterdirac.models.systemdefaults as sys_def
    debug.initLogging()
    local = sys_def.get_system_defaults( component='Master', 
            setting_name="local_settings")
    init_q = local['init-queue']
    directories = {}
    directories = sys_def.get_system_defaults(component='SNAPR',
            setting_name='directories')

    try:
        running = True
        while running:
            s = SNAPr( directories, init_q )
            s.run()
            s.terminate_response()
    except:
        logger = logging.getLogger("server.main")
        logger.exception("Process killing error")

if __name__ == "__main__":
    #the server initialization will go here
    print "Executions starts in main()"
