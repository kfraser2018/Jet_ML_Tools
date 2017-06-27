#Katie Fraser, Harvard, 2017
#
#Plots ROC curves on the same graph

import heppy
import plot_config
hps = plot_config.hps
file1= 'Test_Parameters_0_100GEV_upquark_downquark_K=02_do=01_03_03_03_ROC_data.pickle'
file2 = 'jet_charge_100GEV_upquark_downquark_K=0.4_ROC_data.pickle'
file1_label = 'new parameters NN' 
file2_label = 'old_best'
qe, ge = heppy.load_ROC(file1)
qe2, ge2 = heppy.load_ROC(file2)

heppy.plot_ROC_2var(qe,ge,qe2,ge2,title = '100 GEV', label1= file1_label, label2 = file2_label, particle1_name = hps['particle1_type'], particle2_name = hps['particle2_type'])
heppy.plot_SI_2var(qe,ge,qe2,ge2,title = '100 GEV', label1= file1_label, label2 = file2_label, particle2_name = hps['particle2_type'])

