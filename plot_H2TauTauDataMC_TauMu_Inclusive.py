import imp
import math
import copy
import time
import re
import os
import ROOT

from CMGTools.H2TauTau.proto.HistogramSet import histogramSet
from CMGTools.H2TauTau.proto.plotter.H2TauTauDataMC import H2TauTauDataMC
from CMGTools.H2TauTau.proto.plotter.prepareComponents import prepareComponents
from CMGTools.H2TauTau.proto.plotter.rootutils import *
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import *
from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer
from CMGTools.H2TauTau.proto.plotter.titles import xtitles
from CMGTools.H2TauTau.proto.plotter.blind import blind
from CMGTools.H2TauTau.proto.plotter.plotmod import *
from CMGTools.H2TauTau.proto.plotter.datacards import *
from CMGTools.H2TauTau.proto.plotter.embed import setupEmbedding as setupEmbedding
from CMGTools.H2TauTau.proto.plotter.plotinfo import plots_All as plots_All
# from CMGTools.RootTools.Style import *
from ROOT import kPink, TH1, TPaveText, TPad



cp = copy.deepcopy
EWK = 'WJets'

    
NBINS = 100
XMIN  = 0
XMAX  = 200


def printDataVsQCDInfo(osQCD, ssQCD):
    print "Fit 0-60"
    osQCD.ratioTotalHist.weighted.Fit('pol0', '', '', 0., 60.)
    print "Fit Inclusive"
    osQCD.ratioTotalHist.weighted.Fit('pol0')
        
    dataHist = osQCD.Hist('Data')
    totalMC = osQCD.stack.totalHist
    qcdHist = osQCD.Hist('QCD')

    ssDataHist = ssQCD.Hist('Data')

    print ' --------- KS Test Probability', dataHist.weighted.KolmogorovTest(totalMC.weighted) 
    print ' ------- Chi2 Test Probability', dataHist.weighted.Chi2Test(totalMC.weighted, 'UW') 

    print 'Range: Inclusive'
    print '--- Yield data SS', ssDataHist.Yield()
    print '--- Yield data', dataHist.Yield()
    print '--- Yield stack', totalMC.Yield()
    yieldDataMinusMC = dataHist.Yield() - osQCD.Hist('Ztt').Yield() - osQCD.Hist('TTJets').Yield()- osQCD.Hist('electroweak').Yield()
    print '--- Yield data - MC / Yield QCD', yieldDataMinusMC/qcdHist.Yield()
    print '--- Rough error estimate ----', math.sqrt(yieldDataMinusMC+qcdHist.Yield())/yieldDataMinusMC

    rangePairs = [(0., 40.), (0., 60.), (0., 80.), (40., 80.), (40., 100.),  (60., 100.), (0., 100.), (0., 150.)]
    for pair in rangePairs:
        xmin, xmax = pair
        print 'Range:', xmin, xmax
        print '--- Yield data SS', ssDataHist.Integral(xmin=xmin, xmax=xmax)
        print '--- Yield data', dataHist.Integral(xmin=xmin, xmax=xmax)
        print '--- Yield stack', totalMC.Integral(xmin=xmin, xmax=xmax)
        yieldDataMinusMC = dataHist.Integral(xmin=xmin, xmax=xmax) - osQCD.Hist('Ztt').Integral(xmin=xmin, xmax=xmax) - osQCD.Hist('TTJets').Integral(xmin=xmin, xmax=xmax)- osQCD.Hist('electroweak').Integral(xmin=xmin, xmax=xmax)
        print '--- Yield data - MC / Yield QCD', yieldDataMinusMC/qcdHist.Integral(xmin=xmin, xmax=xmax)
        print '--- Rough error estimate ----', math.sqrt(yieldDataMinusMC+qcdHist.Integral(xmin=xmin, xmax=xmax))/yieldDataMinusMC




def replaceShapeInclusive(plot, var, anaDir,
                          comp, weights, 
                          cut, weight,
                          embed, shift):
    '''Replace WJets with the shape obtained using a relaxed tau iso'''
    # This cut is outdated!
    # cut = cut.replace('l1_looseMvaIso>0.5', 'l1_rawMvaIso>0.5')

    print 'WARNING, relaxing W+Jets shape, NOT STUDIED!!!'
    cut = cut.replace('l1_threeHitIso<1.5', 'l1_threeHitIso<10.0')

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
              VVgroup=None, antiMuIsoForQCD=False, antiTauAntiMuIsoForQCD=False, 
              subtractBGForQCDShape=False, embedForSS=False):
    
    print 'making the plot:', var, 'cut', cut

    oscut = cut+' && diTau_charge==0'
    osign = H2TauTauDataMC(var, anaDir,
                           selComps, weights, nbins, xmin, xmax,
                           cut=oscut, weight=weight, shift=shift,
                           embed=embed)
    osign.Hist(EWK).Scale( wJetScaleOS ) # * w_mt_ratio / w_mt_ratio_os )

    print 'USING wJetScaleOS', wJetScaleOS
    
    if cut.find('mt<')!=-1:
        print 'correcting high->low mT extrapolation factor, OS', w_mt_ratio / w_mt_ratio_os
        osign.Hist(EWK).Scale( w_mt_ratio / w_mt_ratio_os )
    if replaceW:
        osign = replaceShapeInclusive(osign, var, anaDir,
                                      selComps['WJets'], weights, 
                                      oscut, weight,
                                      embed, shift)
    sscut = cut+' && diTau_charge!=0'
    if not embedForSS and embed:
        print 'WARNING, as opposed to old default, not using embedded samples for SS region, but only for OS'
    ssign = H2TauTauDataMC(var, anaDir,
                           selComps, weights, nbins, xmin, xmax,
                           cut=sscut, weight=weight, shift=shift,
                           embed=embedForSS)
    ssign.Hist(EWK).Scale( wJetScaleSS )
    if cut.find('mt<')!=-1:
        if w_mt_ratio_ss > 0.:
            print 'correcting high->low mT extrapolation factor, SS', w_mt_ratio / w_mt_ratio_ss
            ssign.Hist(EWK).Scale( w_mt_ratio / w_mt_ratio_ss  )
        else:
            print 'WARNING! Not correcting W mT ratio from SS to OS region: No events in SS high mT'
    if replaceW:
        ssign = replaceShapeInclusive(ssign, var, anaDir,
                                      selComps['WJets'], weights, 
                                      sscut, weight,
                                      embed, shift)
    if VVgroup:
        ssign.Group('VV',VVgroup)
        osign.Group('VV',VVgroup)
    
    ssQCD, osQCD = getQCD( ssign, osign, 'Data', VVgroup, subtractBGForShape=subtractBGForQCDShape)
    if antiMuIsoForQCD:
        print 'WARNING INVERTING MU ISO FOR QCD SHAPE'
        # replace QCD with a shape obtained from data in an anti-iso control region
        qcd_yield = osQCD.Hist('QCD').Integral()
        
        # sscut_qcdshape = cut.replace('l2_relIso05<0.1','l2_relIso05>0.2 && l2_relIso05<0.5') + ' && diTau_charge!=0' 
        sscut_qcdshape = cut.replace('l2_relIso05<0.1','l2_relIso05>0.2 && l2_relIso05<0.5') + ' && diTau_charge!=0'
        # Do not invert tau iso at the same time
        #.replace('l1_looseMvaIso>0.5', 'l1_rawMvaIso>0.7') 
        ssign_qcdshape = H2TauTauDataMC(var, anaDir,
                                        selComps, weights, nbins, xmin, xmax,
                                        cut=sscut_qcdshape, weight=weight,
                                        embed=embed)
        qcd_shape = copy.deepcopy( ssign_qcdshape.Hist('Data') )    
        qcd_shape.Normalize()
        qcd_shape.Scale(qcd_yield)
        # qcd_shape.Scale( qcd_yield )
        old_qcd_shape = osQCD.Hist('QCD')
        osQCD.old_qcd_shape = copy.deepcopy(old_qcd_shape)
        osQCD.Replace('QCD', qcd_shape)
    elif antiTauAntiMuIsoForQCD:
        print 'WARNING INVERTING TAU AND MU ISO FOR QCD SHAPE'
        # replace QCD with a shape obtained from data in an anti-iso control region
        qcd_yield = osQCD.Hist('QCD').Integral()
        
        # sscut_qcdshape = cut.replace('l2_relIso05<0.1','l2_relIso05>0.2 && l2_relIso05<0.5') + ' && diTau_charge!=0' 
        sscut_qcdshape = cut.replace('l2_relIso05<0.1','l2_relIso05>0.2 && l2_relIso05<0.5').replace('l1_threeHitIso<1.5', 'l1_threeHitIso>1.5 && l1_threeHitIso<10.') + ' && diTau_charge!=0'

        ssign_qcdshape = H2TauTauDataMC(var, anaDir,
                                        selComps, weights, nbins, xmin, xmax,
                                        cut=sscut_qcdshape, weight=weight,
                                        embed=embed)
        qcd_shape = copy.deepcopy( ssign_qcdshape.Hist('Data') )    
        qcd_shape.Normalize()
        qcd_shape.Scale(qcd_yield)
        # qcd_shape.Scale( qcd_yield )
        old_qcd_shape = osQCD.Hist('QCD')
        osQCD.old_qcd_shape = copy.deepcopy(old_qcd_shape)
        osQCD.Replace('QCD', qcd_shape)

    # osQCD.Group('VV', ['WW','WZ','ZZ'])
    osQCD.Group('electroweak', ['WJets', 'Ztt_ZL', 'Ztt_ZJ','VV'])
    osQCD.Group('Higgs 125', ['HiggsVBF125', 'HiggsGGH125', 'HiggsVH125'])
    return ssign, osign, ssQCD, osQCD


def drawAll(cut, plots, embed=True, blind=True):
    '''See plotinfo for more information'''
    for name, plot in plots.items():
        print plot.var
        print '----------------', plot.xmin, plot.xmax, plot.nbins
        print fwss, fwos
        ss, osign, ssQ, osQ = makePlot( plot.var, anaDir,
                                     selComps, weights, fwss, fwos,
                                     w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, 
                                     plot.nbins, plot.xmin, plot.xmax,
                                     cut, weight=weight, embed=embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=antiMuIsoForQCD)
        #makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=antiMuIsoForQCD)

        outDir = 'Summer13StackPlotsOSSumPt/'+options.cutName+'/'
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        if name != plot.var:
            outDir += name + '_'
        # drawOfficial(osQ, blind, plotprefix=outDir)
        draw(osQ, blind, plotprefix=outDir)
        osQ.ratioTotalHist.weighted.Fit('pol0', '', '', 0., 60.)
        plot.ssign = cp(ss)
        plot.osign = cp(osign)
        plot.ssQCD = cp(ssQ)
        plot.osQCD = cp(osQ)
        # time.sleep(1)


def handleW( anaDir, selComps, weights,
             cut, weight, embed, VVgroup, nbins=50, highMTMin=70., highMTMax=1070,
             lowMTMax=20.):
    print 'HANDLING W'
    cut = cut.replace('mt<30', '1')
    cut = cut.replace('mt<20', '1')
    fwss, fwos, ss, os = plot_W(
        anaDir, selComps, weights,
        nbins, highMTMin, highMTMax, cut,
        weight=weight, embed=embed,
        VVgroup = VVgroup)

    w_mt_ratio_ss = w_lowHighMTRatio('mt', anaDir, selComps['WJets'], weights, cut, weight, lowMTMax, highMTMin, highMTMax, 'diTau_charge!=0');
    w_mt_ratio_os = w_lowHighMTRatio('mt', anaDir, selComps['WJets'], weights, cut, weight, lowMTMax, highMTMin, highMTMax, 'diTau_charge==0');
    w_mt_ratio = w_lowHighMTRatio('mt', anaDir, selComps['WJets'], weights, cut, weight, lowMTMax, highMTMin, highMTMax, '1');

    print 'FWSS, FWOS', fwss, fwos
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
    parser.add_option("-N", "--cutName", 
                      dest="cutName", 
                      help="name to prepend for output plots.",
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
    parser.add_option("-a", "--all", 
                      dest="allPlots", 
                      help="All plots.",
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

    isVBF = cutstring.find('Xcat_VBF')!=-1 
    antiMuIsoForQCD = cutstring.find('l1_pt>40')!=-1 or cutstring.find('Xcat_J1')!=-1 or isVBF or cutstring.find('Xcat_J0_mediumX')!=-1 or cutstring.find('Xcat_J0_highX')!=-1
    antiMuRlxTauIsoForQCD = cutstring.find('Xcat_J1_high_mediumhiggsX')!=-1 # Needs to take precedence in code above

    options.cut = replaceCategories(options.cut, categories) 

    dataName = 'Data'
    weight='weight'
    replaceW = False
    
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
    selComps, weights, zComps = prepareComponents(anaDir, cfg.config, aliases, options.embed, 'TauMu', options.higgs)

    print 'SELECTED COMPONENTS', selComps
    print 'WEIGHTS', [weights[w].GetWeight() for w in weights]
    print 'Z COMPONENTS', zComps

    # can, pad, padr = buildCanvas()
    ocan = buildCanvasOfficial()
    

    makeQCDIsoPlots = True

    # fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio = handleW(
    #     anaDir, selComps, weights,
    #     options.cut, weight, options.embed, cfg.VVgroup
    #     )
    if options.embed:
        print 'WARNING, not using embedded samples for W estimation in sideband'
    fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio = handleW(
        anaDir, selComps, weights,
        options.cut, weight, False, cfg.VVgroup
        )

    if options.allPlots:
        # plots_'l1_decayMode':PlotInfo('l1_decayMode', 15, -0.5, 14.5),
        drawAll(options.cut, plots_All, options.embed, options.blind)
    else:
        if makeQCDIsoPlots:
            ssign, osign, ssQCD, osQCD = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=False)

            # ssignAM, osignAM, ssQCDAM, osQCDAM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=True)
            ssignAM, osignAM, ssQCDAM, osQCDAM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=False, subtractBGForQCDShape=True)


            # ssignATM, osignATM, ssQCDATM, osQCDATM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiTauAntiMuIsoForQCD=True)
            ssignATM, osignATM, ssQCDATM, osQCDATM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=True)

            # ssignATM, osignATM, ssQCDATM, osQCDATM = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=False, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=False)

            can = buildCanvasOfficial()
            hQCD = osQCD.Hist('QCD').weighted.Clone()
            hQCD.GetXaxis().SetTitle('m_{#tau #tau} [GeV]')
            hQCD.GetYaxis().SetTitle('Events')
            hQCD.SetFillColor(0)
            hQCD.SetLineColor(hQCD.GetMarkerColor())
            hQCD.SetTitle('QCD SS embedded')
            hQCD.Draw()
            # hQCDAM = osQCDAM.Hist('QCD').weighted
            # hQCDAM.SetTitle('QCD SS #mu')

            hQCDAM = osQCDAM.Hist('QCD').weighted
            hQCDAM.SetTitle('QCD SS BG-subtracted')
            
            hQCDAM.SetMarkerColor(1)
            hQCDAM.SetLineColor(1)
            hQCDAM.SetFillColor(0)
            hQCDAM.Draw("SAME")

            hQCDATM = osQCDATM.Hist('QCD').weighted
            # hQCDATM.SetTitle('QCD SS #mu #tau')
            hQCDATM.SetTitle('QCD SS #mu')
            # hQCDATM.SetTitle('QCD SS')
            hQCDATM.SetMarkerColor(2)
            hQCDATM.SetLineColor(2)
            hQCDATM.SetFillColor(0)
            hQCDATM.Draw("SAME")
            leg = can.BuildLegend()
            ks1 = hQCD.KolmogorovTest(hQCDAM)
            ks2 = hQCD.KolmogorovTest(hQCDATM)
            ks3 = hQCDAM.KolmogorovTest(hQCDATM)
            chi2_1 = hQCD.Chi2Test(hQCDAM, 'WW')
            chi2_2 = hQCD.Chi2Test(hQCDATM, 'WW')
            chi2_3 = hQCDAM.Chi2Test(hQCDATM, 'WW')
            leg.AddEntry(None, 'KS: ' + str(round(ks1, 2)) + ' #chi^{2}: ' + str(round(chi2_1, 2)))
            leg.AddEntry(None, 'KS: ' + str(round(ks2, 2)) + ' #chi^{2}: ' + str(round(chi2_2, 2)))
            leg.AddEntry(None, 'KS: ' + str(round(ks3, 2)) + ' #chi^{2}: ' + str(round(chi2_3, 2)))
            leg.Draw()
            can.Print('QCD_comparison.pdf')
        else:
            ssign, osign, ssQCD, osQCD = makePlot( options.hist, anaDir, selComps, weights, fwss, fwos, w_mt_ratio_ss, w_mt_ratio_os, w_mt_ratio, NBINS, XMIN, XMAX, options.cut, weight=weight, embed=options.embed, shift=shift, replaceW=replaceW, VVgroup=cfg.VVgroup, antiMuIsoForQCD=antiMuIsoForQCD)

        drawOfficial(osQCD, options.blind)
        draw(osQCD, options.blind)
        datacards(osQCD, cutstring, shift)


        # printDataVsQCDInfo(osQCD, ssQCD)
        
        