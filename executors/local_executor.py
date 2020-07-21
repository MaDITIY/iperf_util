from subprocess import Popen, PIPE


class LocalExecutor:

    @staticmethod
    def execute(command, check_output=False):
        process = Popen(
            command,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        print(command)
        if check_output:
            result = process.communicate(), process.returncode
        else:
            result = process.poll()
        return result
