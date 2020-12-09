from MadGraphControl.MadGraphUtils import *
import re
import math, cmath
import os

# PDF
pdflabel = 'lhapdf'
lhaid = 315000 # NNPDF31_lo_as_0118


# Getting bifundamental and inv fraction from filename
## Lets assume MC15.999999.MadGraphPythia8EvtGen_A14N30NLO_Mphi1500_Rinv3.py

Mphi = float(1500)
Rinv  = float(4)/10.0 

masses={
    '9000005': str(Mphi),
    '9000006': str(Mphi),
    '9000007': str(Mphi),
    '9000008': str(Mphi)
}

params={'MASS':masses}


my_process = """"
                import model DMsimp_tchannel/
                define gv = gv11 gv12 gv21 gv22
                define gv~ = gv11~ gv12~ gv21~ gv22~
                define j = g u c t d b s g u~ c~ t~ d~ b~ s~
                generate p p > gv gv~
                add process p p > gv gv~ j
                add process p p > gv gv~ j j
                output -f"""

process_dir = new_process(my_process)
runName='run_01'

genEvts = int(runArgs.maxEvents  * 1.2)

extras = {'lhe_version':'3.0',
          'cut_decays':'F',
          'event_norm':'sum',
          'pdlabel':pdflabel,
          'lhaid':lhaid,
          'use_syst':'T',
          'sys_scalefact': '1 0.5 2',
          'sys_pdf'      : "NNPDF31_lo_as_0130" ,
          'nevents'      : genEvts,
          'xqcut' : 100.0
          }

modify_param_card(process_dir=process_dir,params=params)
modify_run_card(process_dir=process_dir,runArgs=runArgs,settings=extras)

generate(process_dir=process_dir,runArgs=runArgs)

unzip1 = subprocess.Popen(['gunzip',process_dir+'/Events/'+runName+'/unweighted_events.lhe.gz'])
unzip1.wait()
oldlhe = open(process_dir+'/Events/'+runName+'/unweighted_events.lhe','r')
newlhe = open(process_dir+'/Events/'+runName+'/unweighted_events2.lhe','w')
init = True
for line in oldlhe:
            if '49001010' in line:
                line = line.replace('49001010','4900101')
            elif '49001011' in line:
                line = line.replace('49001011','4900101')
            elif '49001012' in line:
                line = line.replace('49001012','4900101')
            elif '49001013' in line:
                line = line.replace('49001013','4900101')
            elif '49001014' in line:
                line = line.replace('49001014','4900101')                            
            newlhe.write(line)
oldlhe.close()
newlhe.close()
zip1 = subprocess.Popen(['gzip',process_dir+'/Events/'+runName+'/unweighted_events2.lhe'])
zip1.wait()
shutil.move(process_dir+'/Events/'+runName+'/unweighted_events2.lhe.gz',process_dir+'/Events/'+runName+'/unweighted_events.lhe.gz')
os.remove(process_dir+'/Events/'+runName+'/unweighted_events.lhe')


arrange_output(process_dir=process_dir,runArgs=runArgs,lhe_version=3)

check_reset_proc_number(opts)

#### Shower 
evgenConfig.description = "Semivisible jets t-chan"
evgenConfig.keywords+=['BSM']
evgenConfig.generators+=["MadGraph","Pythia8","EvtGen"]
evgenConfig.contact  = ['deepak.kar@cern.ch']
#evgenConfig.inputfilecheck = runName
#runArgs.inputGeneratorFile=runName+'._00001.events.tar.gz'

###Pythia8 commands
#include("MC15JobOptions/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
#include("MC15JobOptions/Pythia8_MadGraph.py")
include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
include("Pythia8_i/Pythia8_MadGraph.py")


genSeq.Pythia8.Commands+=["4900001:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900002:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900003:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900004:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900005:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900006:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900011:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900012:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900013:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900014:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900015:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900016:m0 = 5000"]


# Fix dark hadron mass?
genSeq.Pythia8.Commands+=["HiddenValley:Ngauge  = 2"]
genSeq.Pythia8.Commands+=["HiddenValley:Lambda =1.0"]
genSeq.Pythia8.Commands+=["HiddenValley:alphaFSR = 1.0"]
genSeq.Pythia8.Commands+=["HiddenValley:spinFv = 0"]
genSeq.Pythia8.Commands+=["HiddenValley:FSR = on"]
genSeq.Pythia8.Commands+=["HiddenValley:fragment = on"]

genSeq.Pythia8.Commands+=["4900101:m0 = 10"]
genSeq.Pythia8.Commands+=["4900101:mWidth = 0.2"]
genSeq.Pythia8.Commands+=["4900101:mMin = 9.8"]
genSeq.Pythia8.Commands+=["4900101:mMax = 10.2"]
genSeq.Pythia8.Commands+=["4900111:m0 = 20"]
genSeq.Pythia8.Commands+=["4900113:m0 = 20"]
genSeq.Pythia8.Commands+=["51:m0 = 9.99"]
genSeq.Pythia8.Commands+=["53:m0 = 9.99"]

genSeq.Pythia8.Commands+=["HiddenValley:pTminFSR = 1.1"]
genSeq.Pythia8.Commands+=["HiddenValley:probVector = 0.75"]

genSeq.Pythia8.Commands+=["4900111:onechannel = 1 {0} 91 -3 3".format(1 - Rinv)] # check Rinv syntax
genSeq.Pythia8.Commands+=["4900111:addchannel = 1 {0} 0 51 -51".format(Rinv)]
genSeq.Pythia8.Commands+=["4900113:onechannel = 1 {0}  91 -1 1".format((1-Rinv)/5)] 
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -2 2".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -3 3".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -4 4".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -5 5".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0} 0 53 -53".format(Rinv)] 