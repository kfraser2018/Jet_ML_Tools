#Image Generation and NN training Info
#Katherine Fraser, Harvard, 2017

All of the files below import parameters from config.py

This folder contains the code to both generate jet images and to train a NN using these images. To generate images without using jet charge, use image_generator.py. To include jet charge, use charged_image_generator.py. For image_generator.py, nb_channels can be set to 1,2, or 3, but it must be set to 2 for charged_image_generator.py. 

Once jet images are generated, run train_network.py to train the network itself. All parameters for the network that can be modified are set in the hps array at the top of the file. Note that nb_channels must match the number of channels in the original file. For images without jet charge, 'kappa' should be set to 'nocharge'.

To use jet charge without images, run jet_charge_ROC.py. To run this script, you will need

pip install -U scikit-learn

if you haven't already. 

This folder also contains some examples directly from the master branch (image_generation_example.py, jet_image_conv_example.py). Note there have also been a few modifications to the files in the heppy subfolder. 
