import os
import FWCore.ParameterSet.Config as cms

inputROOTs = os.environ["MuonHIP_inputROOTs"]
outputROOT = os.environ["ALIGNMENT_outputROOT"]
outputReportTXT = os.environ["ALIGNMENT_outputReportTXT"]
outputDB = os.environ["ALIGNMENT_outputDB"]

process = cms.Process("collectAlignment")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring("cout"),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR")))

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.CommonDetUnit.bareGlobalTrackingGeometry_cfi")
process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")
process.load("Geometry.RPCGeometry.rpcGeometry_cfi")
process.load("Geometry.TrackerNumberingBuilder.trackerNumberingGeometry_cfi")
process.load("Geometry.TrackerGeometryBuilder.trackerGeometry_cfi")

process.load("TrackingTools.TrackRefitter.globalCosmicMuonTrajectories_cff")
process.globalCosmicMuons.Tracks = cms.InputTag("ALCARECOMuAlGlobalCosmics:GlobalMuon")
process.Path = cms.Path(process.globalCosmicMuons)

process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
process.looper.tjTkAssociationMapTag = cms.InputTag("globalCosmicMuons:Refitted")
process.looper.doTracker = cms.untracked.bool(False)
process.looper.doMuon = cms.untracked.bool(True)
process.looper.algoConfig = cms.PSet(
    algoName = cms.string("MuonAlignmentFromReference"),
    reference = cms.string("tracker"),
    minTrackPt = cms.double(20.),
    minTrackerHits = cms.int32(10),
    maxTrackerRedChi2 = cms.double(10.),
    allowTIDTEC = cms.bool(False),
    minDTSL13Hits = cms.int32(6),
    minDTSL2Hits = cms.int32(3),
    maxDTSL13Residual = cms.double(20.),
    maxDTSL2Residual = cms.double(20.),
    collector = cms.vstring(*inputROOTs.split("\n")),
    collectorROOTDir = cms.string("ntuples"),
    fitAndAlign = cms.bool(True),
    minEntriesPerFitBin = cms.int32(30),
    fitReportName = cms.string(outputReportTXT),
    )
process.looper.ParameterBuilder.Selector = cms.PSet(alignParams = cms.vstring("MuonDTChambers,110001"))

process.looper.applyDbAlignment = cms.untracked.bool(True)
# process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_noesprefer_cff")
process.GlobalTag.globaltag = cms.string("CRAFT_ALL_V4::All")
# del process.SiStripPedestalsFakeESSource
del process.DTFakeVDriftESProducer

process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.muonAlignment = cms.ESSource("PoolDBESSource",
                                     process.CondDBSetup,
                                     connect = cms.string("sqlite_file:CRAFTalignment4_NewTracker_xyphiz.db"),
                                     toGet = cms.VPSet(cms.PSet(record = cms.string("DTAlignmentRcd"),       tag = cms.string("DTAlignmentRcd")),
                                                       cms.PSet(record = cms.string("DTAlignmentErrorRcd"),  tag = cms.string("DTAlignmentErrorRcd")),
                                                       cms.PSet(record = cms.string("CSCAlignmentRcd"),      tag = cms.string("CSCAlignmentRcd")),
                                                       cms.PSet(record = cms.string("CSCAlignmentErrorRcd"), tag = cms.string("CSCAlignmentErrorRcd"))))
process.es_prefer_muonAlignment = cms.ESPrefer("PoolDBESSource", "muonAlignment")

process.TFileService = cms.Service("TFileService", fileName = cms.string(outputROOT))

process.looper.saveToDB = cms.bool(True)
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.PoolDBOutputService = cms.Service("PoolDBOutputService",
                                          process.CondDBSetup,
                                          connect = cms.string("sqlite_file:" + outputDB),
                                          toPut = cms.VPSet(cms.PSet(record = cms.string("DTAlignmentRcd"), tag = cms.string("DTAlignmentRcd")),
                                                            cms.PSet(record = cms.string("DTAlignmentErrorRcd"), tag = cms.string("DTAlignmentErrorRcd")),
                                                            cms.PSet(record = cms.string("CSCAlignmentRcd"), tag = cms.string("CSCAlignmentRcd")),
                                                            cms.PSet(record = cms.string("CSCAlignmentErrorRcd"), tag = cms.string("CSCAlignmentErrorRcd"))))

process.SiStripLorentzAngle = cms.ESSource("PoolDBESSource",
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(2),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('SiStripLorentzAngleRcd'),
       tag = cms.string("SiStripLA_CRAFT_layers")  # 'SiStripLA_CRAFT_V2P-V3P_220_Uniform')#SiStripLA_CRAFT_layers')
    )),
    connect = cms.string('sqlite_file:LA_CRAFT_layers.db')#LA_CRAFT_UNIFORM.db')
)
process.es_prefer_SiStripLorentzAngle = cms.ESPrefer("PoolDBESSource","SiStripLorentzAngle")

import CalibTracker.Configuration.Common.PoolDBESSource_cfi
process.trackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
     connect = 'sqlite_file:HIPMPmerged.db',
     toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentRcd'),
                                tag = cms.string('Alignments')
                                )))

process.trackerAlignmentError = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
     connect = 'sqlite_file:AlignmentParameterErrors_offline_v3.db',
     toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorRcd'),
                                tag = cms.string('Tracker_GeometryErr_v3_offline')
                                )))

process.es_prefer_trackerAlignment      = cms.ESPrefer("PoolDBESSource","trackerAlignment")
process.es_prefer_trackerAlignmentError = cms.ESPrefer("PoolDBESSource","trackerAlignmentError")



