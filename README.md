# crab_submission

#Setup:
checkout any cmssw version, preferably a newer one but the ntupples don't depend on a specific version
```
cmsrel CMSSW_10_1_11
cd CMSSW_10_1_11/src/
git-cms-init
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone git@github.com:BSM3G/crab_submission.git BSM3GAna/BSM3GAna/test
scram b -j8 # if you are brave
git clone git@github.com:BSM3G/Analyzer.git BSM3GAna/BSM3GAna/data/Analyzer
scram b -j8
```
compile the Analyzer

#Run the submission
* Add your config to the analyzer
* **Test that the analyzer runs locally!!** Attention: crab will submbit everything in the data folder, so you might not want to put a large file in the data folder
* Make a text file with the samples you want to submit:
```
dasgoclient -query="dataset=/DY*/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_*/NANOAODSIM" > 05Feb2018_94X_MC.txt
```
* Create the crab config files:
`./make_crab_configs.py 05Feb2018_94X_MC.txt`
see `./make_crab_configs.py` for more options

* Submit the crab job (try a single one first before you submit everything)
`crab submit DYJetsToLL_M-50_HT-200to400_13TeV_ext1_MG_MC_crab_cfg.py`
to submit multiple jobs:
```
for i in *_crab_cfg.py
do
    crab submit $i
done
```
Use the normal CMS tools to supervise your jobs https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab


to copy a file to your local area, use:
```
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2_ext2-v1/40000/7219ED10-E510-E811-B946-D4856460625A.root .
```
    

