# Auto generated configuration file
# using: 
# Revision: 1.20 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: RecoParticleFlow/Configuration/python/source_particleGun_cfi.py reco -s GEN,SIM,DIGI,L1,DIGI2RAW,HLT,RAW2DIGI,L1Reco,RECO --fileout file:/afs/cern.ch/work/s/steggema/GunTest_FULLSIM.root --eventcontent AODSIM --conditions=POSTLS162_V2::All --no_exec --pileup=AVE_40_BX_25ns --customise=SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField=38T_PostLS1 --datatier=GEN-SIM-RAW-RECO --geometry=Extended2015
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('RecoParticleFlow.PFProducer.particleFlowSimParticle_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('RecoParticleFlow/Configuration/python/source_particleGun_cfi.py nevts:1'),
    name = cms.untracked.string('Applications')
)


# Output definition

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:gun_0_photon_and_OOTPU_EB_defReco.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW-RECO')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

process.AODSIMoutput.outputCommands.extend(['drop *', 'keep recoGenParticles_*_*_*', 'keep recoPFSimParticles_*_*_*', 'keep recoPFClusters_particleFlowCluster*_*_*', 'keep recoPFClusters_particleFlowClusterECAL_*_*','keep recoPFClusters_particleFlowClusterECALUncorrected_*_*', 'keep recoPFClusters_particleFlowClusterECALWithTimeUncorrected_*_*'])


process.mix.input = cms.SecSource("PoolSource",
        nbPileupEvents = cms.PSet(
            averageNumber = cms.double(40.0)
        ),
        type = cms.string('fixed'),
        sequential = cms.untracked.bool(False),
        fileNames = cms.untracked.vstring('/store/mc/Fall13/MinBias_TuneA2MB_13TeV-pythia8/GEN-SIM/POSTLS162_V1-v1/30000/F69DBDB5-8623-E311-B248-001EC9B214BB.root')
)

process.mix.input.nbPileupEvents.averageNumber = cms.double(0.000001)
# process.mix.input.nbPileupEvents.averageNumber = cms.double(40.)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)


# Try to generate only OOT
process.mix.input.manage_OOT = cms.untracked.bool(True)
process.mix.input.OOT_type = cms.untracked.string('fixed')  ## generate OOT with a fixed distribution
process.mix.input.intFixed_OOT = cms.untracked.int32(40)
# process.mix.input.intFixed_OOT = cms.untracked.int32(1)

process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PRE_LS171_V9::All', '')

process.generator = cms.EDProducer("Pythia6PtGun",
    PGunParameters = cms.PSet(
        
        # ParticleID = cms.vint32(),
        # ParticleID = cms.vint32(22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22),
        ParticleID = cms.vint32(22),
        # ParticleID = cms.vint32(22, 22, 22, 22, 130, 130, 130, 130),
        # ParticleID = cms.vint32(130, 130, 130, 130, 130, 130, 130, 130),
        MaxEta = cms.double(0.205),
        MinPhi = cms.double(70.0),
        MaxPhi = cms.double(70.1),
        MinEta = cms.double(0.195),
        AddAntiParticle = cms.bool(False),
        MinPt = cms.double(1.0),
        MaxPt = cms.double(100.0)
    ),
    pythiaVerbosity = cms.untracked.bool(False),
    PythiaParameters = cms.PSet(
        pythiaUESettings = cms.vstring('MSTJ(11)=3     ! Choice of the fragmentation function', 
            'MSTJ(22)=2     ! Decay those unstable particles', 
            'PARJ(71)=10 .  ! for which ctau  10 mm', 
            'MSTP(2)=1      ! which order running alphaS', 
            'MSTP(33)=0     ! no K factors in hard cross sections', 
            'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)', 
            'MSTP(52)=2     ! work with LHAPDF', 
            'MSTP(81)=1     ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4     ! Defines the multi-parton model', 
            'MSTU(21)=1     ! Check on possible errors during program execution', 
            'PARP(82)=1.8387   ! pt cutoff for multiparton interactions', 
            'PARP(89)=1960. ! sqrts for which PARP82 is set', 
            'PARP(83)=0.5   ! Multiple interactions: matter distrbn parameter', 
            'PARP(84)=0.4   ! Multiple interactions: matter distribution parameter', 
            'PARP(90)=0.16  ! Multiple interactions: rescaling power', 
            'PARP(67)=2.5    ! amount of initial-state radiation', 
            'PARP(85)=1.0  ! gluon prod. mechanism in MI', 
            'PARP(86)=1.0  ! gluon prod. mechanism in MI', 
            'PARP(62)=1.25   ! ', 
            'PARP(64)=0.2    ! ', 
            'MSTP(91)=1      !', 
            'PARP(91)=2.1   ! kt distribution', 
            'PARP(93)=15.0  ! '),
        parameterSets = cms.vstring('pythiaUESettings')
    )
)


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.pfsim_step = cms.Path(process.particleFlowSimParticle)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.pfsim_step,process.endjob_step,process.AODSIMoutput_step])
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

# customisation of the process.

process.particleFlowClusterECALWithTimeUncorrected.pfClusterBuilder.clusterTimeResFromSeed = cms.bool(True)

process.particleFlowClusterECALWithTimeSelected.timingCutsLowBarrel = cms.vdouble(-12.0, -10.0, -10.0, -10.0, -10.0, -10.0)
process.particleFlowClusterECALWithTimeSelected.timingCutsHighBarrel = cms.vdouble(12.0, 10.0, 10.0, 10.0, 10.0, 10.0)


# process.VtxSmeared.TimeOffset = cms.double(-25.0)
process.VtxSmeared.SigmaZ = cms.double(0.001)
process.VtxSmeared.Z0 = cms.double(0.)
process.VtxSmeared.BetaStar = cms.double(5.)
process.VtxSmeared.Emittance = cms.double(1e-09)

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions
