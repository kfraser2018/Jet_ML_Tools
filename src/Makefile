CXX = g++
ifeq ($(shell uname), Darwin)
  CXX = clang++
endif

CXXFLAGS = -O3 -Wall -std=c++11

FASTJETINC = $(shell fastjet-config --cxxflags)
PYTHIA8INC = $(shell pythia8-config --cxxflags)
ROOTINC    = $(shell root-config --cflags)

FASTJETLIB = $(shell fastjet-config --libs) -lSoftKiller
PYTHIA8LIB = $(shell pythia8-config --libs)
ROOTLIB    = $(shell root-config --libs)
LIBRARIES += $(FASTJETLIB) $(PYTHIA8LIB) $(ROOTLIB)

all: 
	make dijets

dijets: dijets.o CmdLine.o PUPPI.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBRARIES)

dijets.o: dijets.cc FJUI.hh PUPPI.hh
	$(CXX) $(FASTJETINC) $(PYTHIA8INC) $(ROOTINC) -o $@ $< -c $(CXXFLAGS)

PUPPI.o: PUPPI.cc PUPPI.hh FJUI.hh
	$(CXX) $(ROOTINC) $(FASTJETINC) -o $@ $< -c $(CXXFLAGS)

CmdLine.o: CmdLine.cc CmdLine.hh
	$(CXX) -o $@ $< -c $(CXXFLAGS)

clean :
	rm -fv dijets *.o
