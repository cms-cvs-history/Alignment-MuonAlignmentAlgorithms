#ifndef Alignment_MuonAlignmentAlgorithms_MuonResidualsPositionFitter_H
#define Alignment_MuonAlignmentAlgorithms_MuonResidualsPositionFitter_H

/** \class MuonResidualsPositionFitter
 *  $Date: 2009/03/24 00:04:39 $
 *  $Revision: 1.4 $
 *  \author J. Pivarski - Texas A&M University <pivarski@physics.tamu.edu>
 */

#include "Alignment/MuonAlignmentAlgorithms/interface/MuonResidualsFitter.h"

class MuonResidualsPositionFitter: public MuonResidualsFitter {
public:
  enum {
    kPosition = 0,
    kZpos,
    kPhiz,
    kScattering,
    kSigma,
    kGamma,
    kNPar
  };

  enum {
    kResidual = 0,
    kAngleError,
    kTrackAngle,
    kTrackPosition,
    kNData
  };

  MuonResidualsPositionFitter(int residualsModel, int minHits): MuonResidualsFitter(residualsModel, minHits) {};

  int type() const { return MuonResidualsFitter::kPositionFitter; };

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

#endif // Alignment_MuonAlignmentAlgorithms_MuonResidualsPositionFitter_H
