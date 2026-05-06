# How to use Crab
Crab is nativily build into any CMSSW realase and allows useer to use the computing pool from any member instituation to do use complex scrips on their data. Think of crab like any other batch system like HtCondor, but it can nativily run your CMSSW release, unlike condor. So for anyone at ND looking to use a CMSSW release you have three options, locally, lobster or crab. While locally is the easiest it is by far the slowest method and is absoulty impractical once you have to run 10k plus events most of the time. Lobster is a home build tool developed by Kevin's group which allows you too use the condor worker nodes with your CMSSW release, ND has a large comuting cluser which means that lobsters is your fastest option but from my experience very difficult to get running, if you are planning on spending a large portion of your annalysis runing cmsRun scripts looking into lobster might be benifical. But if you are going to use cmsRun script occoncally or for a single step in your analysis (like MC generation) then crab should be your choice

## Basic Crab Setup

Before starting this tutorial I will assume you have a proper CMSSW enviroment and a cmsRun script that run locally.

In this folder you will see test.py and test_crabConfig.py these are both taken from a ScoutingNano script, I more or less want to show what you need to change in the test.py script and how a simple crab configuration file looks like. But before we look at that we should make sure crab is set up properly.

At ND there is some unqiue issue that are prevelant that I figured out through some email and trial and error. So before you do anything in crab I recommend following these commands

```
source /cvmfs/cms.cern.ch/common/crab-setup.sh
/cvmfs/cms.cern.ch/common/cmssw-el9 --cleanenv -B /scratch365/ -B /opt/ -B /cvmfs/
cmsenv
crab checkwrite --site=T3_US_NotreDame
```
