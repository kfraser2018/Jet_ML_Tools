#Katie Fraser, Harvard, 2017
#
#Plots ROC curves on the same graph

import heppy
import plot_config
hps = plot_config.hps

# Choose Files
files = []
files.append('jet_charge_100GEV_upquark_downquark_K=0.1_ROC_data.pickle')
files.append('jet_charge_100GEV_upquark_downquark_K=0.2_ROC_data.pickle')
files.append('jet_charge_100GEV_upquark_downquark_K=0.3_ROC_data.pickle')
files.append('jet_charge_100GEV_upquark_downquark_K=0.4_ROC_data.pickle')
files.append('jet_charge_100GEV_upquark_downquark_K=0.5_ROC_data.pickle')
files.append('jet_charge_100GEV_upquark_downquark_K=0.6_ROC_data.pickle')

# Make labels
labels = []
labels.append('Jet Charge Kappa=0.1')
labels.append('Jet Charge Kappa=0.2')
labels.append('Jet Charge Kappa=0.3')
labels.append('Jet Charge Kappa=0.4')
labels.append('Jet Charge Kappa=0.5')
labels.append('Jet Charge Kappa=0.6')

qes = []
ges = []
for file in files:
    qe, ge = heppy.load_ROC(file)
    qes.append(qe)
    ges.append(ge)

colors = ['r', 'b', 'y', 'k', 'm', 'c']

heppy.plot_ROC_Nvar(qes,ges,title = '100 GEV', labels = labels, particle1_name = hps['particle1_type'], particle2_name = hps['particle2_type'], colors = colors)
heppy.plot_SI_Nvar(qes,ges,title = '100 GEV', labels = labels, particle2_name = hps['particle2_type'], colors = colors)

