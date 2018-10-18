#!/bin/env python

from datetime import datetime
import optparse
import re
from collections import OrderedDict
from string import Template
import sys
import os

generators = OrderedDict()
generators['madgraph'] = 'MG'
generators['powheg'] = 'PH'
generators['herwig6'] = 'HW'
generators['herwigpp'] = 'HP'
generators['herwig'] = 'HW'
generators['sherpa'] = 'SP'
generators['amcatnlo'] = 'AM'
generators['alpgen'] = 'AG'
generators['calchep'] = 'CA'
generators['comphep'] = 'CO'
generators['lpair'] = 'LP'
generators['pythia6'] = 'P6'
generators['pythia8'] = 'P8'
generators['pythia'] = 'PY'
generators['gg2ww'] = 'GG'
generators['gg2zz'] = 'GG'
generators['gg2vv'] = 'GG'
generators['JHUGen'] = 'JG'
generators['blackmax'] = 'BM'
generators['unknown'] = '??'

# list of generators used for hadronization on top of another generator (will be removed from name)
showers = [ 'pythia8', 'pythia6', 'pythia', 'herwigpp']

# list of tags which will be removed from name (case insensitive)
blacklist = ['13tev',
             'madspin',
             'FXFX',
             'MLM',
             'NNPDF30',
             'TuneCUEP8M1',
             'TuneCUETP8M1',
             'TuneCUETP8M2T4']


def parse_name(dataset, options):
    # format of datasetpath: /.../.../...
    # first part contains name + additional tags ( cme, tune, .. )
    # second part has additional information ( campaign, extention sample? ,... )
    # third part contains sample 'format' (AOD, MINIAOD, ...)
    dataset_split = dataset.split('/')
    ds_pt1 = dataset_split[1]
    ds_pt2 = dataset_split[2]
    ds_pt3 = "MC" if "SIM" in dataset_split[3] else "Data"
    for generator in generators.keys():
        # subn() performs sub(), but returns tuple (new_string, number_of_subs_made)
        # using (?i) at the beginning of a regular expression makes it case insensitive
        ( ds_pt1, n ) = re.subn( r'(?i)[_-]' + generator, '', ds_pt1 )
        if n > 0:
            _generator = generator
            for shower in showers:
                ds_pt1 = re.sub( r'(?i)[_-]' + shower, '', ds_pt1 )
            break
        else:
            _generator = 'unknown'
    for item in blacklist:
        ds_pt1 = re.sub( r'(?i)[_-]*' + item, '', ds_pt1 )
    match = re.search('ext\d\d*',ds_pt2)
    if match:
        name = ds_pt1 + "_" + options.cme + "TeV_" + match.group() + "_" + options.postfix + generators[_generator]+"_"+ds_pt3
    else:
        name = ds_pt1 + "_" + options.cme + "TeV_" + options.postfix + generators[_generator]+"_"+ds_pt3
    return name
    

    

def get_samples_from_cfg(cfg):
    samples=[]
    f=open(cfg)
    for line in f:
        if line[0]!="#":
            samples.append(line.strip())
    return samples

def make_config(sample, options):
    
    short_name=parse_name(sample, options)
    
    d=dict(
        SAMPLE=sample,
        SHORTSAMPLE=short_name,
        OUTPUTDIR=options.outputFolder,
    )
    
    file=open("crab_cfg_template.py","r")
    text=file.read()
    file.close()
    newText=Template(text).safe_substitute(d)
    fileNew=open("%s/%s_crab_cfg.py"%(options.outputFolder,short_name),"w+")
    fileNew.write(newText)
    fileNew.close()
        

def main():

    date_time = datetime.now()
    usage = '%prog [options] CONFIG_FILE'
    parser = optparse.OptionParser( usage = usage )

    parser.add_option( '-C', '--configdir', default = "PartDet", metavar = 'DIRECTORY',
                            help = 'Define the config directory. [default = %default]')
    parser.add_option( '-c', '--CR', action = 'store_true', default = False,
                            help = 'Run with the CR flag. [default = %default]')
    parser.add_option( '--debug', metavar = 'LEVEL', default = 'INFO',
                       help= 'Set the debug level. Allowed values: ERROR, WARNING, INFO, DEBUG. [default = %default]' )
    parser.add_option( '-e', '--cme', action = 'store', default = '13', metavar = 'ENERGY',
                       help = 'The center-of-mass energy for this sample' )
    parser.add_option( '-p', '--prefix', action = 'store', default = None, metavar = 'PREFIX',
                       help = 'Specify a PREFIX for your output filename (e.g.  production version). [default = %default]' )
    parser.add_option( '-P', '--postfix', action = 'store', default = None, metavar = 'POSTFIX',
                       help = 'Specify a POSTFIX for every process name in the output file. [default = %default]' )
    parser.add_option( '-o', '--outputFolder', default = "REPLACEBYTAG/",                                                                         metavar = 'DIRECTORY',
                        help = 'Define path for the output files [default = %default]')
    parser.add_option( '-t', '--Tag', default = "run_%s_%s_%s_%s"%(date_time.year,
                                                                        date_time.month,
                                                                        date_time.day,
                                                                        date_time.hour,
                                                                        ), metavar = 'DIRECTORY',
                        help = 'Define a Tag for the output directory. [default = %default]' )

    ( options, args ) = parser.parse_args()
    if len( args ) != 1:
        parser.error( 'Exactly one CONFIG_FILE required!' )
    options.outputFolder=options.outputFolder.replace("REPLACEBYTAG",options.Tag)
    if options.postfix:
        options.postfix += '_'
    if options.postfix == None:
        options.postfix = ''
    
    if os.path.exists(options.outputFolder):
        print "The outpath "+options.outputFolder+" already exists pick a new one or use --force"
        sys.exit(3)
    os.makedirs(options.outputFolder)

    
    cfgFile = args[ 0 ]
    samples=get_samples_from_cfg(cfgFile)
    
    for sample in samples:
        make_config(sample, options)
        # print parse_name(sample, options)
    
    







if __name__ == '__main__':
    main()
