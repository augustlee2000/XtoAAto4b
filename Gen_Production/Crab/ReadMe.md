# How to use Crab
Crab is natively built into any CMSSW release and allows users to run complex scripts on their data using the computing pool from any member institution. Think of crab as any other batch system, like HtCondor, but it can run your CMSSW release natively, unlike Condor. So for anyone at ND looking to use a CMSSW release, you have three options: locally, lobster, or crab. While locally is the easiest, it is by far the slowest method and is absolutely impractical once you have to run 10k-plus events most of the time. Lobster is a home-built tool developed by Kevin's group that allows you to use Condor worker nodes with your CMSSW release. ND has a large computing cluster, which means that Lobster is your fastest option, but from my experience very difficult to get running. If you plan to spend a large portion of your analysis running CMSRun scripts, looking into lobster might be beneficial. But if you are going to use the cmsRun script occasionally or for a single step in your analysis (like MC generation), then crab should be your choice

## Basic Crab Setup

Before starting this tutorial, I will assume you have a proper CMSSW environment and a cmsRun script that runs locally.

In this folder, you will see example.py and example_crabConfig.py. These are both taken from a ScoutingNano script. I more or less want to show what you need to change in the test.py script and what a simple crab configuration file looks like. But before we look at that, we should make sure crab is set up properly.

At ND, I identified some unique issues through emails and trial and error. So, before you do anything in Crab, I recommend following these commands

```
source /cvmfs/cms.cern.ch/common/crab-setup.sh
/cvmfs/cms.cern.ch/common/cmssw-el8 --cleanenv -B /scratch365/ -B /opt/ -B /cvmfs/
cmsenv
crab checkwrite --site=T3_US_NotreDame
```

This source shows how to set up crab, creates a singularity for your CMSSW release (it can be el8 or el9, depending on your release), sets up your cms environment, and then the final step is to check if you can write to the tier 3. 

As a side note, it really doesn't like to play with a conda environment, so if you have one active, even a base conda environment, you should do 

```
conda deactivate
source /cvmfs/cms.cern.ch/common/crab-setup.sh
/cvmfs/cms.cern.ch/common/cmssw-el9 --cleanenv -B /scratch365/ -B /opt/ -B /cvmfs/
conda deactivate
cmsenv
crab checkwrite --site=T3_US_NotreDame
```
# Basic Script and Crab Configuration
In this folder, you will see example.py and example_crabConfig.py. These are both taken from a ScoutingNano script. I more or less want to show what you need to change in the test.py script and what a simple crab configuration file looks like. But before we look at that, we should make sure crab is set up properly.

In example.py, the only thing you need to change is how you are pointing the script to your file. So the commented section is what you would normally have when you run the script locally is what is required for crab 

```
process.source = cms.Source("PoolSource",
	 fileNames = cms.untracked.vstring(),
        secondaryFileNames = cms.untracked.vstring()
)

# Input source
# process.source = cms.Source("PoolSource",
#     fileNames = cms.untracked.vstring('/store/data/Run2024F/ScoutingPFRun3/HLTSCOUT/v1/000/383/779/00000/ac2fde62-8866-4e50-8f36-77d604bfd4e1.root'),
#     secondaryFileNames = cms.untracked.vstring()
# )

```

Luckily, this is the only change you need to make to your cmsRun script!

Now for the crab configuration script! Now I am going to highlight each section

```
import CRABClient
from CRABClient.UserUtilities import config
from WMCore.Configuration import Configuration

config = config()

config.General.requestName = 'Scouting_Run2024F_IsoMu27_JanTagger_V3'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
```

This first part is setting up your general workspace, so you are giving your request a name (it has to be unique, so if you submit it again, you need to change the name), where to save all output information (not your root file), and if you want to transfer your outputs.

```
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'example.py'
config.JobType.allowUndistributedCMSSW = True
```

This section specifies which script to run and whether anything special needs to happen.


```
config.Data.inputDataset = '/ScoutingPFRun3/Run2024F-v1/HLTSCOUT'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10  # Reduced from 50 to avoid wall clock time limit
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24/2024F_Golden.json'
config.Data.publication = True
config.Data.outputDatasetTag = 'Scouting_Run2024F_IsoMu27_JanTagger_V3'


config.Site.storageSite = 'T3_US_NotreDame'
```
Now, finally, this tells the crab about the job, so `config.Data.inputDataset = '/ScoutingPFRun3/Run2024F-v1/HLTSCOUT' tells it which dataset to run on. 
```
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10  # Reduced from 50 to avoid wall clock time limit
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24/2024F_Golden.json'
```
This job is quite large, so I'll split it by luminosity, use 10 luminosity segments per job, and finally run only the jobs in the golden.json.

```
config.Data.publication = True
config.Data.outputDatasetTag = 'Scouting_Run2024F_IsoMu27_JanTagger_V3'


config.Site.storageSite = 'T3_US_NotreDame'
```

Now finally this is telling you how to save it, this will save it under the tag of `Scouting_Run2024F_IsoMu27_JanTagger_V3` this doesn't have to be unqiue but is easiser when you run alot of these jobs, and now finally it says to save it here at ND, you will be able to find your file under `/cms/cephfs/data/store/user/<cern username>/`

Luckily for us, all the configurations are well-defined on the [TWiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile), and LLMs like Claude and ChatGPT are pretty good at making them.


Now that you have both your script and your configuration file, you just have to submit it with `crab submit -c example_crabConfig.py`


## How to use Crab for the Gridpack to GEN-SIM Step

Everyone must create a local GEN-SIM root file before requesting central production. Producing a single event takes almost 1 minute, so generating hundreds to thousands of these events for each mass hypothesis would be a multi-week to a month challenge. Once again, crab can come in for the rescue, where I was able to produce 2k events per mass hypothesis in under 3 hours. 

For the first thing you want to do is modify our start-up commands

```
source /cvmfs/cms.cern.ch/common/crab-setup.sh
/cvmfs/cms.cern.ch/common/cmssw-el8 --cleanenv -B /scratch365/ -B /opt/ -B /cvmfs/
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh
crab checkwrite --site=T3_US_NotreDame
```
Why we have to do the crab setup twice, I have no clue, but this works. We need to do this because this time around we are submitting using Python and not `crab submit`, this is done so that we just have a list of all of our mass hypotheses, and we don't need to submit 20 to 30 unique crab jobs.

Let's look at the GEN_SIM.py script, this take my gridpack and turns it into a GEN-SIM root file. The first thing to look at is,

```
options = VarParsing('analysis')
options.register('gridpack',
    'Xtophiphito4b_X400P40_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'Gridpack tarball filename (basename only; must be in /srv/)')
options.parseArguments()

```

 and
 
```
process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/srv/' + options.gridpack),
    generateConcurrently = cms.untracked.bool(False),
    nEvents = cms.untracked.uint32(100),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)
```

These lines allow the command to look like `cmsRun GEN_SIM.py <tarball.tar.xz>` because we aren't only importing the script; we have to import the tarball as well. This tarball gets saved in the `/srv/` directory. We can't hardcode the names or their directory, so it has to be a parameter we can change, which is what both these lines do. The next line is 

```

generateConcurrently = cms.untracked.bool(False),

```

This makes the LHE step only run on one thread; crab can't do multithread processing like this, so it is safer to do it this way. And finally,

```
import random
process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = random.randint(1, 1000000)
```


For each job, we need a unique random number. The likelihood of the same random number is really low; we could select the same number twice, but it should be super rare

Now we can look at the config file, as I have said before, submitting 20+ crab jobs is not what we want to do, so let's take a look at the GEN_SIM_crabConfig.py.

```
from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process

# ── Add / remove mass points here ────────────────────────────────────────────
MASS_POINTS = [
    'X400P40',
    'X500P200',
    # 'X600P100',
    # 'X700P300',
    # ... add the re
]

GRIDPACK_DIR = '/users/alee43/SignalCreation/Gridpack/genproductions_scripts/bin/MadGraph5_aMCatNLO'
GRIDPACK_SUFFIX = '_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'
CERN_USERNAME = 'aulee'   # replace
STORAGE_SITE  = 'T3_US_NotreDame'
```

This is setting up our imports, mass points, where it can find my gridpacks, the suffix of my gridpack, username, and where to store the gridpacks. Replace this with your specific needs.

```
def submit(mp):
    gridpack = f'{GRIDPACK_DIR}/Xtophiphito4b_{mp}{GRIDPACK_SUFFIX}'
    tag = f'Xtophiphito4b_{mp}'

    cfg = config()

    cfg.General.requestName      = f'{tag}_GEN-SIM_v9'
    cfg.General.workArea         = 'crab_projects'
    cfg.General.transferOutputs  = True
    cfg.General.transferLogs     = True

    cfg.JobType.pluginName               = 'PrivateMC'
    cfg.JobType.psetName                 = 'GEN-RunIII2024Summer24wmLHEGS-00001_1_cfg.py'
    cfg.JobType.inputFiles               = [gridpack]
    cfg.JobType.pyCfgParams              = [f'gridpack=Xtophiphito4b_{mp}{GRIDPACK_SUFFIX}']
    cfg.JobType.allowUndistributedCMSSW  = True
    cfg.JobType.maxMemoryMB              = 3000     # T3_US_NotreDame max for 1-core jobs

    cfg.Data.splitting               = 'EventBased'
    cfg.Data.unitsPerJob             = 100
    cfg.Data.totalUnits              = 2000         # 20 jobs x 100 events
    cfg.Data.publication             = False

    cfg.Site.storageSite = STORAGE_SITE

    crabCommand('submit', config=cfg)

```

This function defines all of the crab configuration we need. I want to point out a few things,

```
cfg.JobType.inputFiles               = [gridpack]
cfg.JobType.pyCfgParams              = [f'gridpack=Xtophiphito4b_{mp}{GRIDPACK_SUFFIX}']

```
This tells the crab that we should import our gridpack and that the pyCfgParams we should pass to this gridpack as a parameter to our cmsRun command.

```
cfg.Data.splitting               = 'EventBased'
cfg.Data.unitsPerJob             = 100
cfg.Data.totalUnits              = 2000         # 20 jobs x 100 events
```
This part tells me to split my jobs based on the number of events: each job should handle 100 events, and it should make 2000 events. Now, finally, the last part

```
for mp in MASS_POINTS:
    p = Process(target=submit, args=(mp,))
    p.start()
    p.join()  # wait for each to finish before starting the next

```

This loops over all the MASS_POINTS and submits a new crab job for each.

Now you are done, you can run `python3 GEN_SIM_crabConfig.py` and hopefully everything runs how you want, and you can make 2k x mass values of events in a single afternoon. 


This is unfortnuilty not a bullet proof guide, but LLM are good, and I have seen many issue before so please reach out to your favorite AI or myself and I can hopefully get everything fixed!



