#EVENT GENERATION INFORMATION
#####Katherine Fraser

Events were generated using pythia 8.2 in two steps. First .lhe files were generated using generate_lhe_files.sh, which selects the output of the hardest subprocess of a qg2Zgmq event to be a specific type of quark. Then run process_events_lh on these .lhe files. process_events_lh takes an input of the form

'''
./process_events_lh -out ../events/100GEV-upantiquark-event-seed1.txt -in lhe_files/upantiquark-seed -ptjetmin 100 -ptjetmax 120 -seed 1
'''

The in flag is followed by the .lhe file names, up to the seed number (The full name of the files is of the form upantiquark-seed1.lhe, for example). The program automatically reads in 10 .lhe files numbered seed_number*10+1 through seed_number*10+11. 
