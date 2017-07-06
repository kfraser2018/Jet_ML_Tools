# Makefile to compile Events.cc

CXX=g++
ifeq ($(shell uname), Darwin)
  CXX = clang++
endif

CXXFLAGS = -O2 -Wall -std=c++0x

BOOST     += -I/usr/local/bin/boost_1_64_0
INCLUDE   += -DHAVEBOOST
LIBRARIES += -lboost_iostreams -ldl

FASTJETINC = $(shell fastjet-config --cxxflags)
PYTHIA8INC = $(shell pythia8-config --cxxflags)

FASTJETLIB = $(shell fastjet-config --libs)
PYTHIA8LIB = $(shell pythia8-config --libs)
LIBRARIES += $(FASTJETLIB) $(PYTHIA8LIB)
INCLUDE   += $(FASTJETINC) $(PYTHIA8INC)

all: events events_lh process_events_lh

events: Events.o CmdLine.o CleverStream.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBRARIES)

events_lh: events_lh.o CmdLine.o CleverStream.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBRARIES)

process_events_lh: process_events_lh.o CmdLine.o CleverStream.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBRARIES)

Events.o: Events.cc
	$(CXX) $(INCLUDE) -o $@ $< -c $(CXXFLAGS)

CmdLine.o: CmdLine.cc CmdLine.hh
	$(CXX) $(BOOST) -o $@ $< -c $(CXXFLAGS)

CleverStream.o: CleverStream.cc CleverStream.hh
	$(CXX) $(BOOST) -o $@ $< -c $(CXXFLAGS)

events_lh.o: events_lh.cc
	$(CXX) $(INCLUDE) $(BOOST) -o $@ $< -c $(CXXFLAGS)

process_events_lh.o: process_events_lh.cc
	$(CXX) $(INCLUDE) $(BOOST) -o $@ $< -c $(CXXFLAGS)
clean :
	rm -fv events *.o
