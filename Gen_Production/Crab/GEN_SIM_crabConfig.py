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
STORAGE_SITE  = 'T3_US_NotreDame'          # replace, e.g. T2_US_UCSD

# ── Each submission must run in its own process (CMSSW cfg can only be
#    loaded once per Python process; multiprocessing resets the cache) ────────
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

for mp in MASS_POINTS:
    p = Process(target=submit, args=(mp,))
    p.start()
    p.join()  # wait for each to finish before starting the next
