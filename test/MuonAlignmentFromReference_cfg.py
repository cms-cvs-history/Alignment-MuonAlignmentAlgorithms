import FWCore.ParameterSet.Config as cms

process = cms.Process("ALIGN")

### 
### GlobalTag for default conditions
### 
# process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# process.GlobalTag.globaltag = cms.string("CRAFT_ALL_V9::All")

process.load("Configuration.StandardSequences.FakeConditions_cff")
process.inertGlobalPositionRcd = cms.ESSource("PoolDBESSource",
                                              process.CondDBSetup,
                                              connect = cms.string("sqlite_file:inertGlobalPositionRcd.db"),
                                              toGet = cms.VPSet(cms.PSet(record = cms.string("GlobalPositionRcd"), tag = cms.string("inertGlobalPositionRcd"))))
process.es_prefer_inertGlobalPositionRcd = cms.ESPrefer("PoolDBESSource", "inertGlobalPositionRcd")

### 
### Optionally silence the MessageLogger
### 
# process.MessageLogger = cms.Service("MessageLogger",
#                                     destinations = cms.untracked.vstring("cout"),
#                                     cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR")))

### 
### Load MuonAlignmentFromReference with default options
### 
process.load("Alignment.MuonAlignmentAlgorithms.MuonAlignmentFromReference_cff")
import Alignment.MuonAlignmentAlgorithms.Reference_intrackfit_cff as chambers

### Include selected muon chambers in the 
# process.MuonAlignmentFromReference.intrackfit = cms.vstring(*(chambers.barrel + chambers.me11all + ["ME+2/1 10", "ME+2/1 11"]))

### Store partial output for job collection
# process.writeTemporaryFile = cms.string("job053.tmp")
# process.doAlignment = False

### Collect and read back previously-generated .tmp files
# process.readTemporaryFiles = cms.vstring("job001.tmp", "job002.tmp", "job003.tmp", )

### Report file (formatted as Python for parsing and searching fit results)
# process.reportFileName = "descriptive_name.py"

### ROOT file with diagnostic histograms
# MuonAlignmentFromReferenceTFileService.fileName = "descriptive_name.root"

### Input database/tag names
process.MuonAlignmentFromReferenceInputDB.connect = cms.string("sqlite_file:trial_xshift.db")
process.MuonAlignmentFromReferenceInputDB.toGet[0].tag = "DTAlignmentRcd"
process.MuonAlignmentFromReferenceInputDB.toGet[1].tag = "DTAlignmentErrorRcd"
process.MuonAlignmentFromReferenceInputDB.toGet[2].tag = "CSCAlignmentRcd"
process.MuonAlignmentFromReferenceInputDB.toGet[3].tag = "CSCAlignmentErrorRcd"

### Output database/tag names
process.PoolDBOutputService.connect = "sqlite_file:output.db"
process.PoolDBOutputService.toPut[0].tag = "DTAlignmentRcd"
process.PoolDBOutputService.toPut[1].tag = "DTAlignmentErrorRcd"
process.PoolDBOutputService.toPut[2].tag = "CSCAlignmentRcd"
process.PoolDBOutputService.toPut[3].tag = "CSCAlignmentErrorRcd"

### 
### Extensive diagnistics plotting (muon system map)
### 
process.load("Alignment.CommonAlignmentMonitor.AlignmentMonitorMuonSystemMap_cfi")
process.looper.monitorConfig = process.AlignmentMonitorMuonSystemMap

### 
### Choose your events source (EmptySource for reading previously-generated .tmp file)
### 
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
    "file:///NOBACKUP/MC/InclusiveMuPt50_TrackerDigis/MuAlCalIsolatedMu000_testing50.root",
    "file:///NOBACKUP/MC/InclusiveMuPt50_TrackerDigis/MuAlCalIsolatedMu001_testing50.root",
    "file:///NOBACKUP/MC/InclusiveMuPt50_TrackerDigis/MuAlCalIsolatedMu002_testing50.root",
    ))
# process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(0))
# process.source = cms.Source("EmptySource")

### 
### Choose your refitter
### 
# process.Path = cms.Path(process.MuonAlignmentFromReferenceGlobalCosmicRefit)
# process.looper.tjTkAssociationMapTag = cms.InputTag("MuonAlignmentFromReferenceGlobalCosmicRefit:Refitted")
process.Path = cms.Path(process.MuonAlignmentFromReferenceGlobalMuonRefit)
process.looper.tjTkAssociationMapTag = cms.InputTag("MuonAlignmentFromReferenceGlobalMuonRefit:Refitted")

