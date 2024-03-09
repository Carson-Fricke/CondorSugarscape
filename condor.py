import sys
import subprocess as s
from codegen import parseConfiguration


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(0)

    conf = sys.argv[1]
    ns, dms, options = parseConfiguration(conf)

    for dm in dms:
        for seed in range(ns):
            s.run(['condor_submit', f'{dm}-{seed}.submit'])
