import subprocess
from util.logger import Logger

class Adb(object):
    serial = ''
    legacy = False
    
    @staticmethod
    def init(config, legacyArg=False):
        """Initialize class fields
        """
        Adb.serial = config.adb['serial']
        Adb.legacy = legacyArg

    @staticmethod
    def check_state():
        """Method that checks if the device is attached and ready to be used.

        Returns:
            (boolean): True if everything is ready, False otherwise.
        """
        cmd = ['adb', '-s', Adb.serial, 'get-state']
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        state = process.communicate()[0].decode()
        return state.find('device') == 0

    @staticmethod
    def start_server():
        """Starts the ADB server
        """
        cmd = ['adb', 'start-server']
        subprocess.call(cmd)

    @staticmethod
    def kill_server():
        """Kills the ADB server
        """
        cmd = ['adb', 'kill-server']
        subprocess.call(cmd)

    @staticmethod
    def exec_out(args):
        """Executes the command via exec-out

        Args:
            args (string): Command to execute.

        Returns:
            tuple: A tuple containing stdoutdata and stderrdata
        """
        cmd = ['adb', '-s', Adb.serial, 'exec-out'] + args.split(' ')
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        return process.communicate()[0]

    @staticmethod
    def shell(args):
        """Executes the command via adb shell

        Args:
            args (string): Command to execute.
        """
        cmd = ['adb', '-s', Adb.serial, 'shell'] + args.split(' ')
        Logger.log_debug(str(cmd))
        subprocess.call(cmd)
