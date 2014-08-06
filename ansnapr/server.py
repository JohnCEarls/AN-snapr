import logging
import multiprocessing
import boto.utils
import json

class SNAPr:
    #STATES
    INIT = 'initializing'
    GEN_GI = 'generating-genome-index'
    GEN_TI = 'generating-transcriptome-index'
    ALIGN = 'aligning'
    READY = 'ready'
    ERROR = 'error'
    def __init__(self, directories, init_q):
        self._state = SNAPr.INIT
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

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def _generate_name( self ):
        """
        Create a unique name for this process
        """
        md =  boto.utils.get_instance_metadata()
        pid = str( multiprocessing.current_process().pid )
        name_patt = "ansnapr.server.SNAPr-%s-%s"
        return name_patt % (md['instance-id'], pid)

    def _get_settings(self):
        """
        Alert master to existence, via sqs with init_q_name
        Get initial settings
        """
        conn = boto.sqs.connect_to_region( 'us-east-1' )
        init_q = None
        ctr = 0
        self._generate_command_queues()
        while init_q is None and ctr < 6:
            init_q = conn.get_queue( init_q_name  )
            time.sleep(1+ctr**2)
            ctr += 1
        if init_q is None:
            self.logger.error("Unable to connect to init q")
            raise Exception("Unable to connect to init q")
        md =  boto.utils.get_instance_metadata()
        self._availabilityzone = md['placement']['availability-zone']
        self._region = self._availabilityzone[:-1]
        message = {'message-type':'snapr-init',
                'name': self.name,
                'cluster-name': self.get_cluster_name(),
                'instance-id': md['instance-id'],
                'command' : self.sqs['command'],
                'response' : self.sqs['response'],
                'zone':self._availabilityzone }
        m = Message(body=json.dumps(message))
        init_q.write( m )
        command_q = conn.get_queue( self.sqs['command'] )
        command = None
        while command is None:
            command = command_q.read( wait_time_seconds=20 )
            if command is None:
                self.logger.warning("No instructions in [%s]"%self.sqs['command'])
        self.logger.debug("Init Message %s", command.get_body())
        parsed = json.loads(command.get_body())
        command_q.delete_message( command )
        self._handle_command(parsed)
        try:
            self.logger.debug("sqs< %s > s3< %s > ds< %s > gpu_id< %s >" % (str(self.sqs), str(self.s3), str(self.data_settings), str(self.gpu_id)) )
        except AttributeError:
            self.logger.exception("Probably terminated before initialization")

    def get_cluster_name( self ):
        return '-'.join(socket.gethostname().split('-')[:-1])



    def run(self):
        self.logger.info("entering main loop (run())")
        self.logger.info("exitting main loop (run())")

    def terminate_response(self):
        self.logger.info("Sending response to master server")
        #TODO




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
