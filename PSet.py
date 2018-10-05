#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
	'/uscms/home/kpadeken/nobackup/stuff/Analyzer_nano/RunIIFall17NanoAODDYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1F4D96515-8844-E811-AEE0-B496910A0290.root', ##you can change only this line
	'/uscms/home/kpadeken/nobackup/stuff/Analyzer_nano/RunIIFall17NanoAODDYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1F4D96515-8844-E811-AEE0-B496910A0290.root', ##you can change only this line
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

