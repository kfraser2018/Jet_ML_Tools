#include <fstream>
#include <iostream>
#include <string>

#include "Pythia8/Pythia.h"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/Selector.hh"
#include "fastjet/contrib/SoftKiller.hh"

#include "CmdLine.hh"
#include "PUPPI.hh"
#include "FJUI.hh"

#define LV_JET_MIN_PT     150
#define MIN_QUARK_PT      95
#define RAP_MAX           2.5
#define DEFAULT_JET_R     0.4
#define MWIDTH            1.0
#define REF_JET_R         0.4

#define SK_GRID_SIZE      0.4
#define SK_RAP_MAX        5.0

#define PRINT_FREQ        500
#define SMUSH             1.e-60
#define OUTPRECISION      12
#define NEVENT            10000
#define DEFAULT_SEED      -1
#define DEFAULT_NPU       150

using namespace std;
using namespace fastjet;

int main(int argc, char** argv) {
  
  CmdLine cmdline(argc, argv);
  
  // Settings
  int     nEvent      =   cmdline.value("-nev", NEVENT);
  int     seed        =   cmdline.value("-seed", DEFAULT_SEED);
  double  jet_R       =   cmdline.value("-R", DEFAULT_JET_R);
  int     NPU         =   cmdline.value("-npu", DEFAULT_NPU);
  double  rap_max     =   cmdline.value("-rap-max", RAP_MAX);
  double  lv_min_pt   =   cmdline.value("-lv-min-pt", LV_JET_MIN_PT);
  double  min_q_pt    =   cmdline.value("-min-q-pt", MIN_QUARK_PT);
  bool    do_UE       =   !cmdline.present("-no-ue");
  bool    do_SK       =   !cmdline.present("-no-sk");
  bool    do_PUPPI    =   !cmdline.present("-no-puppi");
  string  filename    =   cmdline.value<string>("-out", "test.txt");

  // output setup
  ofstream outstream(filename.c_str());
  outstream << "# " << cmdline.command_line() << endl;
  outstream << "# date: " << cmdline.time_stamp() << endl;
   
  cmdline.assert_all_options_used();
  
  // PYTHIA SETUP
  Pythia8::Pythia pythia_LV;
  Pythia8::Pythia pythia_PU;

  // Specify processes
  pythia_LV.readString("HiggsSM:ffbar2H = on");
  pythia_LV.readString("25:m0=500");
  pythia_LV.readString("25:onMode = off");
  pythia_LV.readString("25:onIfAny = 1 2");
  pythia_LV.readString("25:doForceWidth = on");
  pythia_LV.readString("25:mWidth = " + to_string(MWIDTH));
  pythia_LV.settings.flag("PartonLevel:MPI", do_UE);

  pythia_PU.readString("SoftQCD:nonDiffractive = on");
  pythia_PU.readString("HardQCD:all = off");
  pythia_PU.readString("PhaseSpace:pTHatMin = .1");
  pythia_PU.readString("PhaseSpace:pTHatMax = 20000");

  // Beams
  pythia_LV.readString("Beams:idA = 2212");
  pythia_LV.readString("Beams:idB = 2212");
  pythia_LV.readString("Beams:eCM = 13000");

  pythia_PU.readString("Beams:idA = 2212");
  pythia_PU.readString("Beams:idB = 2212");
  pythia_PU.readString("Beams:eCM = 13000");
  
  // Random seed
  pythia_LV.readString("Random:setSeed = on");
  pythia_LV.readString("Random:seed = " + to_string(seed));

  pythia_PU.readString("Random:setSeed = on");
  pythia_PU.readString("Random:seed = " + to_string(seed));

  // event listing
  pythia_LV.readString("Next:numberShowEvent = 0");
  pythia_LV.readString("Next:numberShowProcess = 0");
  pythia_LV.readString("Next:numberShowInfo = 0");

  pythia_PU.readString("Next:numberShowEvent = 0");
  pythia_PU.readString("Next:numberShowProcess = 0");
  pythia_PU.readString("Next:numberShowInfo = 0");

  pythia_LV.init();
  pythia_PU.init();

  // PUPPI setup
  PUPPI puppi(NPU);

  // EVENT LOOP
  for (int iEvent = 0; iEvent < nEvent;) {

    // JET SETUP
    vector<PseudoJet> LV_particles, tot_particles, LV_jets, tot_jets;
    JetDefinition jet_def = JetDefinition(antikt_algorithm, jet_R);
    JetDefinition ref_jet_def = JetDefinition(antikt_algorithm, REF_JET_R);
    // may want to commute
    Selector LV_selector = SelectorAbsRapMax(rap_max) * SelectorNHardest(2);

    // LV particle loop
    if (!pythia_LV.next()) continue;
    int id = 0;
    double quark_pT = 1000000000000;
    for (int i = 0; i < pythia_LV.event.size(); i++, id++) {

      if (pythia_LV.event[i].idAbs() == 25) {
        vector<int> daugthers = pythia_LV.event.daughterList(i);
        for (int j = 0; j < daugthers.size(); j++) {
          if (pythia_LV.event[daugthers[j]].id() == 25) continue;
          if (pythia_LV.event[daugthers[j]].pT() < quark_pT) quark_pT = pythia_LV.event[daugthers[j]].pT();
        }
      }

      if (!pythia_LV.event[i].isFinal()     || pythia_LV.event[i].idAbs() == 12 ||
           pythia_LV.event[i].idAbs() == 13 || pythia_LV.event[i].idAbs() == 14 ||
           pythia_LV.event[i].idAbs() == 16) continue;

      bool ich = pythia_LV.event[i].isCharged();
      PseudoJet p(pythia_LV.event[i].px(), 
                           pythia_LV.event[i].py(), 
                           pythia_LV.event[i].pz(), 
                           pythia_LV.event[i].e());
      p.reset_PtYPhiM(p.pt(), p.rap(), p.phi(), 0);
      p.set_user_info(new MyUserInfo(-1, ich, id));
      tot_particles.push_back(p);
      LV_particles.push_back(p);
    }

    if (quark_pT < min_q_pt) continue;

    ClusterSequence LV_clsq(LV_particles, ref_jet_def);
    LV_jets = sorted_by_pt(LV_selector(LV_clsq.inclusive_jets(lv_min_pt)));
    if (LV_jets.size() < 2) continue;
    
    // PU particle loop
    for (int iPU = 0; iPU < NPU; iPU++) {
      if (!pythia_PU.next()) continue;
      for (int i = 0; i < pythia_PU.event.size(); i++, id++) {
        if (!pythia_PU.event[i].isFinal()     || pythia_PU.event[i].idAbs() == 12 ||
             pythia_PU.event[i].idAbs() == 13 || pythia_PU.event[i].idAbs() == 14 ||
             pythia_PU.event[i].idAbs() == 16) continue;
        bool ich = pythia_PU.event[i].isCharged();
        PseudoJet p(pythia_PU.event[i].px(), 
                             pythia_PU.event[i].py(), 
                             pythia_PU.event[i].pz(), 
                             pythia_PU.event[i].e());
        if (ich) p *= SMUSH;
        p.reset_PtYPhiM(p.pt(), p.rap(), p.phi(), 0);
        p.set_user_info(new MyUserInfo(iPU, ich, id));
        tot_particles.push_back(p);
      }
    }

    // calculate puppi information
    if (do_PUPPI) puppi.compute_median_left_RMS(tot_particles);

    // calculate SK pt threshold
    double SK_pt_threshold;
    if (do_SK) {
      contrib::SoftKiller soft_killer(SK_RAP_MAX, SK_GRID_SIZE);
      vector<PseudoJet> SK_event;
      soft_killer.apply(tot_particles, SK_event, SK_pt_threshold);
    }
    
    ClusterSequence tot_clsq(tot_particles, jet_def);
    tot_jets = sorted_by_pt(tot_clsq.inclusive_jets(lv_min_pt));
    if (tot_jets.size() < 2) continue;

    // match two tot_jets closest to LV_jets based on shared pT
    int jindices[2];
    for (int i = 0; i < 2; i++) {
      int index_max = -1; 
      double shared_max = 0;
      for (int j = 0; j < tot_jets.size(); j++) {
        double shared = 0;
        vector<PseudoJet> LV_consts = LV_jets[i].constituents();
        vector<PseudoJet> tot_consts = tot_jets[j].constituents();
        for (int k = 0; k < LV_consts.size(); k++) {
          for (int l = 0; l < tot_consts.size(); l++) {
            if (LV_consts[k].user_info<MyUserInfo>().id() == tot_consts[l].user_info<MyUserInfo>().id()) 
              shared += LV_consts[k].pt();
          }
        }
        if (shared > shared_max) { shared_max = shared; index_max = j; }
      }
      jindices[i] = index_max;
    }

    // if we've failed to match, continue
    if (jindices[0] == -1 || jindices [1] == -1) continue;

    // rescale charged PU particles
    for (int i = 0; i < 2; i++) {
      vector<PseudoJet> consts = tot_jets[jindices[i]].constituents();
      for (int j = 0; j < consts.size(); j++) {
        PseudoJet & pj_j = consts[j];
        if (pj_j.user_info<MyUserInfo>().vertex() != -1 && 
            pj_j.user_info<MyUserInfo>().isCharged())
          pj_j /= SMUSH;
      }
    }

    // output each jet to file
    for (int i = 0; i < 2; i++) {

      vector<PseudoJet> consts = tot_jets[jindices[i]].constituents();

      // output jet-level info
      outstream << setprecision(OUTPRECISION) << jindices[i] << " " << NPU 
                << " -1 -1 " << tot_jets[jindices[i]].pt() << " " 
                << tot_jets[jindices[i]].eta() << " " << tot_jets[jindices[i]].phi() 
                << " " << tot_jets[jindices[i]].m() << " ";

      // output particle information
      for (int j = 0; j < consts.size(); j++) {
        PseudoJet & pj_j = consts[j];

        // get PUPPI weight for this particle
        if (do_PUPPI) puppi.compute_weight(consts[j]);

        // get SK result for this particle
        string s_sk;
        if (do_SK) s_sk = pj_j.pt() >= SK_pt_threshold ? "1" : "0";

        // output particle information to file
        outstream << setprecision(OUTPRECISION) << pj_j.pt() << " " 
                  << pj_j.eta() << " " << pj_j.phi() << " " 
                  << pj_j.user_info<MyUserInfo>().isCharged() << " " 
                  << pj_j.user_info<MyUserInfo>().vertex() << " " 
                  << pj_j.user_info<MyUserInfo>().puppi() << " "
                  << s_sk << " ";
      }
      outstream << endl;
    }
    iEvent++;
    if (iEvent % PRINT_FREQ == 0) cout << "Generated " << iEvent 
                                       << " events so far..." << endl;
  } // end event loop

  // Statistics
  pythia_LV.stat();
  pythia_PU.stat();

  return 0;
}
