# Gen Produciton for the Run3 X->phi phi -> 4b

I'll explain how to take my data cards and create them into usable MINIAOD. We stop at MINIAOD for this scouting analysis so that the custom ScoutingNano with a custom b-tagger can be applied.

## Making cards

Luckily, this analysis has been done in RECO for Run 2, so most of the work has been done to make the card. I will explain the critical parts of the cards that need to be changed, but minor tweaks have been made and are not critical to producing Run 3 events.

### run_card.dat

Beam energy changed from 6500 to 6800 

### proc_card.dat
`[QCD] -> [Noborn = QCD]` <br>
ninja noinstall: this resolves an import error  

##
