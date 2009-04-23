#ifndef Alignment_MuonAlignmentAlgorithms_MuonResidualsAngleFitter_H
#define Alignment_MuonAlignmentAlgorithms_MuonResidualsAngleFitter_H

/** \class MuonResidualsAngleFitter
 *  $Date: 2009/03/24 00:04:31 $
 *  $Revision: 1.4 $
 *  \author J. Pivarski - Texas A&M University <pivarski@physics.tamu.edu>
 */

#include "Alignment/MuonAlignmentAlgorithms/interface/MuonResidualsFitter.h"

class MuonResidualsAngleFitter: public MuonResidualsFitter {
public:
  enum {
    kAngle = 0,
    kXControl,
    kYControl,
    kSigma,
    kGamma,
    kNPar
  };

  enum {
    kResidual = 0,
    kXAngle,
    kYAngle,
    kNData
  };

  MuonResidualsAngleFitter(int residualsModel, int minHitsPerRegion): MuonResidualsFitter(residualsModel, minHitsPerRegion) {};

  int type() const { return MuonResidualsFitter::kAngleFitter; };

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

#endif // Alignment_MuonAlignmentAlgorithms_MuonResidualsAngleFitter_H
