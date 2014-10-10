# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: reco -s RAW2DIGI,L1Reco,RECO --filein=raw.root --fileout file:reco.root --conditions=POSTLS162_V2::All --no_exec --pileup=AVE_40_BX_25ns --customise=SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField=38T_PostLS1 --datatier=GEN-SIM-RECO- --geometry=Extended2015
import FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring(
    '/store/relval/CMSSW_7_1_0_pre3/RelValH130GGgluonfusion_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_POSTLS171_V1-v6/00000/F2A9CEAE-2AB3-E311-9935-0025904C6414.root',
    '/store/relval/CMSSW_7_1_0_pre3/RelValH130GGgluonfusion_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_POSTLS171_V1-v6/00000/FED5C983-27B3-E311-8203-0025904C5DD8.root',
    '/store/relval/CMSSW_7_1_0_pre3/RelValH130GGgluonfusion_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_POSTLS171_V1-v6/00000/D41354FA-26B3-E311-9E5F-0025904B7C40.root',
    '/store/relval/CMSSW_7_1_0_pre3/RelValH130GGgluonfusion_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_POSTLS171_V1-v6/00000/C81B5DBF-2AB3-E311-8B79-0025904C637A.root',
    '/store/relval/CMSSW_7_1_0_pre3/RelValH130GGgluonfusion_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_POSTLS171_V1-v6/00000/AC79DA22-26B3-E311-AFA6-0025904C637A.root',
    
                                      )
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
    fileName = cms.untracked.string('file:reco_timeFromSeed.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-AOD-')
    )
)

process.particleFlowClusterECALWithTimeUncorrected.pfClusterBuilder.clusterTimeResFromSeed = cms.bool(True)

process.RECOSIMoutput.outputCommands += ['drop SimTracks_g4SimHits_*_*', 'drop SiStripClusteredmNewDetSetVector_siStripClusters__RECO', 'drop SimVertexs_g4SimHits__SIM', 'keep recoPFClusters_particleFlowClusterECAL_*_*']
# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(40.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'POSTLS171_V1::All', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# process.particleFlowSuperClusterECAL.PFClusters = cms.InputTag("particleFlowClusterECALWithTime")
# process.particleFlowSuperClusterECAL.ESAssociation = cms.InputTag("particleFlowClusterECALWithTime")
# process.PFEcalClusterLabel = cms.InputTag("particleFlowClusterECALWithTime")

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions
