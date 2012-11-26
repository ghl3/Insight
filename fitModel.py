

import ROOT
from ROOT import TFile, RooWorkspace
#from ROOT.RooStats.HistFactory import HistFactoryNavigation


def main():

    input_file = TFile("results/dilep_combined_allsys_model.root")
    
    wspace = input_file.Get("combined")
    model = wspace.pdf("simPdf")
    data = wspace.data("obsData")
    
    model.fitTo( data )


    # Print the results
    nav = ROOT.RooStats.HistFactory.HistFactoryNavigation(model, data)
    nav.PrintParameters()
    nav.PrintModelAndData(data)
    


if __name__ == "__main__":
    main()
    
