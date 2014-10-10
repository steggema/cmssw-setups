import ROOT
from CMGTools.RootTools.RootInit import *
from CMGTools.H2TauTau.proto.plotter.categories_TauEle import *
from CMGTools.H2TauTau.proto.plotter.categories_common import *
from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
from CMGTools.H2TauTau.proto.plotter.rootutils import xtitles
from compare_systematics import SystComparisonPlotter as SystPlotter


colors = [1, 2, 3, 4, 6, 7, 9]

def setStyle(hist, i, var):
    hist.UseCurrentStyle()
    hist.SetLineColor(colors[i])
    hist.SetMarkerColor(colors[i])
    hist.SetLineStyle(i+1)
    hist.GetYaxis().SetTitle('Event rate')
    hist.GetXaxis().SetTitle(xtitles[var])

def main():

    officialStyle(ROOT.gStyle)

    tfile = ROOT.TFile('/data/steggema/Sep19EleTau/WJetsSoup/H2TauTauTreeProducerTauEle/H2TauTauTreeProducerTauEle_tree.root')
    tree = tfile.Get('H2TauTauTreeProducerTauEle')
    print tree

    # isoRegions = [(0., 1.5), (1.5, 3.), (3., 6.), (6., 10.)]
    isoRegions = [(0., 1.5), (1.5, 10.)]
    isoTitles = ['|{min:.1f}| < iso < |{max:.1f}|'.format(min=a[0], max=a[1]) for a in isoRegions]

    chargeRegions = ['&& diTau_charge == 0', '&& diTau_charge != 0']
    chargeTitles = ['OS', 'SS']

    vbfRegions = ['&& nJets>=2 && VBF_nCentral==0 && VBF_mjj > 500 && abs(VBF_deta) > 3.5',  '&& nJets>=2 && nBJets==0 && VBF_nCentral==0 && VBF_mjj>200 && abs(VBF_deta) > 2.']
    vbfTitles = ['VBF full', 'VBF relaxed']


    # vars = [('l2_pt', 15, 0., 150.), ('svfitMass', 10, 0., 200.), ('deltaPhiL1MET', 10, 0., 3.141593), ('deltaPhiL2MET', 10, 0., 3.141593), ('l1_pt', 15, 0., 150.), ('mt', 10, 0., 150.), ('met', 10, 0., 150.), ('l1_mass', 10, 0., 2.), ('l1_mass', 10, 0., 2.), ('l1_decayMode', 12, -0.5, 11.5)]

    vars = [('svfitMass', 10, 0., 300.), ('mt', 10, 0., 150.)]

    # basicCuts = [(inc_sig, ''), (str(inc_sig)+'&&'+cat_J1, '1J'), (str(inc_sig)+'&&'+cat_J0, '0J')]
    basicCuts = [(inc_sig, ''), (str(inc_sig) + '&& nJets>=2 && VBF_nCentral==0 && VBF_mjj > 500 && abs(VBF_deta) > 3.5', 'VBF'), (cat_Inc_AntiTauIsoJan, 'relaxTauIso')]
    
    c = ROOT.TCanvas()
    for basicCut in basicCuts:
        for var in vars:

            #ISO PLOT
            legend = SystPlotter.createLegend(xmin=0.45)
            hists = []
            for i, region in enumerate(isoRegions):
                histName = var[0] + str(i)
                hist = ROOT.TH1F(histName, '', var[1], var[2], var[3])
                hist.Sumw2()
                hists.append(hist)
                setStyle(hist, i, var[0])
                cut = str(basicCut[0]).replace('l1_threeHitIso<1.5', '(l1_threeHitIso>={min} && l1_threeHitIso<={max})'.format(min=region[0], max=region[1]))

                tree.Project(histName, var[0], 'weight * (' + cut + ')')
                hist.GetYaxis().SetRangeUser(0., hist.GetMaximum() * 1.3)
                if i == 0:
                    hist.DrawNormalized('hist e')
                else:
                    hist.DrawNormalized('same hist e')

                legend.AddEntry(hist, isoTitles[i], 'L')

            legend.Draw()
            c.Print('WJetsKinematics/'+var[0]+basicCut[1]+'_iso.png')
            c.Print('WJetsKinematics/'+var[0]+basicCut[1]+'_iso.pdf')


            # CHARGE PLOT
            legend = SystPlotter.createLegend(xmin=0.65)
            for i, region in enumerate(chargeRegions):
                histName = var[0] + str(i) + 'charge'
                hist = ROOT.TH1F(histName, '', var[1], var[2], var[3])
                hist.Sumw2()
                hists.append(hist)
                setStyle(hist, i, var[0])
                cut = str(basicCut[0]) + region

                tree.Project(histName, var[0], 'weight * (' + cut + ')')
                hist.GetYaxis().SetRangeUser(0., hist.GetMaximum() * 1.3)
                print chargeTitles[i], hist.Integral()
                if i == 0:
                    hist.DrawNormalized('hist e')
                else:
                    hist.DrawNormalized('same hist e')

                legend.AddEntry(hist, chargeTitles[i], 'L')

            legend.Draw()
            c.Print('WJetsKinematics/'+var[0]+basicCut[1]+'_charge.png')
            c.Print('WJetsKinematics/'+var[0]+basicCut[1]+'_charge.pdf')

            # VBF PLOT
            legend = SystPlotter.createLegend(xmin=0.65)
            for i, region in enumerate(vbfRegions):
                histName = var[0] + str(i) + 'vbf'
                hist = ROOT.TH1F(histName, '', var[1], var[2], var[3])
                hist.Sumw2()
                hists.append(hist)
                setStyle(hist, i, var[0])
                cut = str(basicCut[0]) + region

                tree.Project(histName, var[0], 'weight * (' + cut + ')')
                hist.GetYaxis().SetRangeUser(0., hist.GetMaximum() * 1.3)
                print chargeTitles[i], hist.Integral()
                if i == 0:
                    hist.DrawNormalized('hist e')
                else:
                    hist.DrawNormalized('same hist e')

                legend.AddEntry(hist, vbfTitles[i], 'L')

            legend.Draw()
            c.Print('WJetsKinematics/'+var[0]+basicCut[1]+'_vbf.png')
            c.Print('WJetsKinematics/'+var[0]+basicCut[1]+'_vbf.pdf')

if __name__ == '__main__':
    main()
