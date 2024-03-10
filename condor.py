#import shlex
import shlex
import sys
from time import sleep
import subprocess as s
from codegen import parseConfiguration
from subprocess import PIPE, run
import getpass

USER = getpass.getuser()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(0)

    conf = sys.argv[1]
    ns, dms, options = parseConfiguration(conf)

    for dm in dms:
        #s.run(['condor_submit', f'{dm}.submit'])
        for seed in range(ns):
            s.run(['condor_submit', f'{dm}-{seed}.submit'])


    while True:
        # for some reason using shlex was the only way to get the contraint to work propperly
        proc = run(shlex.split(f'''condor_q -constraint 'sugarscape_simulation_{USER} == true' -f "%s" JobStatus'''), stdout=PIPE)
        job_status = str(proc.stdout.decode('utf-8'))
        print(f'Jobs Left: {len(job_status)}; Idle: {job_status.count("1")}; Running: {job_status.count("2")}; On Hold: {job_status.count("5")}')
        if len(job_status) == 0:
            break
        if job_status.count("5") > 0:
            #_ = run(shlex.split(f"""condor_release -constraint 'sugarscape_simulation_{USER} == true'"""), stdout=PIPE)
            pass
        sleep(3)
        print('\033[1A', end='\x1b[2K')

    print('Job Complete!')