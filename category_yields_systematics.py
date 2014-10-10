import ROOT
import math

from CMGTools.H2TauTau.proto.plotter.categories_TauMu import *

samples = ['TTJets', 'HiggsVBF125', 'HiggsVBF145', 'HiggsVBF110', 'HiggsGGH125', 'HiggsVH125', 'ZJ', 'ZL']
# samples = ['ZJ', 'ZL']

directories = ['/data/steggema/June19jetidnominal', '/data/steggema/June19jesup', '/data/steggema/June19jesdown']

names = ['nominal', 'jesup', 'jesdown']

treeLocation = 'H2TauTauTreeProducerTauMu/H2TauTauTreeProducerTauMu_tree.root'
treeName = 'H2TauTauTreeProducerTauMu'

cats = [cat_J0_high, cat_J0_medium, cat_J0_low, cat_J1_high_mediumhiggs, cat_J1_high_lowhiggs, cat_J1_medium, cat_VBF_tight, cat_VBF_loose, cat_J0, cat_J1, cat_VBF, cat_J0_oldlow, cat_J0_oldhigh, cat_J1_oldlow, cat_J1_oldhigh, cat_0B, cat_1BInclusive]
catNames = ['0 jet high', '0 jet medium', '0 jet low', '1 jet high medium higgs', '1 jet high low higgs', '1 jet medium', 'VBF tight', 'VBF loose', '0 jet', '1 jet', 'VBF', 'Old 0 jet low', 'Old 0 jet high', 'Old 1 jet low', 'Old 1 jet high', '0 b jets', '>= 1 bjet']

ele = True

categories = [cat_Inc + '&& mt < 30.' + '&&' + cat for cat in cats]
if ele:
    categories = [cat_Inc_elelike + '&& mt < 30.' + '&&' + cat for cat in cats]

if ele:
    cats = [cat_J0_high, cat_J0_medium, cat_J0_low, cat_J1_high_mediumhiggs + '&& met>30.', cat_J1_high_lowhiggs + '&& met>30.', cat_J1_medium + '&& met>30.', cat_VBF_tight, cat_VBF_loose, cat_J0, cat_J1 + '&& met>30.', cat_VBF]

weight = 'weight'

variable = 'svfitMass'
xmin = 0.
xmax = 1000.
nbins = 50

catsSamplesUncertaintiesErrors = {}
for s in catNames:
    catsSamplesUncertaintiesErrors[s] = {}

for sample in samples:
    print '\n\nSAMPLE\n', sample
    catYields = []
    for j, directory in enumerate(directories): # samples first to only open trees once
        print 'VARIATION', names[j]
        fileSample = sample
        if sample == 'ZJ' or sample == 'ZL':
            fileSample = 'DYJets'
        tfile = ROOT.TFile(directory + '/' + fileSample + '/' +treeLocation)
        tree = tfile.Get(treeName)
        catYields.append([])
        for i, cat in enumerate(categories):
            histName = 'h_'+sample+str(i)
            hist = ROOT.TH1F(histName, '', nbins, xmin, xmax)
            hist.Sumw2()
            if sample == 'ZJ':
                cat = cat + '&& isFake==2'
            elif sample == 'ZL':
                cat = cat + '&& isFake==1'
            tree.Project(histName, variable, weight + '*(' + cat +')')
            error = ROOT.Double(0.)
            integral = hist.IntegralAndError(1, hist.GetNbinsX(), error)
            # print hist.Integral()
            

            histNJets = ROOT.TH1F(histName+'njets', '', 4, -0.5, 3.5)
            tree.Project(histName+'njets', 'nJets', weight + '*(' + cat +')')
            if histNJets.Integral() > 0.:
                histNJets.Scale(1./histNJets.Integral())
            errorSum = 0.
            for iBin in range(1, 5):
                binContent = histNJets.GetBinContent(iBin)
                errorSum += binContent * math.sqrt(sum(0.01*0.01 for n in range(iBin - 1)))
            print 'errorSum', errorSum

            catYields[j].append((integral, error, errorSum))

    for i, cat in enumerate(categories):
        print '\n', catNames[i]
        # print [yields[i][0] for yields in catYields]
        # print [yields[i][1] for yields in catYields]
        if catYields[0][i][0] == 0.:
            catsSamplesUncertaintiesErrors[catNames[i]][sample] = (0., 0.)
            continue
        diffs = [yields[i][0]/catYields[0][i][0] - 1. for yields in catYields]
        statUncDiffUncorr = [yields[i][1]/yields[i][0] for yields in catYields]
        statUncDiff = [math.sqrt(abs(yields[i][0] - catYields[0][i][0]))/yields[i][0] for yields in catYields]
        print diffs[1], "pm", statUncDiff[1], "pm", statUncDiffUncorr[1]
        print diffs[2], "pm", statUncDiff[2], "pm", statUncDiffUncorr[2]
        average = (diffs[1] - diffs[2])/2.
        errorAverage = math.sqrt(statUncDiff[1]**2 +statUncDiff[2]**2)
        print "Average", average, "pm", errorAverage
        average = math.sqrt(average*average +catYields[0][i][2]*catYields[0][i][2] )
        print 'With PU ID 1%', catYields[0][i][2], 'pm', average
        catsSamplesUncertaintiesErrors[catNames[i]][sample] = (average, errorAverage)

for c in catsSamplesUncertaintiesErrors:
    print
    print "CATEGORY", c
    print
    for sample in samples:
        print sample, round(catsSamplesUncertaintiesErrors[c][sample][0], 2), round(catsSamplesUncertaintiesErrors[c][sample][1], 2)


