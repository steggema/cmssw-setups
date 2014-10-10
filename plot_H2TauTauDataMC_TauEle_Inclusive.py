import imp
import math
import copy
import time
import re

from CMGTools.H2TauTau.proto.HistogramSet import histogramSet
from CMGTools.H2TauTau.proto.plotter.H2TauTauDataMC import H2TauTauDataMC
from CMGTools.H2TauTau.proto.plotter.prepareComponents import prepareComponents
from CMGTools.H2TauTau.proto.plotter.rootutils import *
from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer
from CMGTools.H2TauTau.proto.plotter.titles import xtitles
from CMGTools.H2TauTau.proto.plotter.blind import blind
from CMGTools.H2TauTau.proto.plotter.plotmod import *
from CMGTools.H2TauTau.proto.plotter.datacards import *
# from CMGTools.H2TauTau.proto.plotter.plotinfo import *
from CMGTools.H2TauTau.proto.plotter.plotinfo import plots_All as plots_All
from CMGTools.H2TauTau.proto.plotter.categories_TauEle import *
from CMGTools.RootTools.Style import *
from ROOT import kPink, TH1, TPaveText, TPad
import ROOT

cp = copy.deepcopy
EWK = 'WJets'

    
NBINS = 100
XMIN  = 0
XMAX  = 200


# JAN = we don't need this do we?

def replaceShapeInclusiveRetarded(plot, var, anaDir,
                          comp, weights, 
                          cut, weight,
                          embed, shift):
    '''Replace WJets with the shape obtained using a relaxed tau iso'''
    cut = cut.replace('l1_looseMvaIso>0.5', 'l1_rawMvaIso>0.5')
    # cut = cut.replace('nBJets>=1', '1')
    print '[INCLUSIVE] estimate',comp.name,'with cut',cut
    plotWithNewShape = cp( plot )
    wjyield = plot.Hist(comp.name).Integral()
    nbins = plot.bins
    xmin = plot.xmin
    xmax = plot.xmax
    wjshape = shape(var, anaDir,
                    comp, weights, nbins, xmin, xmax,
                    cut, weight,
                    embed, shift)
    # import pdb; pdb.set_trace()
    wjshape.Scale( wjyield )
    # import pdb; pdb.set_trace()
    plotWithNewShape.Replace(comp.name, wjshape) 
    # plotWithNewShape.Hist(comp.name).on = False 
    return plotWithNewShape

    

def makePlot( var, anaDir, selComps, weights, wJetScaleSS, wJetScaleOS,
              w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio,
              nbins=None, xmin=None, xmax=None,
              cut='', weight='weight', embed=False, shift=None, replaceW=False,
              VVgroup=None, antiEleIsoForQCD=False, subtractBGForQCDShape=False):
    
    print 'making the plot:', var, 'cut', cut

    oscut = cut+' && diTau_charge==0'
    osign = H2TauTauDataMC(var, anaDir,
                           selComps, weights, nbins, xmin, xmax,
                           cut=oscut, weight=weight, shift=shift,
                           embed=embed,
                           treeName = 'H2TauTauTreeProducerTauEle')
    osign.Hist(EWK).Scale( wJetScaleOS ) # * w_mt_ratio / w_mt_ratio_os )
    
    if cut.find('mt<')!=-1:
        print 'correcting high->low mT extrapolation factor, OS', w_mt_ratio / w_mt_ratio_os
        osign.Hist(EWK).Scale( w_mt_ratio / w_mt_ratio_os )

    replaceW = False
    if replaceW:
        osign = replaceShapeInclusive(osign, var, anaDir,
                                      selComps['WJets'], weights, 
                                      oscut, weight,
                                      embed, shift)
    sscut = cut+' && diTau_charge!=0'
    ssign = H2TauTauDataMC(var, anaDir,
                           selComps, weights, nbins, xmin, xmax,
                           cut=sscut, weight=weight, shift=shift,
                           embed=embed,
                           treeName = 'H2TauTauTreeProducerTauEle')
    ssign.Hist(EWK).Scale( wJetScaleSS )
    if cut.find('mt<')!=-1:
        print 'correcting high->low mT extrapolation factor, SS', w_mt_ratio / w_mt_ratio_ss
        ssign.Hist(EWK).Scale( w_mt_ratio / w_mt_ratio_ss  ) 
    if replaceW:
        ssign = replaceShapeInclusive(ssign, var, anaDir,
                                      selComps['WJets'], weights, 
                                      sscut, weight,
                                      embed, shift)
    if VVgroup:
        ssign.Group('VV',VVgroup)
        osign.Group('VV',VVgroup)
    
    ssQCD, osQCD = getQCD( ssign, osign, 'Data', VVgroup, subtractBGForShape=subtractBGForQCDShape)
    if antiEleIsoForQCD:
        print 'WARNING INVERTING ELE ISO FOR QCD SHAPE'
        # replace QCD with a shape obtained from data in an anti-iso control region
        qcd_yield = osQCD.Hist('QCD').Integral()
        
        # sscut_qcdshape = cut.replace('l2_relIso05<0.1','l2_relIso05>0.2 && l2_relIso05<0.5') + ' && diTau_charge!=0' 
        sscut_qcdshape = cut.replace('l2_relIso05<0.1','l2_relIso05>0.2 && l2_relIso05<0.5') + ' && diTau_charge!=0'
        # JAN - don't replace tau iso #.replace('l1_looseMvaIso>0.5', 'l1_rawMvaIso>0.7') +
        ssign_qcdshape = H2TauTauDataMC(var, anaDir,
                                        selComps, weights, nbins, xmin, xmax,
                                        cut=sscut_qcdshape, weight=weight,
                                        embed=embed,
                                        treeName = 'H2TauTauTreeProducerTauEle')
        qcd_shape = copy.deepcopy( ssign_qcdshape.Hist('Data') )    
        qcd_shape.Normalize()
        qcd_shape.Scale(qcd_yield)
        osQCD.Replace('QCD', qcd_shape)

    # osQCD.Group('VV', ['WW','WZ','ZZ'])
    osQCD.Group('electroweak', ['WJets', 'Ztt_ZJ','VV'])
    osQCD.Group('Higgs 125', ['HiggsVBF125', 'HiggsGGH125', 'HiggsVH125'])
    return ssign, osign, ssQCD, osQCD


def drawAll(cut, plots, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, embed=True, blind=True):
    '''See plotinfo for more information'''
    for name, plot in plots.items():
        print plot.var
        print '----------------', plot.xmin, plot.xmax, plot.nbins
        print fwss, fwos
        ss, osign, ssQ, osQ = makePlot( plot.var, anaDir=anaDir,
                                     selComps=selComps, weights=weights, wJetScaleSS=fwss, wJetScaleOS=fwos,
                                     w_mt_ratio_ss=w_mt_ratio_ss, w_mt_ratio_os=w_mt_ratio_os, w_mt_ratio=w_mt_ratio, 
                                     nbins=plot.nbins, xmin=plot.xmin, xmax=plot.xmax,
                                     cut=cut, weight=weight, embed=embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiEleIsoForQCD=antiEleIsoForQCD)

        outDir = 'Summer13StackPlotsJul04/'+options.cutName+'/'
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        if name != plot.var:
            outDir += name + '_'
        # drawOfficial(osQ, blind, plotprefix=outDir)
        draw(osQ, blind, plotprefix=outDir, channel='TauEle')
        osQ.ratioTotalHist.weighted.Fit('pol0', '', '', 0., 60.)
        plot.ssign = cp(ss)
        plot.osign = cp(osign)
        plot.ssQCD = cp(ssQ)
        plot.osQCD = cp(osQ)
        # time.sleep(1)

def handleW( anaDir, selComps, weights,
             cut, weight, embed, VVgroup, nbins=50, highMTMin=70., highMTMax=1070,
             lowMTMax=20.):

    treeName = 'H2TauTauTreeProducerTauEle'
    cut = cut.replace('mt<30', '1') # 30 is the new default
    cut = cut.replace('mt<20', '1')
    fwss, fwos, ss, os = plot_W(
        anaDir, selComps, weights,
        nbins, highMTMin, highMTMax, cut,
        weight=weight, embed=embed,
        VVgroup = VVgroup,
        treeName = treeName)

    w_mt_ratio_ss = w_lowHighMTRatio('mt', anaDir, selComps['WJets'], weights, cut, weight, lowMTMax, highMTMin, highMTMax, 'diTau_charge!=0', treeName=treeName);
    w_mt_ratio_os = w_lowHighMTRatio('mt', anaDir, selComps['WJets'], weights, cut, weight, lowMTMax, highMTMin, highMTMax, 'diTau_charge==0', treeName=treeName);
    w_mt_ratio = w_lowHighMTRatio('mt', anaDir, selComps['WJets'], weights, cut, weight, lowMTMax, highMTMin, highMTMax, '1', treeName=treeName);

    return fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio


if __name__ == '__main__':

    import copy
    from optparse import OptionParser
    from CMGTools.RootTools.RootInit import *
    from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
    officialStyle(gStyle)


    parser = OptionParser()
    parser.usage = '''
    %prog <anaDir> <cfgFile>

    cfgFile: analysis configuration file, see CMGTools.H2TauTau.macros.MultiLoop
    anaDir: analysis directory containing all components, see CMGTools.H2TauTau.macros.MultiLoop.
    hist: histogram you want to plot
    '''
    parser.add_option("-H", "--hist", 
                      dest="hist", 
                      help="histogram list",
                      default=None)
    parser.add_option("-C", "--cut", 
                      dest="cut", 
                      help="cut to apply in TTree::Draw",
                      default='1')
    parser.add_option("-E", "--embed", 
                      dest="embed", 
                      help="Use embedd samples.",
                      action="store_true",
                      default=False)
    parser.add_option("-B", "--blind", 
                      dest="blind", 
                      help="Blind.",
                      action="store_true",
                      default=False)
    parser.add_option("-b", "--batch", 
                      dest="batch", 
                      help="Set batch mode.",
                      action="store_true",
                      default=False)
    parser.add_option("-n", "--nbins", 
                      dest="nbins", 
                      help="Number of bins",
                      default=None)
    parser.add_option("-m", "--min", 
                      dest="xmin", 
                      help="xmin",
                      default=None)
    parser.add_option("-M", "--max", 
                      dest="xmax", 
                      help="xmax",
                      default=None)
    parser.add_option("-g", "--higgs", 
                      dest="higgs", 
                      help="Higgs mass: 125, 130,... or dummy",
                      default=None)
    parser.add_option("-a", "--all", 
                      dest="allPlots", 
                      help="All plots.",
                      action="store_true",
                      default=False)
    parser.add_option("-N", "--cutName", 
                      dest="cutName", 
                      help="name to prepend for output plots.",
                      default='1')

    (options,args) = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)
    if options.batch:
        gROOT.SetBatch()
    if options.nbins is None:
        NBINS = binning_svfitMass_finer
        XMIN = None
        XMAX = None
    else:
        NBINS = int(options.nbins)
        XMIN = float(options.xmin)
        XMAX = float(options.xmax)
        
    cutstring = options.cut
    antiEleIsoForQCD = cutstring.find('l1_pt>40')!=-1 or cutstring.find('Xcat_J1X')!=-1
    options.cut = replaceCategories(options.cut, categories) 
    
    # TH1.AddDirectory(False)
    dataName = 'Data'
    weight='weight'
    replaceW = False

    makeQCDIsoPlots = True
    
    anaDir = args[0].rstrip('/')
    shift = None
    if anaDir.endswith('_Down'):
        shift = 'Down'
    elif anaDir.endswith('_Up'):
        shift = 'Up'
        
    cfgFileName = args[1]
    file = open( cfgFileName, 'r' )
    cfg = imp.load_source( 'cfg', cfgFileName, file)
    embed = options.embed

    aliases = None
    selComps, weights, zComps = prepareComponents(anaDir, cfg.config, aliases, options.embed, channel='TauEle', higgsMass=options.higgs)

    # can, pad, padr = buildCanvas()
    ocan = buildCanvasOfficial()
    
    fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio = handleW(
        anaDir, selComps, weights,
        options.cut, weight, options.embed, cfg.VVgroup
        )

    if options.allPlots:
        drawAll(options.cut, plots_All, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, options.embed, options.blind)
    else:
        if makeQCDIsoPlots:
            ssign, osign, ssQCD, osQCD = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiEleIsoForQCD=False)

            # ssignAM, osignAM, ssQCDAM, osQCDAM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiEleIsoForQCD=True)
            ssignAM, osignAM, ssQCDAM, osQCDAM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiEleIsoForQCD=False, subtractBGForQCDShape=True)


            # ssignATM, osignATM, ssQCDATM, osQCDATM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiTauAntiMuIsoForQCD=True)
            ssignATM, osignATM, ssQCDATM, osQCDATM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiEleIsoForQCD=True, subtractBGForQCDShape=False)

            # ssignATM, osignATM, ssQCDATM, osQCDATM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=False, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=False)

            # can = buildCanvasOfficial()
            can, pad, padr = buildCanvas()
            pad.cd()
            #
            hQCD = osQCD.Hist('QCD').weighted.Clone()
            hQCD.GetXaxis().SetTitle('m_{#tau #tau} [GeV]')
            hQCD.GetYaxis().SetTitle('Events')
            hQCD.SetFillColor(0)
            hQCD.SetLineColor(hQCD.GetMarkerColor())
            hQCD.SetTitle('SS')
            # hQCDAM = osQCDAM.Hist('QCD').weighted
            # hQCDAM.SetTitle('QCD SS #mu')
            #
            hQCDAM = osQCDAM.Hist('QCD').weighted
            hQCDAM.SetTitle('SS BG-sub')
            hQCDAM.GetXaxis().SetTitle('m_{#tau #tau} [GeV]')
            hQCDAM.GetYaxis().SetTitle('Events')
            #
            hQCDAM.SetMarkerColor(1)
            hQCDAM.SetLineColor(1)
            hQCDAM.SetFillColor(0)
            #
            hQCDATM = osQCDATM.Hist('QCD').weighted
            # hQCDATM.SetTitle('QCD SS #mu #tau')
            hQCDATM.SetTitle('SS anti e iso')
            # hQCDATM.SetTitle('QCD SS')
            hQCDATM.SetMarkerColor(2)
            hQCDATM.SetLineColor(2)
            hQCDATM.SetFillColor(0)
            leg = ROOT.TLegend(0.5,0.46,0.88,0.89)
            leg.SetFillColor(0)
            leg.SetFillStyle(0)
            leg.SetLineColor(0)
            # leg.AddEntry(hQCD, hQCD.GetTitle())
            leg.AddEntry(hQCDAM, hQCDAM.GetTitle())
            leg.AddEntry(hQCDATM, hQCDATM.GetTitle())
            ks1 = hQCD.KolmogorovTest(hQCDAM)
            ks2 = hQCD.KolmogorovTest(hQCDATM)
            ks3 = hQCDAM.KolmogorovTest(hQCDATM)
            chi2_1 = hQCD.Chi2Test(hQCDAM, 'WW')
            chi2_2 = hQCD.Chi2Test(hQCDATM, 'WW')
            chi2_3 = hQCDAM.Chi2Test(hQCDATM, 'WW')
            oldTitle = hQCDAM.GetTitle()
            hQCDAM.SetTitle('')
            hQCDAM.Draw()
            maxVal = max(hQCDATM.GetMaximum() + hQCDATM.GetBinError(hQCD.GetMaximumBin()), hQCDAM.GetMaximum() + hQCDAM.GetBinError(hQCDAM.GetMaximumBin()))
            hQCDAM.GetYaxis().SetRangeUser(0., maxVal*1.3)
            # hQCD.Draw("SAME")
            hQCDATM.Draw("SAME")
            dummyl = ROOT.TLine()
            dummyl.SetLineColor(0)
            # leg.AddEntry(dummyl, 'KS: ' + str(round(ks1, 2)) + ' #chi^{2}: ' + str(round(chi2_1, 2)), 'l')
            # leg.AddEntry(dummyl, 'KS: ' + str(round(ks2, 2)) + ' #chi^{2}: ' + str(round(chi2_2, 2)), 'l')
            leg.AddEntry(dummyl, 'KS: ' + str(round(ks3, 2)) + ' #chi^{2}: ' + str(round(chi2_3, 2)), 'l')
            leg.Draw()
            padr.cd()
            hr = copy.deepcopy(hQCDAM)
            hr.Divide(hQCDATM)
            hr.GetYaxis().SetNdivisions(4)
            # hr.GetYaxis().SetTitle(oldTitle+'/'+hQCDATM.GetTitle())
            hr.GetYaxis().SetTitle('BG-sub/anti-e-iso')
            hr.GetYaxis().SetTitleSize(0.1)
            hr.GetYaxis().SetTitleOffset(0.5)
            hr.GetXaxis().SetTitle('{xtitle}'.format(xtitle='m_{#tau #tau} [GeV]'))
            hr.GetXaxis().SetTitleSize(0.13)
            hr.GetXaxis().SetTitleOffset(0.9)
            rls = 0.075
            hr.GetYaxis().SetLabelSize(rls)
            hr.GetXaxis().SetLabelSize(rls)
            hr.GetYaxis().SetRangeUser(0.5, 1.5)

            hrup = hr.Clone()
            hrup.SetTitle(hr.GetTitle()+'up')
            hrup.SetMarkerStyle(22)
            hrdown = hr.Clone()
            hrdown.SetTitle(hr.GetTitle()+'down')
            hrdown.SetMarkerStyle(23)
            hrdown.SetMarkerStyle(23)

            for iBin in range(hr.GetNbinsX()):
                if hQCDATM.GetBinContent(iBin+1) == 0. and hQCDAM.GetBinContent(iBin+1) != 0.:
                    hr.SetBinContent(iBin+1, 9999.)
                elif hQCDATM.GetBinContent(iBin+1) == 0. and hQCDAM.GetBinContent(iBin+1) == 0.:
                    hr.SetBinContent(iBin+1, 1.)

                if hr.GetBinContent(iBin + 1) > 1.5:
                    hrup.SetBinContent(iBin+1, 1.4)
                else:
                    hrup.SetBinContent(iBin+1, -9999.)

                if hr.GetBinContent(iBin + 1) < 0.5:
                    hrdown.SetBinContent(iBin+1, 0.6)
                else:
                    hrdown.SetBinContent(iBin+1, -9999.)
                hrdown.SetBinError(iBin+1, 0.)
                hrup.SetBinError(iBin+1, 0.)

            hr.Draw()
            hrup.Draw('same p')
            hrdown.Draw('same p')
            line = ROOT.TLine()
            print 'XMIN', XMIN
            if XMIN != None:
                line.DrawLine(float(XMIN), 1, float(XMAX), 1)
            else:
                line.DrawLine(NBINS[0], 1, NBINS[-1], 1)
            padr.Update()
            can.Print('QCD_comparison'+options.hist+'_'+options.cutName+'.pdf')

        ssign, osign, ssQCD, osQCD = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiEleIsoForQCD=antiEleIsoForQCD)

        # drawOfficial(osQCD, options.blind, channel='TauEle')
        draw(osQCD, options.blind, channel='TauEle')
          
        datacards(osQCD, cutstring, shift, 'eleTau')

        printLowMassInfo = False


        if printLowMassInfo:

            print "Fit 0-60"
            osQCD.ratioTotalHist.weighted.Fit('pol0', '', '', 0., 60.)
            print "Fit Inclusive"
            osQCD.ratioTotalHist.weighted.Fit('pol0')
            datacards(osQCD, cutstring, shift)
            
            print ' --------- KS Test Probability', osQCD.Hist('Data').weighted.KolmogorovTest(osQCD.stack.totalHist.weighted) 
            print ' ------- Chi2 Test Probability', osQCD.Hist('Data').weighted.Chi2Test(osQCD.stack.totalHist.weighted, 'UW') 

            print 'Range: Inclusive'
            print '--- Yield data SS', ssQCD.Hist('Data').Yield()
            print '--- Yield data', osQCD.Hist('Data').Yield()
            print '--- Yield stack', osQCD.stack.totalHist.Yield()
            yieldDataMinusMC = osQCD.Hist('Data').Yield() - osQCD.Hist('Ztt').Yield() - osQCD.Hist('TTJets').Yield()- osQCD.Hist('electroweak').Yield()
            print '--- Yield data - MC / Yield QCD', yieldDataMinusMC/osQCD.Hist('QCD').Yield()
            print '--- Rough error estimate ----', math.sqrt(yieldDataMinusMC+osQCD.Hist('QCD').Yield())/yieldDataMinusMC

            rangePairs = [(0., 40.), (0., 60.), (0., 80.), (40., 80.), (40., 100.),  (60., 100.), (0., 100.), (0., 150.)]
            for pair in rangePairs:
                xmin, xmax = pair
                print 'Range:', xmin, xmax
                print '--- Yield data SS', ssQCD.Hist('Data').Integral(xmin=xmin, xmax=xmax)
                print '--- Yield data', osQCD.Hist('Data').Integral(xmin=xmin, xmax=xmax)
                print '--- Yield stack', osQCD.stack.totalHist.Integral(xmin=xmin, xmax=xmax)
                yieldDataMinusMC = osQCD.Hist('Data').Integral(xmin=xmin, xmax=xmax) - osQCD.Hist('Ztt').Integral(xmin=xmin, xmax=xmax) - osQCD.Hist('TTJets').Integral(xmin=xmin, xmax=xmax)- osQCD.Hist('electroweak').Integral(xmin=xmin, xmax=xmax)
                print '--- Yield data - MC / Yield QCD', yieldDataMinusMC/osQCD.Hist('QCD').Integral(xmin=xmin, xmax=xmax)
                print '--- Rough error estimate ----', math.sqrt(yieldDataMinusMC+osQCD.Hist('QCD').Integral(xmin=xmin, xmax=xmax))/yieldDataMinusMC


