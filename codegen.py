import json
import sys

def parseConfiguration(configFile):
    file = open(configFile)
    options = json.loads(file.read())
    dco = {}
    sso = {}
    num_seeds = 0
    dec_models = []

    # If using the top-level config file, access correct JSON object
    if 'dataCollectionOptions' in options:
        dco = options['dataCollectionOptions']

    if 'sugarscapeOptions' in options:
        sso = options['sugarscapeOptions']

    # Keep compatibility with outdated configuration files
    dcokeys = dco.keys()
    if 'numSeeds' in dcokeys:
        num_seeds = dco['numSeeds']
    if 'decisionModels' in dcokeys:
        dec_models = dco['decisionModels']
    return num_seeds, dec_models, options

def make_config(confo, seed: int, dec_model: str):

    options = confo

    if 'dataCollectionOptions' in options:
        dco = options['dataCollectionOptions']

    options['dataCollectionOptions']['decisionModels'] = [dec_model]
    options['sugarscapeOptions']['seed'] = seed
    options['sugarscapeOptions']['logfile'] = f'{dec_model}-{seed}log.json'

    # options that must be set for propper running
    # Right now, we will not support profiling, screenshots, or plots
    options['dataCollectionOptions']['plots'] = []
    options['dataCollectionOptions']['pythonAlias'] = 'python3'
    options['dataCollectionOptions']['numSeeds'] = 1
    options['dataCollectionOptions']['numParallelSimJobs'] = 1
    options['sugarscapeOptions']['headlessMode'] = True
    options['sugarscapeOptions']['profileMode'] = False
    options['sugarscapeOptions']['screenshots'] = False

    out = json.dumps(options)
    
    with open(f'{dec_model}-{seed}conf.json', 'w') as f:
        f.truncate(0)
        f.write(out)

    



# very silly indenting syntax incoming
def make_description(configf, num_seeds: int, dec_model: str):
    with open(configf, 'r+') as f:
        f.truncate(0)
        f.write(
f'''
+sugarscape_simulation = true

executable = python3
transfer_input_files = {inputpov}, WRC_RubiksCube.inc
arguments = +I{inputpov} +Oframe$(Process).png Width={renderwidth} Height={renderheight} +K$$([$(Process) * {1 / float(frames):.3f}])

request_cpus = 1
request_memory = 4096M
request_disk = 1G

error = err.log
output = output{renderheight}p.log
log = povray.log

transfer_output_files = frame$(Process).png

should_transfer_files = YES
queue {frames}
''')

if __name__ == '__main__':

    if len(sys.argv) != 2:
        exit(0)

    conf = sys.argv[1]
    ns, dms, options = parseConfiguration(conf)
    
    for dm in dms:
        for seed in range(ns):
            make_config(options, seed, dm)

    pass


