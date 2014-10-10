{
    gROOT->ProcessLine(".L /afs/cern.ch/user/b/benitezj/public/HTTSync/compareDataCardSummer13MSSM.C");
    compareDataCardSummer13MSSM("eleTau", "2012", "CERN", "./htt_et.inputs-mssm-8TeV-0.root", "Imperial", 
"/afs/cern.ch/user/s/steggema/CMSSW/CMSSW_6_1_1/src/auxiliaries/shapes/Imperial/htt_et.inputs-mssm-8TeV-0.root");
}
