// main20.cc is a part of the PYTHIA event generator.
// Copyright (C) 2017 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// This is a simple test program. It shows how PYTHIA 8 can write
// a Les Houches Event File based on its process-level events.

#include "Pythia8/Pythia.h"
#include "CleverStream.hh"
#include "CmdLine.hh"

using namespace Pythia8;
using namespace std;

#define OUTPRECISION 12
#define MAX_KEPT 1
#define PRINT_FREQ 100

int main(int argc, char** argv) {

  CmdLine cmdline(argc, argv);

  // Settings
  int    nEvent    = cmdline.value("-nev", 200000);
  bool   qcd       = cmdline.present("-allqcd");
  bool   Zg        = cmdline.present("-Zg");
  bool   Zq        = cmdline.present("-Zq");
  bool   qqqq      = cmdline.present("-qqqq");
  bool   ggqb      = cmdline.present("-ggqb");
  bool   gggg      = cmdline.present("-gggg");
  bool   qbgg      = cmdline.present("-qbgg");
  bool   upantiqk    = cmdline.present("-upantiquark");
  bool   upqk        = cmdline.present("-upquark");
  bool   dnantiqk    = cmdline.present("-downantiquark");
  bool   dnqk        = cmdline.present("-downquark");
  string lhefile  = cmdline.value<string>("-out","-");
  int    seed      = cmdline.value("-seed", 0);

  cmdline.assert_all_options_used();

  // Generator.
  Pythia pythia;

  // Specify processes
  assert(qcd || Zg || Zq || qqqq || ggqb || qbgg || gggg);
  pythia.settings.flag("HardQCD:all", qcd);
  pythia.settings.flag("WeakBosonAndParton:qqbar2gmZg", Zg);
  pythia.settings.flag("WeakBosonAndParton:qg2gmZq", Zq);
  pythia.settings.flag("HardQCD:qq2qq", qqqq);
  pythia.settings.flag("HardQCD:gg2qqbar", ggqb);
  pythia.settings.flag("HardQCD:qqbar2gg", qbgg);
  pythia.settings.flag("HardQCD:gg2gg", gggg);

  // Z decay settings
  pythia.readString("WeakZ0:gmZmode = 2");
  pythia.readString("23:onMode = off");
  pythia.readString("23:onIfAny = 12 14 16");

  // Random seed
  pythia.settings.flag("Random:setSeed", true);
  pythia.settings.mode("Random:seed", seed);

  // Switch off generation of steps subsequent to the process level one.
  // (These will not be stored anyway, so only steal time.)
  pythia.readString("PartonLevel:all = off");

  // Create an LHAup object that can access relevant information in pythia.
  LHAupFromPYTHIA8 myLHA(&pythia.process, &pythia.info);

  // Open a file on which LHEF events should be stored, and write header.
  myLHA.openLHEF(lhefile);

  // Initialisation
  pythia.readString("Beams:idA = 2212");
  pythia.readString("Beams:idB = 2212");
  pythia.readString("Beams:eCM = 13000.");

  pythia.init();

  // Store initialization info in the LHAup object.
  myLHA.setInit();

  // Write out this initialization info on the file.
  myLHA.initLHEF();

  // Loop over events.
  for (int iEvent = 0; iEvent < nEvent;) {
  bool correct_quark_flavor = true;
  if (!pythia.next()) continue;

    for (int i = 0; i < pythia.process.size(); ++i) {
      // Select quark or antiquark flavor
      if (pythia.process[i].status() == 23){
          if (pythia.process[i].idAbs()==3 || pythia.process[i].idAbs()==4 || 
              pythia.process[i].idAbs() == 5){
              correct_quark_flavor = 0;
              break;}
          else if (upqk == 1){
              if (pythia.process[i].id() == -2 || pythia.process[i].idAbs() == 1){
              correct_quark_flavor = 0;
              break;}}
          else if (upantiqk == 1){
              if (pythia.process[i].id() == 2 || pythia.process[i].idAbs() == 1){
              correct_quark_flavor = 0;
              break;}}
          else if (dnqk == 1){
              if (pythia.process[i].id() == -1 || pythia.process[i].idAbs() == 2){
              correct_quark_flavor = 0;
              break;}}
          else if (dnantiqk == 1){
              if (pythia.process[i].id() == 1 || pythia.process[i].idAbs() == 2){
              correct_quark_flavor = 0;
              break;}}
        }}
    if (correct_quark_flavor == 0) {continue;}
    
    //Uncomment to see events being written 
//    for (int i = 0; i < pythia.process.size(); ++i) {
//       cout << i << ' ' << pythia.process[i].status() << ' ' << pythia.process[i].id() << endl;
//    }

    // Store event info in the LHAup object.
    myLHA.setEvent();

    // Write out this event info on the file.
    // With optional argument (verbose =) false the file is smaller.
    myLHA.eventLHEF();
    
    iEvent++;
  }

  // Statistics: full printout.
  pythia.stat();

  // Update the cross section info based on Monte Carlo integration during run.
  myLHA.updateSigma();

  // Write endtag. Overwrite initialization info with new cross sections.
  myLHA.closeLHEF(true);

  // Done.
  return 0;
}
