import os

execfile("splitCRAFTfiles.py")
stepSize = 36

submitlist = []
jobnames = []

inputBegin = 0
inputEnd = stepSize + 1
for job in range(100):
  outputROOT = "fillAlignment%03d.root" % job

  file("fillAlignment%03d.sh" % job, "w").write("""#!/bin/sh

export WORKINGDIR=`pwd`
cd /afs/cern.ch/user/p/pivarski/ALCA_MUONALIGN/SWAlignment/CRAFTchambers/CMSSW_2_2_3/src
eval `scramv1 run -sh`
export STAGE_SVCCLASS=cmscaf

export ALIGNMENT_inputBegin=%s
export ALIGNMENT_inputEnd=%s
export ALIGNMENT_outputROOT=%s

cp fillAlignment.py splitCRAFTfiles.py HIPMPmerged.db AlignmentParameterErrors_offline_v3.db LA_CRAFT_layers.db CRAFTalignment4_NewTracker_xyphiz.db $WORKINGDIR/
cd $WORKINGDIR/
cmsRun fillAlignment.py  &&  rfcp %s /castor/cern.ch/cms/store/cmscaf/alca/alignment/MuonCosmics/CRAFTalignment4_NewTracker_xyphiz2/
ls -l
pwd
uname -a

""" % (inputBegin, inputEnd, outputROOT, outputROOT))
  os.system("chmod +x fillAlignment%03d.sh" % job)

  submitlist.append("bsub -q cmsexpress -G ALCA_EXPRESS -J \"fillAlignment%03d\" fillAlignment%03d.sh" % (job, job))
  jobnames.append("ended(fillAlignment%03d)" % job)

  inputBegin += stepSize
  inputEnd += stepSize

file("collectAlignment.sh", "w").write("""#!/bin/sh

export WORKINGDIR=`pwd`
cd /afs/cern.ch/user/p/pivarski/ALCA_MUONALIGN/SWAlignment/CRAFTchambers/CMSSW_2_2_3/src
eval `scramv1 run -sh`
export STAGE_SVCCLASS=cmscaf

cp collectAlignment.py splitCRAFTfiles.py HIPMPmerged.db AlignmentParameterErrors_offline_v3.db LA_CRAFT_layers.db CRAFTalignment4_NewTracker_xyphiz.db $WORKINGDIR/
cd $WORKINGDIR/

for i in 0 1 2 3 4 5 6 7 8 9; do for j in 0 1 2 3 4 5 6 7 8 9; do rfcp /castor/cern.ch/cms/store/cmscaf/alca/alignment/MuonCosmics/CRAFTalignment4_NewTracker_xyphiz2/fillAlignment0$i$j.root .; done; done

export MuonHIP_inputROOTs=`ls fillAlignment*.root`
export ALIGNMENT_outputROOT=collected.root
export ALIGNMENT_outputReportTXT=alignment_report.txt
export ALIGNMENT_outputDB=alignment.db

cmsRun collectAlignment.py
rfcp collected.root /castor/cern.ch/cms/store/cmscaf/alca/alignment/MuonCosmics/CRAFTalignment4_NewTracker_xyphiz2/
rfcp alignment_report.txt /castor/cern.ch/cms/store/cmscaf/alca/alignment/MuonCosmics/CRAFTalignment4_NewTracker_xyphiz2/
rfcp alignment.db /castor/cern.ch/cms/store/cmscaf/alca/alignment/MuonCosmics/CRAFTalignment4_NewTracker_xyphiz2/
ls -l
pwd
uname -a

""")
os.system("chmod +x collectAlignment.sh")
submitlist.append("bsub -q cmsexpress -G ALCA_EXPRESS -J \"collectAlignment\" -w \"%s\" collectAlignment.sh\n" % "  &&  ".join(jobnames))

bsubstitute = file("bsubstitute.sh", "w")
bsubstitute.write("\n".join(submitlist))
bsubstitute.close()
os.system("chmod +x bsubstitute.sh")
