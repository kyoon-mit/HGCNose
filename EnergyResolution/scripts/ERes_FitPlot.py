#!/usr/bin/env python2

# For reference, see: https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html

from ROOT import *
from math import sqrt, sinh
from numpy import zeros, array
import os

# PyConfig.IgnoreCommandLineOptions = True # Don't pass argv into TApplication
gROOT.SetBatch(True) # Enable batch mode (i.e. suppress graphic windows)

# ---- Function definitions ----

def addQuad (*args):
    # type: float, [float, ] -> float
    " Addition in quadrature. "
    ans_squared = 0
    for arg in args:
        ans_squared += arg**2
    return sqrt(ans_squared)
    
    
def getMathEResolution (tgrapherrors, mode='num'):
    # type: TGraphErrors -> dict('key': 'float') (mode='num')
    # type: TGraphErrors -> TGraphErrors (mode='obj')
    # type: TGraphErrors -> (TGraphErrors, dict) (mode='all')
    " Fit dE/E to TGraphErrors. "
    

def fitGaussian (hist, mode='num'):
    # type: TH1 -> TCanvas (mode='draw')
    # type: TH1 -> dict('key': 'float') (mode='data') <- useful for Pandas DataFrame conversion
    # type: TH1 -> (TH1, TF1) (mode='raw')
    # type: TH1 -> (TH1, TF1, dict('key': 'float')) (mode='all')
    " Fit un-normalized Gaussian to histogram. "
    
    Xaxis = hist.GetXaxis()    
    Yaxis = hist.GetYaxis()
    fit = TF1('fit', 'gaus', Xaxis.GetXmin(), Xaxis.GetXmax())
    fitresult = hist.Fit('fit', 'QS')
    
    if mode=='draw':
        c = TCanvas(hist.GetTitle())
        hist.Draw()
        fit.Draw('SAME')
        return c
    
    elif mode=='num':
        n = dict()
        n['scale'], n['scale_error'] = fitresult.Parameter(0), fitresult.ParError(0)
        n['mean'], n['mean_error'] = fitresult.Parameter(1), fitresult.ParError(1)
        n['sigma'], n['sigma_error'] = fitresult.Parameter(2), fitresult.ParError(2)
        return n
    
    elif mode=='raw':
        fit.GetHistogram().GetXaxis().SetTitle(Xaxis.GetTitle())
        fit.GetHistogram().GetYaxis().SetTitle(Yaxis.GetTitle())
        return hist, fit
    
    elif mode=='all':        
        n = dict()
        n['scale'], n['scale_error'] = fitresult.Parameter(0), fitresult.ParError(0)
        n['mean'], n['mean_error'] = fitresult.Parameter(1), fitresult.ParError(1)
        n['sigma'], n['sigma_error'] = fitresult.Parameter(2), fitresult.ParError(2)
        
        return fit, n
        
    else:
        raise Exception(" Correct mode not provided in function \'fitGaussian\'. Valid modes are \'draw\', \'num\', \'raw\', and \'all\'.")
        
        


        
def setTGraphStyle (graph, histtitle, preset):
    # type: (TGraphErrors, str, int) -> None
    " Set style, title, labels, etc. Should add more styles here for readability. "
    
    if preset=='ERes_1':
        graph.SetTitle(histtitle) 
        graph.GetXaxis().SetTitle('E [GeV]')
        graph.GetXaxis().SetLimits(0, 150)
        graph.GetYaxis().SetTitle('#sigma_{E}/E (%)')
        graph.SetMinimum(0)
        graph.SetLineColor(14)
        graph.SetMarkerColor(9)
        graph.SetLineWidth(1)
        graph.SetLineStyle(1)
        graph.SetMarkerSize(1)
        graph.SetMarkerStyle(21)
        
    elif preset=='ERes_2':
        graph.SetTitle(histtitle)
        graph.GetXaxis().SetTitle('E [GeV]')
        graph.GetXaxis().SetLimits(0, 150)
        graph.GetYaxis().SetTitle('#sigma_{E}/E (%)')
        graph.SetMinimum(0)
        graph.SetLineColor(14)
        graph.SetMarkerColor(46)
        graph.SetLineWidth(1)
        graph.SetLineStyle(1)
        graph.SetMarkerSize(1)
        graph.SetMarkerStyle(20)
        
    elif preset=='EMean_1':
        graph.SetTitle(histtitle)
        graph.GetXaxis().SetTitle('p_{T} [GeV/c]')
        graph.GetXaxis().SetLimits(0, 10)
        graph.GetYaxis().SetTitle('E [GeV]')
        graph.SetMinimum(0)
        graph.SetMaximum(150)
        graph.SetLineColor(14)
        graph.SetMarkerColor(9)
        graph.SetLineWidth(1)
        graph.SetLineStyle(1)
        graph.SetMarkerSize(1)
        graph.SetMarkerStyle(21)
        
    elif preset=='EMean_2':
        graph.SetTitle(histtitle)
        graph.GetXaxis().SetTitle('p_{T} [GeV/c]')
        graph.GetXaxis().SetLimits(0, 10)
        graph.GetYaxis().SetTitle('E [GeV]')
        graph.SetMinimum(0)
        graph.SetMaximum(150)
        graph.SetLineColor(14)
        graph.SetMarkerColor(46)
        graph.SetLineWidth(1)
        graph.SetLineStyle(1)
        graph.SetMarkerSize(1)
        graph.SetMarkerStyle(20)
        
    elif preset=='EMean_3':
        graph.SetTitle(histtitle)
        graph.GetXaxis().SetTitle('p_{T} [GeV/c]')
        graph.GetXaxis().SetLimits(0, 10)
        graph.GetYaxis().SetTitle('E [GeV]')
        graph.SetMinimum(0)
        graph.SetMaximum(150)
        graph.SetLineColor(14)
        graph.SetMarkerColor(14)
        graph.SetLineWidth(1)
        graph.SetLineStyle(1)
        graph.SetMarkerSize(2)
        graph.SetMarkerStyle(33)
    
    return

    
def getPlotsEResolutionComprehensive (tuple_filenames, tuple_pt):
    # type: ((str), (str)) -> dict('key': 'TGraph' / 'list(hist)')
    " Plot resolution for different energy values. "
    
    num_points = len(tuple_filenames)

    # Container for truth
    truth_mean_array, truth_mean_error_array = zeros(num_points), zeros(num_points)
    
    # Container for hits method
    hits_draw_gauss = [] # list of histograms
    hits_mean_array, hits_mean_error_array = zeros(num_points), zeros(num_points)
    hits_ERes_array, hits_ERes_error_array = zeros(num_points), zeros(num_points)
    
    # Container for clusters method
    clusters_draw_gauss = [] # list of histograms
    clusters_mean_array, clusters_mean_error_array = zeros(num_points), zeros(num_points)
    clusters_ERes_array, clusters_ERes_error_array = zeros(num_points), zeros(num_points)
    
    
    for i in range(num_points): # Should not do this but put it under a bigger umbrella
    
        filename = tuple_filenames[i]
        pt = tuple_pt[i]
        infile = TFile.Open(filename, 'READ')
        print (filename)
        tree = infile.Get('analysis')
        
        # Get summary histograms
        hits_EDist = tree.Get('EDist_hits')
        clusters_EDist = tree.Get('EDist_clusters_scaler_sum') # typo in original hist name
        truth_EDist = tree.Get('truthEDist')
        
        hits_EDist.SetDirectory(0)
        clusters_EDist.SetDirectory(0)
        truth_EDist.SetDirectory(0)
        
        # Get detailed histograms
        tuple_layer_hits_EDist = zeros(8)
        tuple_layer_clusters_EDist = zeros(8)
        tuple_layer_clusters_num = zeros(8)

        # Modify some TH1 params
        hits_EDist.SetTitle("Energy Distribution (hits, scalar sum): p_{T}=%s" % (pt))
        hits_EDist.GetXaxis().SetTitle("E [GeV]")
        hits_EDist.GetYaxis().SetTitle("count")
        
        clusters_EDist.SetTitle("Energy Distribution (clusters, scalar sum): p_{T}=%s" % (pt))
        clusters_EDist.GetXaxis().SetTitle("E [GeV]")
        clusters_EDist.GetYaxis().SetTitle("count")

        # For truths
        truth_stats = fitGaussian(truth_EDist, mode='num')
                
        truth_mean_array[i] = truth_stats['mean']
        truth_mean_error_array[i] = truth_stats['mean_error']
        
        # For hits
        hits_fit, hits_stats = fitGaussian(hits_EDist, mode='all')
        hits_sigma, hits_sigma_error = hits_stats['sigma'], hits_stats['sigma_error']
        hits_mean, hits_mean_error = hits_stats['mean'], hits_stats['mean_error']
        
        hits_ERes_array[i] = hits_sigma/hits_mean
        hits_ERes_error_array[i] = hits_ERes_array[i] * addQuad(hits_sigma_error/hits_sigma, hits_mean_error/hits_mean)
        
        hits_draw_gauss.append((hits_EDist, hits_fit))
        
        hits_mean_array[i] = hits_mean
        hits_mean_error_array[i] = hits_mean_error
        
        # For clusters
        clusters_fit, clusters_stats = fitGaussian(clusters_EDist, mode='all')
        clusters_sigma, clusters_sigma_error = clusters_stats['sigma'], clusters_stats['sigma_error']
        clusters_mean, clusters_mean_error = clusters_stats['mean'], clusters_stats['mean_error']

        clusters_draw_gauss.append((clusters_EDist, clusters_fit))
        
        clusters_ERes_array[i] = clusters_sigma/clusters_mean
        clusters_ERes_error_array[i] = (clusters_sigma/clusters_mean)*addQuad(clusters_sigma_error/clusters_sigma, clusters_mean_error/clusters_mean)
        
        clusters_mean_array[i] = clusters_mean
        clusters_mean_error_array[i] = clusters_mean_error
        
        
    # Set dictionary for containing the return plots
    dict_plots = dict()
    
    # pt plots
    dict_plots['hits_EDist_draw_list'] = hits_draw_gauss
    dict_plots['clusters_EDist_draw_list'] = clusters_draw_gauss
    
    # Energy Resolution Plots
    dict_plots['hits_ERes_graph'] = TGraphErrors(num_points, hits_mean_array, hits_ERes_array*100, hits_mean_error_array, hits_ERes_error_array*100)
    dict_plots['clusters_ERes_graph'] = TGraphErrors(num_points, clusters_mean_array, clusters_ERes_array*100, clusters_mean_error_array, clusters_ERes_error_array*100)
    
    # Mean Energy Plots
    array_pt = array([float(i) for i in tuple_pt])
    dict_plots['hits_EMean_graph'] = TGraph(num_points, array_pt, hits_mean_array)
    dict_plots['clusters_EMean_graph'] = TGraph(num_points, array_pt, clusters_mean_array)
    dict_plots['truth_EMean_graph'] = TGraph(num_points, array_pt, truth_mean_array)
    
    return dict_plots
    

def plotPerPT (hits_EDist, hits_fit, clusters_EDist, clusters_fit, pt, TOP_DIR):
    # (TH1, TF1, TH1, TF1) -> None
    " Plot per pt "
    
    if not os.path.exists(TOP_DIR + '/pt_plots'):
        os.makedirs(TOP_DIR + '/pt_plots')
    
    ch = TCanvas()
    ch.cd()
    hits_EDist.Draw()
    hits_fit.Draw('SAME')
    ch.SaveAs(TOP_DIR + '/pt_plots/hits_EDist_pt%s.png' % (pt))
    
    cc = TCanvas()
    cc.cd()
    clusters_EDist.Draw()
    clusters_fit.Draw('SAME')
    cc.SaveAs(TOP_DIR + '/pt_plots/clusters_EDist_pt%s.png' % (pt))
    
    return
    

def plotEResolutionFit (hits_ERes, clusters_ERes, TOP_DIR):
    # (TH1, TH1) -> None
    " Plot energy resolution + fit"
        
    if not os.path.exists(TOP_DIR + '/ERes_plots'):
        os.makedirs(TOP_DIR + '/ERes_plots')
        
    # Set style
    group = 1 # group will later disappear
    
    setTGraphStyle(hits_ERes, "Energy Resolution (hits): HGCNose, single #gamma, |#eta| = 3.5", preset='ERes_%d' % (group))
    setTGraphStyle(clusters_ERes, "Energy Resolution (clusters): HGCNose, single #gamma, |#eta| = 3.5", preset='ERes_%d' % (group))
        
    c1 = TCanvas("ERes_hits_TGraphErrors")
    hits_ERes.Draw('AP')
    
    c2 = TCanvas("ERes_clusters_TGraphErrors")
    c2.cd()
    clusters_ERes.Draw('AP')
    
    c1.SaveAs(TOP_DIR + '/ERes_plots/EResolution_hits.png')
    c2.SaveAs(TOP_DIR + '/ERes_plots/EResolution_clusters.png')
    
    return
    
    
def plotEMean (hits_EMean, clusters_EMean, truth_EMean, TOP_DIR):
    # (TH1, TH1) -> None
    " Plot mean energy per pt "
        
    if not os.path.exists(TOP_DIR + '/EMean_plots'):
        os.makedirs(TOP_DIR + '/EMean_plots')
        
    # Set style
    group = 1 # group will later disappear
    
    
    setTGraphStyle(hits_EMean, "hits", preset='EMean_1')
    setTGraphStyle(clusters_EMean, "clusters", preset='EMean_2')
    setTGraphStyle(truth_EMean, "truth", preset='EMean_3')
        
    c = TCanvas("EMean_TMultigraph")
    mg = TMultiGraph()
    mg.Add(truth_EMean)
    mg.Add(hits_EMean)
    mg.Add(clusters_EMean)
    mg.Draw('ALP')
    
    mg.SetTitle("Mean Energy Comparison")
    mg.GetXaxis().SetTitle('p_{T} [GeV/c]')
    mg.GetXaxis().SetLimits(0, 10)
    mg.GetYaxis().SetTitle('E [GeV]')
    mg.SetMinimum(0)
    mg.SetMaximum(150)
    
    c.Update()
    c.BuildLegend()
    c.SaveAs(TOP_DIR + '/EMean_plots/EMean_compare.png')
    
    return
    

        
# ---- Main -----

def main():
    # File names
    tuple_pt = ('.33', '.66', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    tuple_filenames = tuple('output/ERes_pt%s.root' % (i) for i in tuple_pt)
        
    # Get the comprehensive dictionary of plots
    dict_plots = getPlotsEResolutionComprehensive(tuple_filenames, tuple_pt)
    
    # Save directory
    TOP_DIR = '/home/kyoon/CMSSW_11_1_0_pre7_RECHIT/src/HGCNose/EnergyResolution/plots'
    
    # Save Energy Distribution TCanvas that shows fitted histograms
    for i in range(len(tuple_pt)):
        plotPerPT (dict_plots['hits_EDist_draw_list'][i][0], dict_plots['hits_EDist_draw_list'][i][1], dict_plots['clusters_EDist_draw_list'][i][0], dict_plots['clusters_EDist_draw_list'][i][1], tuple_pt[i], TOP_DIR)
    
    # Save Energy Resolution plots
    plotEResolutionFit (dict_plots['hits_ERes_graph'], dict_plots['clusters_ERes_graph'], TOP_DIR)

    # Save Mean Energy plots
    plotEMean (dict_plots['hits_EMean_graph'], dict_plots['clusters_EMean_graph'], dict_plots['truth_EMean_graph'], TOP_DIR)


if __name__=='__main__':
    main()
