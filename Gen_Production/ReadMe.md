# Gen Produciton for the Run3 X->phi phi -> 4b

I'll explain how to take my data cards and create them into usable MINIAOD. We stop at MINIAOD for this scouting analysis so that the custom ScoutingNano with a custom b-tagger can be applied.

## Making cards

Luckily, this analysis has been done in RECO for Run 2, so most of the work has been done to make the card. I will explain the critical parts of the cards that need to be changed, but minor tweaks have been made and are not critical to producing Run 3 events.

### run_card.dat

Beam energy changed from 6500 to 6800 

### proc_card.dat
`[QCD] -> [Noborn = QCD]` <br>
ninja noinstall: this resolves an import error  

I would suggest now to skip to the Making the Gridpack section and make a single gridpack so that there are no errors in your cards. Each card in the customizedcards.dat for this analyis will have the lines

```
set param_card mass 54 X Mass
set param_card decay 54 AUTO
set param_card mass 90000054 Phi Mass
set param_card decay 90000054 AUTO
```

Which means that for each X and Phi mass you want to make samples of you need to change, for example of a X1500 and Phi 600 events you have,

```
set param_card mass 54 1.500000e+03
set param_card decay 54 AUTO
set param_card mass 90000054 6.000000e+02
set param_card decay 90000054 AUTO
```

Now for this analysis and most other you will want to test a large array of these masses, other than spending an afternoon copy and making new cards the script of Generating_cards.py will make all your cards for you as long as you provide it with a json file. This copies over all your cards and names them correctly other than your customizedcards.dat which pulls the X and Phi mass from your json file and updates that card. Now that we have all the cards made for the analysis we can no go back into the Making the Gridpack section.

## Making the Gridpack

To set up your environment properly, please follow the [How to produce gridpacks wiki](https://cms-generators.docs.cern.ch/how-to-produce-gridpacks/mg5-amcnlo/#generating-the-gridpack) Remember for run 3 you want to be on a machine that has a el8 arcitecture. If you are not you can create a singularity using `cmssw-el8`

Then you run the command of <br>

`./gridpack_generation.sh NAME CARDDIR RUNHOME QUEUE JOBSTEP SCRAM_ARCH CMSSW_VERSION` <br>

which for the X 1000 and A 50 looks like <br>

`./gridpack_generation.sh XtoAAto4b_X1000A50 cards/examples/XtoAAto4b/` <br>

This produces the gridpack as a tarball, which leads us into the next step. 

### Side note
This process can take a long time, so you could potentially set up a condor job to automatically make all your gridpacks. Unfortunily ND Teir 3 system doesn't have a quick and easy way to do that, so if you choose that route I highly suggest using LXPLUS. 

## Making the LHE file and GEN-SIM
This next step is taking the tarball to the LHE/GEN SIM step; at the moment. For this analysis using the general Run 3 pythia cards is works. The pythia fragament controls the hadronization process. Since this analysis final state is 4 b quarks we do not want to change how these b quarks hadronize. You can find this pythia fragament [here](https://gitlab.cern.ch/cms-b2g/b-2-g-m-csample-requests/-/blob/master/genFragments/Hadronizer/13p6TeV/Hadronizer_TuneCP5_13p6TeV_generic_TauFix_LHE_pythia8_cff.py?ref_type=heads) Also, this part needs to be done in the correct CMSSW environment for the correct year. In this example, we are talking about 2024 MC samples. If testing for another year, please look up the recommended CMSSW version. Luckily everything else is has been done many times before and is integrated into CMSSW. So we can use the cmsDriver command below to make the configuration file that we need. Once again this is year specific, to find the correct configuraiton that you need I suggest going to the [MCM Website](https://cms-pdmv-prod.web.cern.ch/mcm/).


```
cmsDriver.py Configuration/GenProduction/python/Hadronizer_TuneCP5_13p6TeV_generic_TauFix_LHE_pythia8_cff.py --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot DBrealistic --step LHE,GEN,SIM --geometry DB:Extended --conditions 140X_mcRun3_2024_realistic_v26 --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --datatier GEN-SIM,LHE --eventcontent RAWSIM,LHE --python_filename GEN-RunIII2024Summer24wmLHEGS-00001_1_cfg.py --fileout file:GEN-RunIII2024Summer24wmLHEGS-00001.root --number 100 --number_out 100 --no_exec --mc

```
This will create the GEN SIM root file which now needs to go through, the trigger selection, and then made into AOD->MiniAod->NanoAod




