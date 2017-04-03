#include "fastjet/PseudoJet.hh"

#ifndef __FJUI_HH__
#define __FJUI_HH__

class MyUserInfo : public fastjet::PseudoJet::UserInfoBase{
public:

  // main constructor
  MyUserInfo(const int & ivertex, const bool & charged, const int & id) :
    _charged(charged), _ivertex(ivertex), _id(id), _puppi(0) {}

  // copy contructor
  MyUserInfo(const MyUserInfo & myui) : 
    _charged(myui.isCharged()), _ivertex(myui.vertex()), _id(myui.id()), _puppi(myui.puppi()) {}

  bool isCharged() const { return _charged; }
  int vertex() const { return _ivertex; }
  int id() const { return _id; }

  double puppi() const { return _puppi; }
  void puppi(double val) { _puppi = val; }

protected:
  bool _charged;
  int _ivertex, _id;
  double _puppi;
};

#endif // __FJUI_HH__