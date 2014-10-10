import ROOT

from officialStyle import officialStyle

ROOT.gROOT.SetBatch(True)
officialStyle(ROOT.gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetPadLeftMargin(0.18)
ROOT.gStyle.SetPadBottomMargin(0.15)

from DataFormats.FWLite import Events, Handle
handle  = Handle ('std::vector<reco::GsfElectron>')
label = ("gsfElectrons")

#RR
handleRR  = Handle ('std::vector<reco::GsfElectron>')
labelRR = ("gedGsfElectrons")

files = [
    {'file':'/afs/cern.ch/user/s/steggema/work/PF71X/recoTestData_noTime.root', 'name':'No time', 'id':'notime'},
    {'file':'/afs/cern.ch/user/s/steggema/work/PF71X/recoTestData.root', 'name':'3D: Default', 'id':'def'},
    {'file':'/afs/cern.ch/user/s/steggema/work/PF71X/recoTestData_timeCuts.root', 'name':'Time cuts', 'id':'tcuts'},

    
    # {'file':'/afs/cern.ch/user/s/steggema/work/Release/CMSSW_7_1_0_pre5/reco_jan.root', 'name':'2#sigma nb.', 'id':'twosigma'},
    # # {'file':'/afs/cern.ch/user/s/steggema/work/Release/CMSSW_7_1_0_pre5/reco_jan_3sigma.root', 'name':'3#sigma nb.', 'id':'threesigma'},
    # {'file':'/afs/cern.ch/user/s/steggema/work/Release/CMSSW_7_1_0_pre5/reco_michalis.root', 'name':'Tight nb.', 'id':'adhoc'},
    # {'file':'/afs/cern.ch/user/s/steggema/work/Release/CMSSW_7_1_0_pre5/reco_jan_3sigma.root', 'name':'25 ns comp', 'id':'bx25'},

]

hists = []
outFile = ROOT.TFile('out.root', 'RECREATE')

algo = 1

for f in files:
    print
    print 'Analysing file', f['file']
    outFile.cd()
    hist = ROOT.TH1F('zmass'+f['id'], f['name'] + ' OR', 20, 50., 120.)
    hist.Sumw2()

    histRR = ROOT.TH1F('zmass'+f['id']+'RR', f['name'] + ' Re-reco', 20, 50., 120.)
    histRR.Sumw2()

    # hists.append(hist)
    hists.append(histRR)

    events = Events(f['file'])
    print 'N(events)', events.size()

    for ev in events:
        ev.getByLabel(label, handle)
        ev.getByLabel(labelRR, handleRR)
        electrons = handle.product()
        electronsRR = handleRR.product()
        electrons = [p for p in electrons if p.pt()>20.]
        # electronsRR = [p for p in electrons if p.p4(algo).pt()>20.]
        electronsRR = [p for p in electronsRR if p.pt()>20.]

        if len(electrons) != len(electronsRR):
            print 'Different N ele',  len(electrons), len(electronsRR)

        # if len(electrons) > 0 and len(electronsRR) > 0:
        #     e1 = electrons[0]
        #     print e1.pt(), e1.eta(), e1.phi()
        #     e2 = electronsRR[0]
        #     print e2.pt(), e2.eta(), e2.phi()

        if len(electrons) >= 2:
            zP4 = electrons[0].p4(algo)
            zP4 += electrons[1].p4(algo)
            # print higgsP4.mass(),
            hist.Fill(zP4.mass())
            # print 'Z mass classic', zP4.mass()

        if len(electronsRR) >= 2:
            zP4RR = electronsRR[0].p4(algo)
            zP4RR += electronsRR[1].p4(algo)
            # print higgsP4.mass(),
            histRR.Fill(zP4RR.mass())
            # print 'Z mass re-reco', zP4RR.mass()


    for h in [hist, histRR]: 
        print h.GetName()    
        print 'Mean', h.GetMean()
        print 'RMS', h.GetRMS(), '+/-', h.GetRMSError()
        print 'Integral', h.Integral()

outFile.cd()
cv = ROOT.TCanvas()
ymax = max(h.GetMaximum() for h in hists) * 1.3

leg = ROOT.TLegend(0.65, 0.5, 0.88, 0.9)
for i, h in enumerate(hists):
    h.GetYaxis().SetTitle('Events')
    h.GetXaxis().SetTitle('di-electron mass (GeV)')
    
    h.GetYaxis().SetRangeUser(0., ymax)
    h.SetLineColor(i+1)
    if i+1 >= 5:
        h.SetLineColor(i+2) # no yellow
    h.SetLineWidth(3)
    h.SetLineStyle(i+1)
    h.DrawCopy('SAME HIST' if i != 0 else 'HIST')
    leg.AddEntry(h, h.GetTitle(), 'l')

leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.SetLineWidth(0)
leg.Draw()

cv.Print('zmass.pdf')

        # print [p.pdgId() for p in gps3]



       # import pdb; pdb.set_trace()
