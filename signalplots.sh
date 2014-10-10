python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX' -a -b -E -B -N 'Inclusive'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30' -a -b -E -B -N 'Inclusive_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0X' -a -b -E -B -N 'ZeroJet_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1X' -a -b -E -B -N 'OneJet_LowMT'

python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt>70' -a -b -E -B -N 'Inclusive_HighMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt>70 && Xcat_J0X' -a -b -E -B -N 'ZeroJet_HighMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt>70 && Xcat_J1X' -a -b -E -B -N 'OneJet_HighMT'


python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0_highX' -a -b -E -B -N 'ZeroJetHigh_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0_mediumX' -a -b -E -B -N 'ZeroJetMedium_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J0_lowX' -a -b -E -B -N 'ZeroJetLow_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1_high_mediumhiggsX' -a -b -E -B -N 'OneJetHighMediumHiggs_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1_high_lowhiggsX' -a -b -E -B -N 'OneJetHighLowHiggs_LowMT'
python plot_H2TauTauDataMC_TauMu_All.py /data/steggema/Jul19MuTauIncl/ tauMu_2012_cfg.py -H nJets -C 'Xcat_IncX && mt<30 && Xcat_J1_mediumX' -a -b -E -B -N 'OneJetMedium_LowMT'