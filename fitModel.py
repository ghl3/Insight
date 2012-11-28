
import sys
sys.argv.append( '-b' )
import ROOT
from ROOT import TFile, RooWorkspace

from common import color_map

from PlotMaker.style.AtlasStyle import AtlasStyle

#from makePlots import hist_name, top_plot_maker


def get_model():

    input_file = TFile("results/dilep_combined_allsys_model.root")
    wspace = input_file.Get("combined")
    model = wspace.pdf("simPdf")
    data = wspace.data("obsData")
    poi = wspace.var("TopCrossSection")

    return (wspace, model, data, poi)
    

def main():

    style = AtlasStyle()
    ROOT.gROOT.SetStyle( style.GetName() )

    # Open the file and gather the necessary objects

    (wspace, model, data, poi) = get_model()

    # Graph and fit
    model.graphVizTree("model.dot")
    result = model.fitTo( data, ROOT.RooCmdArg("Save", True) )
    corr_matrix = result.correlationMatrix()
    cov_matrix = result.covarianceMatrix()

    # Make the profile likelihood curve
    nll = model.createNLL(data)
    profile = nll.createProfile(ROOT.RooArgSet(poi))       

    # Draw and Save the Profile Likelihood
    poi.setRange(0.4, 1.5)
    frame = poi.frame()
    ROOT.RooStats.HistFactory.FormatFrameForLikelihood(frame)
    nll.plotOn(frame, ROOT.RooCmdArg("ShiftToZero",True), 
               ROOT.RooCmdArg("LineColor",ROOT.kRed), 
               ROOT.RooCmdArg("LineStyle",ROOT.kDashed) )
    profile.plotOn(frame);
    frame.SetMinimum(0);
    frame.SetMaximum(2.);
    ProfileLikelihoodCanvas = ROOT.TCanvas("canvas", "", 800,600)
    frame.Draw("goff");
    ProfileLikelihoodCanvas.Print("Plots/ProfileLikelihood.pdf")

    # Print the results
    nav = ROOT.RooStats.HistFactory.HistFactoryNavigation(model, data)
    nav.PrintParameters()
    nav.PrintModelAndData(data)

    # Set the colors
    for sample, color in color_map.iteritems():
        nav.SetColor(sample, color)

    # Make some fitted plots
    canvas = ROOT.TCanvas("Canvas", "")

    for channel in ['ee', 'emu', 'mumu']:
        nav.DrawChannel(channel, data, True)
        canvas.Print("Plots/%s_fitted.pdf" % channel)

    print "Covariance Matrix: "
    cov_matrix.Print("V")

    print "Correlation Matrix: "
    corr_matrix.Print("V")

    return nav

if __name__ == "__main__":
    main()
    
