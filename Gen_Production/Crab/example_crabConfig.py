import CRABClient
from CRABClient.UserUtilities import config
from WMCore.Configuration import Configuration

config = config()

config.General.requestName = 'Scouting_Run2024F_IsoMu27_JanTagger_V3'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '2024Data.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/ScoutingPFRun3/Run2024F-v1/HLTSCOUT'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10  # Reduced from 50 to avoid wall clock time limit
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24/2024F_Golden.json'
config.Data.publication = True
config.Data.outputDatasetTag = 'Scouting_Run2024F_IsoMu27_JanTagger_V3'


config.Site.storageSite = 'T3_US_NotreDame'
