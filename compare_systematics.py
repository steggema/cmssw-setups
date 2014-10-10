import math

from CMGTools.RootTools.Style import *
import ROOT
import os
import numpy

from CMGTools.RootTools.RootInit import *
from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle

from CMGTools.H2TauTau.proto.plotter.categories_common import *
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import *

xtitles = {
    'VBF_mjj':'m_{jj} [GeV]',
    'l2_pt':'p_{T,#mu} [GeV]',
    'l1_eta':'#eta_{#tau}',
    'l2_eta':'#eta_{#mu}',
    'l1_rawMvaIso':'MVA #tau iso',
    'l2_relIso05':'#mu iso',
    'mt':'m_{T} [GeV]',
    'visMass':'m_{vis} [GeV]',
    'svfitMass':'m_{sv} [GeV]',
    'nJets':'N_{jets}',
    'jet1_pt':'p_{T,jet1} [GeV]',
    'jet2_pt':'p_{T,jet2} [GeV]',
    'jet1_eta':'#eta_{jet1}',
    'jet2_eta':'#eta_{jet2}',
    'nVert':'# vertices',
    'mt':'m_T [GeV]',
    'pfmet':'PF E_{T}^{miss} [GeV]',
    'met':'PF E_{T}^{miss} [GeV]',
    'nJets':'N_{jets}',
    'nJets20':'N_{jets} (20 GeV)',
    'nBJets':'N_{B jets}',
    }


class SystComparisonPlotter:

    def __init__(self, directories=['/data/steggema/MuTauSignals', '/data/steggema/MuTauSignalsJERCorr'], titles=['Nominal', 'JER corrected'], treeName='H2TauTauTreeProducerTauMu', samples=['HiggsGGH125', 'HiggsVBF125', 'HiggsVH125']):

        self.treeName = treeName
        self.samples = samples
        self.sampleDirs = [os.path.join(os.getcwd(), dir) for dir in directories]
        self.titles = titles

        officialStyle(ROOT.gStyle)

        self.canvas = ROOT.TCanvas()

        self.canvas.UseCurrentStyle()
        self.canvas.SetLeftMargin(0.18)

    @staticmethod
    def createTPaveText(text, lowY=0.77, lowX=0.18):
        
        insertText = TPaveText(lowX, lowY, lowX+0.8, lowY+0.16, "NDC")
        insertText.SetBorderSize(0)
        insertText.SetFillStyle(0)
        insertText.SetTextAlign(12)
        insertText.SetTextSize (0.05)
        insertText.SetTextFont (62)
        insertText.AddText(text)
        insertText.Draw('same')

        return insertText

    @staticmethod
    def rocCurve(hSignal, hBG):
        ''' Create a ROC TGraph from two input histograms.
        '''
        maxBin = hSignal.GetNbinsX()

        effsS = [hS.Integral(nBin, maxBin)/hS.Integral() for nBin in range(1, maxBin + 1) ]
        rejB = [1. - hB.Integral(nBin, maxBin)/hB.Integral() for nBin in range(1, maxBin + 1) ]

        rocCurve = ROOT.TGraph(maxBin, numpy.asarray(effsS), numpy.asarray(rejB))

        return rocCurve

    @staticmethod
    def createLegend(xmin=0.19, xmax=0.85, ymin=0.7, ymax=0.9):
        ''' Creates legend with sensible defaults.
        '''
        legend = ROOT.TLegend(xmin, ymin, xmax, ymax, "", "NDC")
        legend.UseCurrentStyle()
        legend.SetFillColor(0)
        legend.SetLineColor(0)
        legend.SetLineWidth(0)
        legend.SetFillStyle(0)
        legend.SetLineStyle(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        return legend


    @staticmethod
    def drawHistComparison(hists):
        colours = [1, 2, 4, 6, 7, 8, 9]
        ymax = max([h.GetMaximum() for h in hists])
        drawString = ''
        for iColor, hist in enumerate(hists):
            #hist.SetTitle('')
            hist.UseCurrentStyle()
            hist.SetMinimum(0.)
            hist.GetYaxis().SetRangeUser(0., ymax * 1.1)
            hist.SetLineColor(colours[iColor])
            hist.SetMarkerColor(colours[iColor])
            hist.SetLineWidth(4)
            hist.SetLineStyle(iColor+1)
            hist.DrawCopy(drawString)
            drawString = 'SAME'

    def plotComparison(self, var, cut='',
             nbins=100, xmin=-1., xmax=1., weight=None, name='', cutTitle='', directory='JERPlots/'):

        if directory:
            if not os.path.exists(os.path.join(os.getcwd(), directory)):
                os.mkdir(os.path.join(os.getcwd(), directory))

        if weight is None:
            weight = 'weight'

        hists = []

        for sampleDir in self.sampleDirs:

            sName = var+'_s'
            hS = ROOT.TH1F(sName, sName, nbins, xmin, xmax)
            hS.SetTitle('')
            hS.GetYaxis().SetTitle("Event rate")
            hS.GetXaxis().SetTitle(xtitles[var])
            hists.append(hS)

            for sample in self.samples:

                tfile = ROOT.TFile.Open(os.path.join(sampleDir, sample, self.treeName)+'/'+self.treeName+'_tree.root')

                tree = tfile.Get(self.treeName)
                sName = var+sample+"_s_tmp"
                hSTmp = ROOT.TH1F(sName, sName, nbins, xmin, xmax)

                sExpr = '{0} * ({1})'.format(weight, cut)

                #print tree.GetEntries()
                tree.Project(sName, var, sExpr)
                print "Integral", hSTmp.Integral()
                #print sExpr
                hS.Add(hSTmp)
                

        self.drawHistComparison(hists)

        baseIntegral = hists[0].Integral()
        if baseIntegral == 0.:
            baseIntegral = 9999999999.

        legend = self.createLegend(xmin=0.45)
        for i, hist in enumerate(hists):
            if len(self.titles) > i:
                legend.AddEntry(hist, self.titles[i] + ' ({0:.3f})'.format(hist.Integral()/baseIntegral), 'L')

        legend.Draw()

        self.canvas.Print(directory+'/'+name+var+"_cuts.png")

        return self.canvas


if __name__ == '__main__':
    #p = SystComparisonPlotter(directory='/data/steggema/MuTauSignals', samples=['HiggsVBF125'])
    p = SystComparisonPlotter(directories=['/data/steggema/MuTauSignals', '/data/steggema/MuTauSignalsJERCorr'], titles=['Nominal', 'JER corrected']) # all samples

    newPUID = '&& ( (abs({jet}_eta) < 2.5 && {jet}_puMvaFull53X > -0.63) || (abs({jet}_eta) < 2.75 && {jet}_puMvaFull53X > -0.60) || (abs({jet}_eta) < 3.0 && {jet}_puMvaFull53X > -0.55) || (abs({jet}_eta) >= 3.0 && {jet}_puMvaFull53X > -0.45) )'

    #newPUIDSignalWeightUp = '(1. + ({jet}_genJetPt > 10. ' + newPUID + ') * 0.01)'
    newPUIDSignalWeightUp = '(1. + ({jet}_genJetPt > 10.) * 0.01)'
    #newPUIDSignalWeightDown = '(1. + ({jet}_genJetPt > 10. ' + newPUID + ') * (-0.01))'
    newPUIDSignalWeightDown = '(1. - ({jet}_genJetPt > 10.) * 0.01)'

    newPUIDBGWeightUp = '(1. + ({jet}_genJetPt < 10.) * 0.3)'
    newPUIDBGWeightDown = '(1. + ({jet}_genJetPt < 10.) * (-0.3))'

    newPUIDveto = '&& (!((abs({jet}_eta) < 2.5 && {jet}_puMvaFull53X > -0.63) || (abs({jet}_eta) < 2.75 && {jet}_puMvaFull53X > -0.60) || (abs({jet}_eta) < 3.0 && {jet}_puMvaFull53X > -0.55) || (abs({jet}_eta) >= 3.0 && {jet}_puMvaFull53X > -0.45) ))'

    inclusiveCut = categories['Xcat_IncX']

    cat0Jet = '&&'.join([categories['Xcat_J0X'], inclusiveCut])
    cat1Jet = '&&'.join([categories['Xcat_J1X'], inclusiveCut])
    cat2Jet = '&&'.join([categories['Xcat_J2X'], inclusiveCut])
    cat1B = '&&'.join([categories['Xcat_J1BX'], inclusiveCut])
    catVBF = '&&'.join([categories['Xcat_VBFX'], inclusiveCut])

    #p.plotSampleComparison('VBF_mjj', cut=catVBF, nbins=50, xmin=0., xmax=1000., cutName='VBF', cutTitle='VBF')

    class Variable:
        def __init__(self, name='VBF_mjj', nbins=50, xmin=500., xmax=2500.):
            self.name = name
            self.nbins = nbins
            self.xmin = xmin
            self.xmax = xmax


    variables = [
        Variable(name='VBF_mjj', xmin=500., xmax=2500., nbins=50),
        Variable(name='jet1_pt', xmin=0., xmax=500., nbins=50),
        Variable(name='jet2_pt', xmin=0., xmax=300., nbins=50),
        Variable(name='jet1_eta', xmin=-5., xmax=5., nbins=50),
        Variable(name='jet2_eta', xmin=-5., xmax=5., nbins=50),
        Variable(name='mt', xmin=0., xmax=150., nbins=50),
        Variable(name='pfmet', xmin=0., xmax=150., nbins=50),
        Variable(name='met', xmin=0., xmax=150., nbins=50),
        Variable(name='nJets', xmin=-0.5, xmax=3.5, nbins=4),
        Variable(name='nJets20', xmin=-0.5, xmax=6.5, nbins=7),
        Variable(name='nBJets', xmin=-0.5, xmax=3.5, nbins=4),
    ]

    for var in variables:
        p.plotComparison(var.name, cut=catVBF, nbins=var.nbins, xmin=var.xmin, xmax=var.xmax, name='VBF', cutTitle='VBF')
        p.plotComparison(var.name, cut=cat0Jet, nbins=var.nbins, xmin=var.xmin, xmax=var.xmax, name='ZeroJet', cutTitle='0 jets')
        p.plotComparison(var.name, cut=cat1Jet, nbins=var.nbins, xmin=var.xmin, xmax=var.xmax, name='OneJet', cutTitle='1 jet')
        p.plotComparison(var.name, cut=cat2Jet, nbins=var.nbins, xmin=var.xmin, xmax=var.xmax, name='TwoJets', cutTitle='2 jets')
        p.plotComparison(var.name, cut=cat1B, nbins=var.nbins, xmin=var.xmin, xmax=var.xmax, name='OneB', cutTitle='1 b jet')
