from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from datetime import datetime

config = Configuration()
date_time = datetime.now()

config.section_("General")
config.General.requestName = 'NanoBSM3G_$SHORTSAMPLE'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py'] 
config.JobType.sendPythonFolder	 = True
config.JobType.outputFiles = ['output_log.log']
config.section_("Data")
config.Data.inputDataset = '$SAMPLE'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 300000
#config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/%s/$OUTPUTDIR' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoBSM3G_$SHORTSAMPLE'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"
config.JobType.allowUndistributedCMSSW = True 
#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

