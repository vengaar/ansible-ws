import daemon
import os
import subprocess

def launch(folder):
    # os.mkdir(folder)
    fpid = os.path.join(folder, 'run.pid')
    fpid_out = os.path.join(folder, 'pid.out')
    fpid_err = os.path.join(folder, 'pid.err')

    with open(fpid_out, 'w+') as pid_out, open(fpid_err, 'w+') as pid_err:
        with daemon.DaemonContext(
            # files_preserve = [
            #   fh.stream,
            # ],
            working_directory=folder,
            # pidfile=lockfile.LockFile(fpid),
            stdout=pid_out,
            stderr=pid_err,
        ) as ctx:
            run(folder)

def run(folder):
    command = [
        # 'sleep 2',
        # '&&',
        # 'date',
        'ansible-playbook /home/vengaar/ansible-ws/test/data/playbooks/tags.yml -vvv',
    ]
    file_output = os.path.join(folder, 'run.out')
    file_error = os.path.join(folder, 'run.err')
    file_error = os.path.join(folder, 'run.in')
    with open(file_output, 'w+') as out, open(file_error, 'w+') as err:
        print(out.isatty())
        print(err.isatty())
        with subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            # stdout=out,
            # stderr=err
        ) as proc:
            pid = proc.pid
            return_code = proc.wait()

if __name__ == '__main__':
    folder = '/tmp/test'
    #run(folder)
    launch(folder)
