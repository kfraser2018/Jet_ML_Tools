// Finishes processing events from lhe file
// lhe file only contains events with up quarks in main process and subprocesses

#include "Pythia8/Pythia.h"
#include "fastjet/Selector.hh"
#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"
#include "CleverStream.hh"
#include "CmdLine.hh"

using namespace Pythia8;
using namespace std;

#define OUTPRECISION 12
#define MAX_KEPT 1
#define PRINT_FREQ 100

int main(int argc, char** argv) {

  CmdLine cmdline(argc, argv);

  //Settings
  int    nEvent    = cmdline.value("-nev", 10000);
  double pthatmin  = cmdline.value("-pthatmin", 25.);
  double pthatmax  = cmdline.value("-pthatmax", -1.);
  double ptpow     = cmdline.value("-ptpow", -1.);
  bool   do_UE     = !cmdline.present("-noUE");
  bool   do_hadr   = !cmdline.present("-parton");
  bool   do_FSR    = !cmdline.present("-noFSR");
  bool   do_ISR    = !cmdline.present("-noISR");
  double Rparam    = cmdline.value("-R", 0.4);
  double etaMax    = cmdline.value("-etamax", 2.5);
  double ptjetmin  = cmdline.value("-ptjetmin", 50.);
  double ptjetmax  = cmdline.value("-ptjetmax", 10000.);
  string infile  = cmdline.value<string>("-in","-");
  string outfile  = cmdline.value<string>("-out","-");
  int    seed      = cmdline.value("-seed", 0);

  cout << infile << endl; 
  // output setup
  CleverOFStream outstream(outfile);
  outstream << "# " << cmdline.command_line() << endl;
  outstream << "# date: " << cmdline.time_stamp() << endl;

  cmdline.assert_all_options_used();

  // Generator
  Pythia pythia;

  // Random seed
  pythia.settings.flag("Random:setSeed", true);
  pythia.settings.mode("Random:seed", seed);

  // generation cuts and ptpow
  pythia.settings.parm("PhaseSpace:pTHatMin", pthatmin);
  pythia.settings.parm("PhaseSpace:pTHatMax", pthatmax);
  pythia.settings.parm("PhaseSpace:bias2SelectionPow", ptpow);
  pythia.settings.flag("PhaseSpace:bias2Selection", ptpow >= 0 ? true : false);
  
  // Multiparton Interactions, hadronisation, ISR, FSR
  pythia.settings.flag("PartonLevel:MPI", do_UE);
  pythia.settings.flag("PartonLevel:ISR", do_ISR);
  pythia.settings.flag("PartonLevel:FSR", do_FSR);
  pythia.settings.flag("HadronLevel:Hadronize", do_hadr);

  // Turn off default event listing
  pythia.readString("Next:numberShowEvent = 0");
  pythia.readString("Next:numberShowProcess = 0");
  pythia.readString("Next:numberShowInfo = 0");

  // Initialize Les Houches Event File run. List initialization information.
  pythia.readString("Beams:frameType = 4");
  pythia.readString("Beams:LHEF =" + infile);
  pythia.init();
  
  // Jet clustering setup
  fastjet::JetDefinition jet_def = fastjet::JetDefinition(fastjet::antikt_algorithm, Rparam);
  std::vector <fastjet::PseudoJet> particles;
  fastjet::Selector jet_selector = fastjet::SelectorPtMin(ptjetmin) &&
                                   fastjet::SelectorPtMax(ptjetmax) &&
                                   fastjet::SelectorAbsEtaMax(etaMax) &&
                                   fastjet::SelectorNHardest(MAX_KEPT);

  outstream << "# Jet algorithm is anti-kT with R=" << Rparam << endl;
  outstream << "# Multiparton interactions are switched "
      << ( (do_UE) ? "on" : "off" ) << endl;
  outstream << "# Hadronisation is "
      << ( (do_hadr) ? "on" : "off" ) << endl;
  outstream << "# Final-state radiation is "
      << ( (do_FSR) ? "on" : "off" ) << endl;
  outstream << "# Initial-state radiation is "
      << ( (do_ISR) ? "on" : "off" ) << endl;
  outstream << "# Random seed is " << seed << endl;
  outstream << setprecision(OUTPRECISION);

  // Begin event loop; generate until none left in input file.
  for (int iEvent = 0; iEvent < nEvent;) {

    // Generate events, and check whether generation failed.
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop.
      if (pythia.info.atEndOfFile()) {break;}

      // Otherwise continue
      else {continue;}
    }

    // Reset Fastjet input
    particles.resize(0);

    // Loop over event record to decide what to pass to FastJet
    for (int i = 0; i < pythia.event.size(); ++i) {
      //if (pythia.event[i].status() == -23) {cout << pythia.event[i].id() << endl;}

      // Final state only, no neutrinoutstream
      if (!pythia.event[i].isFinal() ||
          pythia.event[i].idAbs() == 12 ||
          pythia.event[i].idAbs() == 14 ||
          pythia.event[i].idAbs() == 16) continue;
      

      // Store as input to Fastjet
      fastjet::PseudoJet particle(pythia.event[i].px(),
                                  pythia.event[i].py(),
                                  pythia.event[i].pz(),
                                  pythia.event[i].e());
      particle.set_user_index(pythia.event[i].id());
      particles.push_back(particle);
    }

    if (particles.size() == 0) {
      cerr << "Error: event with no final state particles" << endl;
      continue;
    }

    // Run Fastjet with selection
    vector<fastjet::PseudoJet> jets = sorted_by_pt(jet_selector(jet_def(particles)));
    
    // If we've found a jet
    if (jets.size() > 0) {

      iEvent++;
      if (iEvent % PRINT_FREQ == 0) cout << "Generated " << iEvent
          << " jets so far..." << endl;

      // output particles
      vector<fastjet::PseudoJet> consts = jets[0].constituents();
      outstream << "Event " << iEvent << ", "
                << jets[0].rap() << ","
                << jets[0].phi() << ","
                << jets[0].pt()  << endl; 
 
      for (int j = 0; j < consts.size(); j++)
        outstream << consts[j].rap() << "," << consts[j].phi() << ","
                  << consts[j].pt()  << "," << consts[j].user_index() << endl;
      outstream << endl;
    }

  // End of event loop.
  }

  // Statistics
  pythia.stat();


  // Done.
  return 0;
}
