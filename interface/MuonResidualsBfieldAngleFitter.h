#ifndef Alignment_MuonAlignmentAlgorithms_MuonResidualsBfieldAngleFitter_H
#define Alignment_MuonAlignmentAlgorithms_MuonResidualsBfieldAngleFitter_H

/** \class MuonResidualsBfieldAngleFitter
 *  $Date: 2009/03/24 00:04:31 $
 *  $Revision: 1.4 $
 *  \author J. Pivarski - Texas A&M University <pivarski@physics.tamu.edu>
 */

#include "Alignment/MuonAlignmentAlgorithms/interface/MuonResidualsFitter.h"

class MuonResidualsBfieldAngleFitter: public MuonResidualsFitter {
public:
  enum {
    kAngle = 0,
    kBfrompt,
    kBfrompz,
    kdEdx,
    kSigma,
    kGamma,
    kNPar
  };

  enum {
    kResidual = 0,
    kQoverPt,
    kQoverPz,
    kNData
  };

  MuonResidualsBfieldAngleFitter(int residualsModel, int minHitsPerRegion): MuonResidualsFitter(residualsModel, minHitsPerRegion) {};

  int type() const { return MuonResidualsFitter::kAngleBfieldFitter; };

  int npar() {
    if (residualsModel() == kPureGaussian) return kNPar - 1;
    else if (residualsModel() == kPowerLawTails) return kNPar;
    else if (residualsModel() == kROOTVoigt) return kNPar;
    else assert(false);
  };
  int ndata() { return kNData; };

  bool fit(Alignable *ali);
  double sumofweights() { return numResiduals(); };
  double plot(std::string name, TFileDirectory *dir, Alignable *ali);

protected:
  void inform(TMinuit *tMinuit);
};

#endif // Alignment_MuonAlignmentAlgorithms_MuonResidualsBfieldAngleFitter_H