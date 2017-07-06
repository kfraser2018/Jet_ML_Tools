#EVENT GENERATION INFORMATION
#####Katherine Fraser

Events were generated using pythia 8.2 in two steps. First .lhe files were generated using generate_lhe_files.sh, which selects the output of the hardest subprocess of a qg2Zgmq event to be a specific type of quark or antiquark. Then run process_events_lh on these .lhe files. process_events_lh takes an input of the form

'''
./process_events_lh -out ../events/100GEV-upantiquark-event-seed1.txt -in lhe_files/upantiquark-seed -ptjetmin 100 -ptjetmax 120 -seed 1
'''

