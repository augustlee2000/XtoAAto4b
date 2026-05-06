# How to use Crab
Crab is natively built into any CMSSW release and allows users to run complex scripts on their data using the computing pool from any member institution. Think of crab as any other batch system, like HtCondor, but it can run your CMSSW release natively, unlike Condor. So for anyone at ND looking to use a CMSSW release, you have three options: locally, lobster, or crab. While locally is the easiest, it is by far the slowest method and is absolutely impractical once you have to run 10k-plus events most of the time. Lobster is a home build tool developed by Kevin's group which allows you too use the condor worker nodes with your CMSSW release, ND has a large comuting cluser which means that lobsters is your fastest option but from my experience very difficult to get running, if you are planning on spending a large portion of your annalysis runing cmsRun scripts looking into lobster might be benifical. But if you are going to use the cmsRun script occasionally or for a single step in your analysis (like MC generation) then crab should be your choice

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

This sources how to set up crab, creates a singularity for your CMSSW release (it can be el8 or el9, depending on your release), sets up your cms eviroment, and then the final step is to check if you can write to the tier 3. 

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
This job is quite large, so I'll split my jobs based on the luminosity and do 10 luminosity segments per job, and finally, only run on jobs in the golden.json.

```
config.Data.publication = True
config.Data.outputDatasetTag = 'Scouting_Run2024F_IsoMu27_JanTagger_V3'


config.Site.storageSite = 'T3_US_NotreDame'
```

Now finally this is telling you how to save it, this will save it under the tag of `Scouting_Run2024F_IsoMu27_JanTagger_V3` this doesn't have to be unqiue but is easiser when you run alot of these jobs, and now finally it says to save it here at ND, you will be able to find your file under `/cms/cephfs/data/store/user/<cern username>/`

Luckily for us, all the configurations are well-defined on the [TWiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile), and LLMs like Claude and ChatGPT are pretty good at making them.


Now that you have both your script and your configuration file you just have to submit it with `crab submit -c example_crabConfig.py`


## How to use Crab for Gridpack to GEN-SIM

A thing that almost everyone has to do it to make local GEN-SIM root file before asking for central production. The production of a single event take almost 1 minute, so getting hundreads to thousands of these events for every mass hypothosis would be a muliple week too month challenge. Once again crab can come in for the rescure where I was able to produce 2k events per mass hypothosis in under 3 hours. 

For the first thing you want to to do is modifiy our start up commands

```
source /cvmfs/cms.cern.ch/common/crab-setup.sh
/cvmfs/cms.cern.ch/common/cmssw-el8 --cleanenv -B /scratch365/ -B /opt/ -B /cvmfs/
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh
crab checkwrite --site=T3_US_NotreDame
```
why we have to do the crab setup twice I have no clue but this works. We need to do this because this time around we are submitting using python and not `crab submit`, this is done so that we just have a list of all of our mass hypthosis and we don't need to submit 20 to 30 unqiue crab jobs.
