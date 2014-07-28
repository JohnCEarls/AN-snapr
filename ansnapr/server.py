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
