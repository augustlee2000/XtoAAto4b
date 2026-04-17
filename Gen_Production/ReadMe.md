# Gen Produciton for the Run3 X->phi phi -> 4b

I'll explain how to take my data cards and create them into usable MINIAOD. We stop at MINIAOD for this scouting analysis so that the custom ScoutingNano with a custom b-tagger can be applied.

## Making cards

Luckily, this analysis has been done in RECO for Run 2, so most of the work has been done to make the card. I will explain the critical parts of the cards that need to be changed, but minor tweaks have been made and are not critical to producing Run 3 events.

### run_card.dat

Beam energy changed from 6500 to 6800 

### proc_card.dat
`[QCD] -> [Noborn = QCD]` <br>
ninja noinstall: this resolves an import error  

## Making the gridpack

To set up your environment properly, please follow the [How to produce gridpacks wiki](https://cms-generators.docs.cern.ch/how-to-produce-gridpacks/mg5-amcnlo/#generating-the-gridpack) 

Then you run the command of <br>

`./gridpack_generation.sh NAME CARDDIR RUNHOME QUEUE JOBSTEP SCRAM_ARCH CMSSW_VERSION` <br>

which for the X 1000 and A 100 looks like <br>

`./gridpack_generation.sh XtoAAto4b_X1000A50 cards/examples/XtoAAto4b/` <br>

This produces the gridpack as a tarball, which leads us into the next step

## Making the LHE file
This next step is taking the tarball to the LHE step; at the moment, I am using Rob's Pythia fragment for X to phi phi to 4-photon. Some of the values might need to change. This part needs to be done in the correct CMSSW environment for the correct year. In this example, we are talking about 2024 MC samples. If testing for another year, please look up the recommended CMSSW version.

Please see [XtoPHiPHito4b_pythia.py](https://github.com/augustlee2000/XtoAAto4b/blob/main/Gen_Production/CMS%20Run%20Scripts/XtoPhiPhito4b_pythia.py)

## LHE to RAW-Sim

We now have the LHE, and we want to convert it into a RAW-SIM version. To produce the configuration file that we might want we need to use a cmsDriver command of,

```
cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-02112-fragment.py \
  --eventcontent RAWSIM,LHE \
  --customise Configuration/DataProcessing/Utils.addMonitoring \
  --datatier GEN-SIM,LHE \
  --conditions 102X_upgrade2018_realistic_v11 \
  --beamspot Realistic25ns13TeVEarly2018Collision \
  --customise_commands 'process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int(${SEED});process.externalLHEProducer.args=cms.vstring("/path/to/your/gridpack.tar.xz")' \
  --step LHE,GEN,SIM \
  --geometry DB:Extended \
  --era Run2_2018 \
  --python_filename B2G-RunIIFall18wmLHEGS-02112_1_cfg.py \
  --fileout file:B2G-RunIIFall18wmLHEGS-02112.root \
  --number 232 \
  --number_out 100 \
  --no_exec \
  --mc
```





