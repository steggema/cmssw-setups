# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: reco -s RAW2DIGI,L1Reco,RECO --filein=/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-22Jan2013-v1/10000/FEE45EC2-F08F-E211-9F47-0030486791AA.root --fileout file:recoTestData.root --conditions=POSTLS171_V1::All --no_exec --datatier=AOD --data
import FWCore.ParameterSet.Config as cms

process = cms.Process('RERECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('/store/data/Run2012D/DoubleElectron/RAW-RECO/ZElectron-22Jan2013-v1/10000/FEE45EC2-F08F-E211-9F47-0030486791AA.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('reco nevts:1'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:recoTestData_timeCuts.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('AOD')
    )
)

# process.RECOSIMoutput.outputCommands += ['drop SiStripClusteredmNewDetSetVector_*_*_*', 'drop recoTrackExtras_generalTracks__*', 'drop SiPixelClusteredmNewDetSetVector_*_*_*', 'drop CaloTowersSorted_*_*_*', 'drop EcalRecHitsSorted_ecalPreshowerRecHit_*_*', 'drop TrackingRecHitsOwned_generalTracks_*_*', 'keep recoPFClusters_particleFlowClusterECAL_*_*']
process.RECOSIMoutput.outputCommands += ['drop *', 'keep recoPFClusters_particleFlowClusterECAL_*_*', 'keep recoTracks_generalTracks_*_*', 'keep recoPFJets_ak5PFJets_*_*', 'keep recoPFCandidates_particleFlow_*_*', 'keep recoPFMETs_*_*_*', 'keep recoGsfElectrons_*_*_*', 'keep recoPFCandidatesrecoPFCandidaterecoPFCandidatesrecoPFCandidateedmrefhelperFindUsingAdvanceedmRefsedmValueMap_particleBasedIsolation_gedGsfElectrons_*', 'keep floatedmValueMap_eid*_*_*', 'keep recoGsfTracks_electronGsfTracks_*_*', 'keep recoPFClusters_particleFlowClusterECALWithTimeUncorrected_*_*']

process.particleFlowClusterECALWithTimeUncorrected.pfClusterBuilder.minChi2Prob = cms.double(0.)
process.pfClusteringECAL = cms.Sequence(process.particleFlowRecHitECAL+process.particleFlowClusterECALSequence)
process.particleFlowClusterECALSequence.insert(1, process.particleFlowClusterECALWithTimeSelected)
process.particleFlowClusterECALWithTimeSelected.src = cms.InputTag('particleFlowClusterECALUncorrected')

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag, 'POSTLS171_V1::All', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_R_71_V1::All', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOSIMoutput_step)

process.csc2DRecHits.readBadChannels = cms.bool(False)
