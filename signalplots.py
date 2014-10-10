import subprocess
import os
import time

processes = set()
max_processes = 4

inputDir = '/data/steggema/Jul23TauEle/'
inputCfg = 'tauEle_2012_cfg.py'

cats = [
	('Xcat_IncX', 'Inclusive_NoMT'),
	('Xcat_IncX && mt<30', 'Inclusive'),
	('Xcat_IncX && mt<30 && Xcat_J0X', 'ZeroJet'), 
	('Xcat_IncX && mt<30 && Xcat_J1X', 'OneJet'),
	('Xcat_IncX && mt>70', 'Inclusive_HighMT'),
	('Xcat_IncX && mt>70 && Xcat_J0X', 'ZeroJet_HighMT'),
	('Xcat_IncX && mt>70 && Xcat_J1X', 'OneJet_HighMT'),
	('Xcat_IncX && mt<30 && Xcat_J0_highX', 'ZeroJetHigh'),
	('Xcat_IncX && mt<30 && Xcat_J0_mediumX', 'ZeroJetMedium'),
	('Xcat_IncX && mt<30 && Xcat_J0_lowX', 'ZeroJetLow'),
	('Xcat_IncX && mt<30 && Xcat_J1_high_mediumhiggsX && met>30', 'OneJetHighMediumHiggs'),
	('Xcat_IncX && mt<30 && Xcat_J1_high_lowhiggsX && met>30', 'OneJetHighLowHiggs'),
	('Xcat_IncX && mt<30 && Xcat_J1_mediumX && met>30', 'OneJetMedium'),
    ('Xcat_IncX && mt<30 && Xcat_VBF_looseX', 'VBF_loose'),
    ('Xcat_IncX && mt<30 && Xcat_VBF_tightX', 'VBF_tight'),
    ('Xcat_IncX && mt<30 && Xcat_J1BX', 'OneB'),
    ('Xcat_IncX && mt<30 && Xcat_0BX', 'ZeroB'),
]

# From http://stackoverflow.com/questions/4992400/running-several-system-commands-in-parallel
for cat in cats:
    args = ['python', 'plot_H2TauTauDataMC_TauEle_All.py', inputDir, inputCfg, '-H', 'nJets', '-C', cat[0], '-a', '-b', '-E', '-B', '-N', cat[1], '-g', '125']
    print args
    processes.add(subprocess.Popen(args))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update(
            p for p in processes if p.poll() is not None)

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()



# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX' -a -b -E -B -N 'Inclusive'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30' -a -b -E -B -N 'Inclusive_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0X' -a -b -E -B -N 'ZeroJet_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1X' -a -b -E -B -N 'OneJet_LowMT'

# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt>70' -a -b -E -B -N 'Inclusive_HighMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt>70 && Xcat_J0X' -a -b -E -B -N 'ZeroJet_HighMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt>70 && Xcat_J1X' -a -b -E -B -N 'OneJet_HighMT'


# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0_highX' -a -b -E -B -N 'ZeroJetHigh_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0_mediumX' -a -b -E -B -N 'ZeroJetMedium_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0_lowX' -a -b -E -B -N 'ZeroJetLow_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1_high_mediumhiggsX' -a -b -E -B -N 'OneJetHighMediumHiggs_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1_high_lowhiggsX' -a -b -E -B -N 'OneJetHighLowHiggs_LowMT'
# python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1_mediumX' -a -b -E -B -N 'OneJetMedium_LowMT'