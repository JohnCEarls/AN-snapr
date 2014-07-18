import subprocess
import re
def get_unmounted():
    result = subprocess.check_output(['fdisk', '-l'], stderr=subprocess.STDOUT)
    unmounted_disks = []
    for line in result.split('\n'):
        m = re.match(r'Disk ([\/|\w]+) doesn\'t contain a valid partition table', line.strip())
        if m:
            unmounted_disks.append(m.group(1))
    return unmounted_disks

def format_disk( disk ):
    command = 'mkfs -t ext4 %s' % disk
    print command
    try:
        result = subprocess.check_output(command, shell=True)
        print result
        return result
    except:
        return False

def mount_all():
    command = 'mount -a'
    print command
    try:
        result =  subprocess.check_output(command, shell=True)
        print result
        return result
    except:
        print "*" * 25
        print "ERROR on mount all"
        print "*" * 25
        return False
if __name__ == "__main__":
    disks =  get_unmounted()
    disks.append('/dev/xvdab')
    formatted = []
    for disk in disks:
        print
        print "Formatting: %s" % disk
        if format_disk(disk):
            print "Format successful"
        else:
            print "Format unsuccessful"
    mount_all()
        
