# Deep Learning in Particle Physics
###### Patrick T. Komiske and Eric M. Metodiev

This is a collection of code that grew out of [1612.01551](https://arxiv.org/abs/1612.01551) and related projects. It contains Python code for processing events, computing values of observables, creating jet images from an event record, and training neural networks. It also contains Pythia event generation code.

### Helpful Resources
##### Deep Learning

There are many introductions and free online tutorials on machine learning and deep learning. There is not a very high barrier to understanding the various algorithms and architectures. We will highlight some useful resources that are particularly helpful.

* Michael Nielsen's [online textbook](http://neuralnetworksanddeeplearning.com/chap1.html) gives a no-nonsense introduction starting from the basic definition of a neuron and neural network through convolutional net architectures much like the one used in the deep learning with jet images study.

* I. Goodfellow, Y. Bengion, and A. Courville's [deep learning textbook](http://www.deeplearningbook.org/) has its chapters available online through their website. This book provides a more in-depth treatment of many aspects of deep learning and the mathematical preprequisites.

##### High Energy Physics

To learn about quantum field theory and the standard model, read:

[Quantum Field Theory and the Standard Model](http://www.schwartzqft.com/index.html)


##### Keras

[Keras](keras.io) is a deep learning library for Python, which wraps other powerful neural network libraries (Theano and Tensorflow) to provide a way to quickly define neural networks based on the high-level architecture.

As you'll see, Keras lets you quickly implement and train the architecture you want. You can essentially add layers to your neural network in Keras with lines like `model.add(Dense(50))`.

##### Pythia

Pythia was the high priestess in the Temple of Apollo at Dephi, more commonly known as the Oracle of Delphi. 

[Pythia](http://home.thep.lu.se/~torbjorn/Pythia.html) is also a C++ event generator that outputs realistic LHC event records for the process you want. It seems like an apt name for a black box program that magically outputs events. When you're getting started, you'll probably use event files others generate and give to you (a second-order black-box), but it's an important skill to have and not that hard to get started.


### Getting Started
#### Setting up Keras

1. Install [Python 3.5](https://www.python.org/downloads/release/python-353/).

2. Python3.5 should come with pip3.5. You can also download it online. At the terminal, execute the following:
```
pip3.5 install -U keras
pip3.5 install -U h5py
pip3.5 install -U matplotlib
pip3.5 install -U jupyter
```

3. Start an interactive python session in the terminal by executing `python3.5`. Try importing keras, `import keras`. This should fail with a message like:
```
Error, no module named tensorflow installed.
```
That’s expected. We have to tell Keras to use Theano as its deep learning backend instead. At the terminal, execute:
```
cd ~/.keras/
nano keras.json
```
This should open a basic text editor with the Keras settings. Change the "backend" field to "theano" and change "image_dim_ordering" to "th". Then use `ctrl + X` to quit and save changes.

4. Start another interactive python session with `python3.5` and again try importing keras with `import keras`. If everything is installed properly, it should import without errors this time.

#### Setting up Pythia

Coming soon!

#### Heppy

Coming soon!

### Example


Python code should be run from the `python/` directory using python 3 (version 3.5 has been the most extensively tested). There are two examples which can be invoked as
```bash
python3 jet_image_conv_example.py
```
and
```bash
python3 image_generation_example.py
```

The `src/` directory contains event generation code. Take a look at the beginning of `Events.cc` for options. Requires Pythia8 and FastJet to be installed and pythis8-config and fastjet-config to be available in the `PATH` (for the makefile to work as is). A standard invocation after compiling would look like
```bash
 ./events -out gluon-event-seed1.txt -pthatmin 160 -ptjetmin 200 -Zg -seed 1
```
