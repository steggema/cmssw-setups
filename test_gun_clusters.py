import ROOT

from officialStyle import officialStyle

from Display import deltaR2

ROOT.gROOT.SetBatch(True)
officialStyle(ROOT.gStyle)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetPadLeftMargin(0.18)
ROOT.gStyle.SetPadBottomMargin(0.15)

from DataFormats.FWLite import Events, Handle
handle  = Handle ('std::vector<reco::PFCluster>')
genParticleHandle  = Handle ('std::vector<reco::GenParticle>')

handleNoneFound = Handle('std::vector<reco::PFCluster>')

label = ("particleFlowClusterECALWithTimeUncorrected")
labelNoneFound = ("particleFlowClusterECALWithTimeUncorrected")
labelNoTime = ("particleFlowClusterECALUncorrected")

label = ("particleFlowClusterECAL")
labelNoTime = ("particleFlowClusterECAL")

labelGenParticles = ('genParticles')

handlePFSim = Handle('std::vector<reco::PFSimParticle>')
labelPFSim = ('particleFlowSimParticle')

abgFiles = ['ABG/Job_1/gun_0_photon_and_OOTPU_EB.root',    'ABG/Job_31/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_54/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_77/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_10/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_32/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_55/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_78/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_100/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_33/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_56/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_79/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_11/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_34/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_57/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_8/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_12/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_35/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_58/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_80/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_13/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_36/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_59/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_81/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_14/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_37/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_6/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_82/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_15/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_38/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_60/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_83/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_16/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_39/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_61/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_84/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_17/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_4/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_62/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_85/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_18/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_40/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_63/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_86/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_19/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_41/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_64/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_87/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_2/gun_0_photon_and_OOTPU_EB.root',    'ABG/Job_42/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_65/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_88/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_20/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_43/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_66/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_89/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_21/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_44/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_67/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_9/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_22/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_45/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_68/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_90/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_23/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_46/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_69/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_91/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_24/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_47/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_7/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_92/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_25/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_48/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_70/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_93/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_26/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_49/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_71/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_94/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_27/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_5/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_72/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_95/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_28/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_50/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_73/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_96/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_29/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_51/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_74/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_97/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_3/gun_0_photon_and_OOTPU_EB.root',    'ABG/Job_52/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_75/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_98/gun_0_photon_and_OOTPU_EB.root',
'ABG/Job_30/gun_0_photon_and_OOTPU_EB.root',   'ABG/Job_53/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_76/gun_0_photon_and_OOTPU_EB.root',  'ABG/Job_99/gun_0_photon_and_OOTPU_EB.root']

defFiles = ['Default/Job_1/gun_0_photon_and_OOTPU_EB_defReco.root',    'Default/Job_31/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_54/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_77/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_10/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_32/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_55/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_78/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_100/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_33/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_56/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_79/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_11/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_34/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_57/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_8/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_12/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_35/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_58/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_80/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_13/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_36/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_59/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_81/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_14/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_37/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_6/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_82/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_15/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_38/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_60/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_83/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_16/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_39/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_61/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_84/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_17/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_4/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_62/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_85/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_18/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_40/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_63/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_86/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_19/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_41/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_64/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_87/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_2/gun_0_photon_and_OOTPU_EB_defReco.root',    'Default/Job_42/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_65/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_88/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_20/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_43/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_66/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_89/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_21/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_44/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_67/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_9/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_22/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_45/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_68/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_90/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_23/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_46/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_69/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_91/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_24/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_47/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_7/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_92/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_25/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_48/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_70/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_93/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_26/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_49/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_71/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_94/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_27/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_5/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_72/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_95/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_28/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_50/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_73/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_96/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_29/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_51/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_74/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_97/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_3/gun_0_photon_and_OOTPU_EB_defReco.root',    'Default/Job_52/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_75/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_98/gun_0_photon_and_OOTPU_EB_defReco.root',
'Default/Job_30/gun_0_photon_and_OOTPU_EB_defReco.root',   'Default/Job_53/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_76/gun_0_photon_and_OOTPU_EB_defReco.root',  'Default/Job_99/gun_0_photon_and_OOTPU_EB_defReco.root']


files = [
    # {'file':'/afs/cern.ch/user/s/steggema/work/CMSSW_7_1_0_pre8/src/gun_0_photon.root', 'name':'ABG', 'id':'abg'},
    # {'file':'/afs/cern.ch/user/s/steggema/work/Release/CMSSW_7_1_0_pre5/gun_0_photon_SEED.root', 'name':'Default reco', 'id':'full3d'},
    {'file':abgFiles, 'name':'ABG (40 PU)', 'id':'abg40pu'},
    {'file':defFiles, 'name':'Def. reco (40 PU)', 'id':'def40pu'},
    
]


hists = {}
outFile = ROOT.TFile('out.root', 'RECREATE')

algo = 0

# energySlices = [(0., 2., '0to2'), (2., 4., '2to4'), (4., 6., '4to6'), (6., 8., '6to8'), (8., 10., '8to10'), (10., 15., '10to15'), (15., 20., '15to20')] #(0., 0.5, '0to05'), (0.5, 1., '05to1'), (1., 2., '1to2'), , (10., 20., '10to20')

energySlices = [(0., 5., '0to5'), (5., 10., '5to10'), (10., 20., '10to20'), (20., 55., '20to50'), (50., 100., '50to100'), (100., 1000., '100to1000')]

for f in files:
    print
    print 'Analysing file', f['file']
    outFile.cd()

    hists[f['id']] = []
    hists[f['id']+'smallestT'] = []
    hists[f['id']+'time'] = []
    hists[f['id']+'timeOther'] = []
    hists[f['id']+'sumE'] = []

    events = Events(f['file'])
    print 'N(events)', events.size()

    outFile.cd()

    hist2D = ROOT.TH2F('time_vs_energy'+f['id'], '', 100, 0., 200., 100, -20., 20.,)
    hist2DFracE = ROOT.TH2F('time_vs_energyf'+f['id'], '', 30, -0.5, 1.0, 100, -50., 50.)

    for elow, ehigh, ename in energySlices:
        outFile.cd()
        # hist = ROOT.TH1F('resolution'+f['id']+ename, f['name'], 50, -10., 10.)
        histTime = ROOT.TH1F('time'+f['id']+ename, f['name'], 100, -10., 10.)
        # histTime = ROOT.TH1F('time'+f['id']+ename, f['name'], 50, -25., 25.)
        # histTime = ROOT.TH1F('time'+f['id']+ename, f['name'], 30, -5., 5.)
        histTimeOther = ROOT.TH1F('timeOther'+f['id']+ename, f['name'], 50, -50., 50.)
        histSumE = ROOT.TH1F('sumE'+f['id']+ename, f['name'], 50, -1.01, 3.)
        hist = ROOT.TH1F('relres'+f['id']+ename+'relres', f['name'], 50, -1.01, 1.5)
        # histSumE = ROOT.TH1F('sumE'+f['id']+ename, f['name'], 40, -0.2, 0.2)
        # hist = ROOT.TH1F('relres'+f['id']+ename+'relres', f['name'], 40, -0.2, 0.2)
        histESmallestT = ROOT.TH1F('relres'+f['id']+ename+'smallestT', f['name'], 50, -1.01, 2.)

        hists[f['id']].append(hist)
        hists[f['id']+'smallestT'].append(histESmallestT)
        hists[f['id']+'sumE'].append(histSumE)
        hists[f['id']+'time'].append(histTime)
        hists[f['id']+'timeOther'].append(histTimeOther)

    # clusters = [p for p in clusters if abs(p.eta()) < 1.442] 
    for ev in events:
        if 'notime' in f['id']  or  'timecuts' in f['id']:
            ev.getByLabel(labelNoTime, handle)
        else:
            ev.getByLabel(label, handle)
        ev.getByLabel(labelGenParticles, genParticleHandle)
        clusters = handle.product()
        genParticles = genParticleHandle.product()

        ev.getByLabel(labelPFSim, handlePFSim)
        simParticles = handlePFSim.product()

        for j, energySlice in enumerate(energySlices):
            elow, ehigh, ename = energySlice
            hist = hists[f['id']][j]
            outFile.cd()

            # selGenPs = [p for p in genParticles if abs(p.eta()) > 1.442 and p.energy()>elow and p.energy()<ehigh] 
            for genP in genParticles:
                #find closest cluster
                bestCluster = 0
                minDeltaR2 = 1.0


                # print 'ENERGY', genP.energy(), elow, ehigh
                if genP.energy() < elow or genP.energy() > ehigh:
                    continue

                smallestTime = 999.
                smallestTimeCluster = 0
                for cluster in clusters:
                    if deltaR2(genP.eta(), genP.phi(), cluster.eta(), cluster.phi()) < minDeltaR2:
                        minDeltaR2 = deltaR2(genP.eta(), genP.phi(), cluster.eta(), cluster.phi()) 
                        bestCluster = cluster
                    if abs(cluster.time()) < smallestTime:
                        smallestTime = abs(cluster.time())
                        smallestTimeCluster = cluster


                # clusters = [c for c in clusters if deltaR2(genP.eta(), genP.phi(), c.eta(), c.phi()) < 0.04]
                clusters = [c for c in clusters if deltaR2(genP.eta(), genP.phi(), c.eta(), c.phi()) < 0.09]

                isConversion = False
                for simp in simParticles:
                    if deltaR2(simp.trajectoryPoint(0).momentum().eta(), simp.trajectoryPoint(0).momentum().phi(), genP.eta(), genP.phi()) < 0.25:
                        if simp.pdgCode() == 22 and len(simp.daughterIds()) > 0:
                            isConversion = True
                            break

                if isConversion:
                    continue

                hists[f['id']+'sumE'][j].Fill((sum(c.energy() for c in clusters)-genP.energy())/genP.energy())
                for cluster in clusters:
                    if cluster != bestCluster and cluster.energy() > 1.:
                        histTimeOther.Fill(cluster.time())
                if bestCluster:
                    # hist.Fill(bestCluster.energy()-genP.energy())
                    hists[f['id']+'time'][j].Fill(bestCluster.time())
                    hist2D.Fill(genP.energy(), bestCluster.time())
                    hist2DFracE.Fill((bestCluster.energy()-genP.energy())/genP.energy(), bestCluster.time())
                    hist.Fill((bestCluster.energy()-genP.energy())/genP.energy())
                    # print f['name'], 'Found best cluster, time', bestCluster.time()
                else:
                    print 'No cluster found, gen energy', genP.energy()
                    hist.Fill(-1.)

                if smallestTimeCluster:
                    hists[f['id']+'smallestT'][j].Fill((smallestTimeCluster.energy()-genP.energy())/genP.energy())


    outFile.cd()
    hist2D.Write()
    hist2DFracE.Write()
cv = ROOT.TCanvas()
    

for j, energySlice in enumerate(energySlices):
    

    for label in ['', 'time', 'sumE', 'timeOther', 'smallestT']:
        leg = ROOT.TLegend(0.65, 0.5, 0.88, 0.9)
        elow, ehigh, ename = energySlice
        theHists = [hists[f['id']+label][j] for f in files]
        # import pdb; pdb.set_trace()
        ymax = max(h.GetMaximum() for h in theHists) * 1.3
        for i, h in enumerate(theHists):
            
            h.GetYaxis().SetTitle('Events')
            # h.GetXaxis().SetTitle('cluster energy resolution (GeV)')
            # h.GetXaxis().SetTitle('(E(highest E cluster) - E_{gen})/E_{gen} (GeV)')
            if label == '':
                h.GetXaxis().SetTitle('(E(closest cluster) - E_{gen})/E_{gen} (GeV)')
            if label == 'smallestT':
                h.GetXaxis().SetTitle('(E(minimum time cluster) - E_{gen})/E_{gen} (GeV)')
            if label == 'time':
                h.GetXaxis().SetTitle('Time (closest cluster) (ns)')
            if label == 'timeOther':
                h.GetXaxis().SetTitle('Time (non-closest clusters) (ns)')
            if label == 'sumE':
                h.GetXaxis().SetTitle('(#Sigma energy (all clusters) - E_{gen})/E_{gen} (GeV)')
            
            h.GetYaxis().SetRangeUser(0., ymax)
            h.SetLineColor(i+1)
            if i+1 >= 5:
                h.SetLineColor(i+2) # no yellow
            h.SetLineWidth(4)
            h.SetLineStyle(i+1)
            h.DrawCopy('SAME HIST' if i!=0 else 'HIST')
            print h.GetTitle(),  'Integral', h.Integral(), h.GetRMS()
            leg.AddEntry(h, h.GetTitle(), 'l')

        leg.SetFillStyle(0)
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        leg.SetLineWidth(0)
        leg.Draw()

        cv.Print('plots/gun_cluster_{label}_{ename}.pdf'.format(label=label, ename=ename))

        # print [p.pdgId() for p in gps3]



       # import pdb; pdb.set_trace()
outFile.Close()
