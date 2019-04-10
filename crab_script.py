#!/usr/bin/env python
import os
import subprocess
import shutil
from PhysicsTools.NanoAODTools.postprocessing.framework.jobreport import JobReport
# from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles#,runsAndLumis

# from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
#p=PostProcessor(".",inputFiles(),"Jet_pt>200",modules=[exampleModuleConstr()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
# p.run()
# cmssw_base=os.getenv("CMSSW_BASE")
# cmssw_base="./src/"

# inputFiles="dcap://dcap01.jinr-t1.ru:22125/pnfs/jinr-t1.ru/data/cms/store/mc/RunIIFall17NanoAOD/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/00580AEF-EB91-E811-9049-0CC47A4C8F0C.root"
job_report=JobReport()
bin_path="%s/src/BSM3GAna/BSM3GAna/data/Analyzer/"%(os.environ['CMSSW_BASE'])

output_file="tree.root"
output_log="output_log.log"

if os.path.exists(output_log):
    os.remove(output_log)
if os.path.exists(output_file):
    os.remove(output_file)


    
cwd=os.getcwd()
os.chdir(bin_path)
command="make clean; make ;./Analyzer -in "+" ".join(inputFiles())+" -out "+output_file+" -C PartDet"
# command="./Analyzer -in "+inputFiles+" -out output.root -C PartDet -t"
print "Command: "+command
# subprocess.call(command, shell=True, stderr=subprocess.STDOUT,)
try:
    logfile=open(output_log,"w")
    subprocess.call(command, shell=True, stderr=subprocess.STDOUT, stdout=logfile)
    logfile.close()

    if os.path.exists(output_log):
        shutil.copy(output_log,cwd)
    else:
        print "no log file"
    if os.path.exists(output_file):
        shutil.move(output_file,cwd)
    else:
        print "no output root file"
    logfile.close()
    
except Exception as e:
    print "problem at runtime ", e
# print out
logfile=open(output_log,"r")
print logfile.read()
os.chdir(cwd)
input_events=1
for line in logfile:
    if "TOTAL EVENTS:" in line:
        input_events=int(line.split(":")[-1].strip())

for infile in inputFiles():
    job_report.addInputFile(infile,input_events)

job_report.addOutputFile(output_file,input_events)

job_report.save()
try:
    if os.path.exists(output_log):
        shutil.copy(output_log,"cmsRun-stderr.log")
except Exception as e:
    print "could not copy logfile ",e
print "DONE"
os.system("ls -lR")

