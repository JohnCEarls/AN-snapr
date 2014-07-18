
def main():
    from ansnapr.utils import debug
    import masterdirac.models.systemdefaults as sys_def
    debug.InitLogging()
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
            d.run()
            running = d.restart
            if not running:
                d.terminate_response()
    except:
        logger = logging.getLogger("server.main")
        logger.exception("Process killing error")

if __name__ == "__main__":
    #the server initialization will go here
    print "Executions starts in main()"
