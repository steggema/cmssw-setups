# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: reco -s DIGI,L1,DIGI2RAW,RAW2DIGI,L1Reco,RECO --filein=gen.root --fileout file:reco.root --conditions=POSTLS171_V1::All --no_exec --pileup=AVE_40_BX_25ns --datatier=GEN-SIM-AOD --eventcontent AODSIM --geometry=Extended2015 --magField=38T_PostLS1 --customise=SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1
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
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('/store/mc/Fall13/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/GEN-SIM/POSTLS162_V1-v1/00000/F8433ED1-FCBD-E311-BB25-003048D2C16A.root')
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

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:reco.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-AOD')
    )
)

# Additional output definition

from CMGTools.Production.dataset import  createDataset
data = createDataset('CMS', '/MinBias_TuneA2MB_13TeV-pythia8/Fall13-POSTLS162_V1-v1/GEN-SIM', '*root', True)


process.mix.input = cms.SecSource("PoolSource",
        nbPileupEvents = cms.PSet(
            averageNumber = cms.double(1.0)
        ),
        type = cms.string('poisson'),
        sequential = cms.untracked.bool(False),
        fileNames = cms.untracked.vstring([data.listOfGoodFiles()[0]])
        # fileNames = cms.untracked.vstring('/store/mc/Fall13/MinBias_TuneA2MB_13TeV-pythia8/GEN-SIM/POSTLS162_V1-v1/30000/F69DBDB5-8623-E311-B248-001EC9B214BB.root')
    )

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(40.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'POSTLS171_V1::All', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.AODSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions
