// Standard demo of the ProfileInspector class
/*
StandardProfileInspectorDemo

Author: Kyle Cranmer
date: Dec. 2010

This is a standard demo that can be used with any ROOT file 
prepared in the standard way.  You specify:
 - name for input ROOT file
 - name of workspace inside ROOT file that holds model and data
 - name of ModelConfig that specifies details for calculator tools
 - name of dataset 

With default parameters the macro will attempt to run the 
standard hist2workspace example and read the ROOT file
that it produces.

The actual heart of the demo is only about 10 lines long.

The ProfileInspector plots the conditional maximum likelihood estimate
of each nuisance parameter in the model vs. the parameter of interest.
(aka. profiled value of nuisance parameter vs. parameter of interest)
(aka. best fit nuisance parameter with p.o.i fixed vs. parameter of interest)

*/

#include <iostream>

#include "TAxis.h"
#include "TFile.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TList.h"
#include "TMath.h"
#include "RooWorkspace.h"
#include "RooAbsData.h"
#include "RooRealVar.h"

#include "RooStats/ModelConfig.h"
#include "RooStats/ProfileInspector.h"

using namespace std;
using namespace RooFit;
using namespace RooStats;

void StandardProfileInspectorDemo(const char* infile = "",
		      const char* workspaceName = "combined",
		      const char* modelConfigName = "ModelConfig",
		      const char* dataName = "obsData"){

  /////////////////////////////////////////////////////////////
  // First part is just to access a user-defined file 
  // or create the standard example file if it doesn't exist
  ////////////////////////////////////////////////////////////
  const char* filename = "";
  if (!strcmp(infile,""))
    filename = "results/example_combined_GaussExample_model.root";
  else
    filename = infile;
  // Check if example input file exists
  TFile *file = TFile::Open(filename);

  // if input file was specified byt not found, quit
  if(!file && strcmp(infile,"")){
    cout <<"file not found" << endl;
    return;
  } 

  // if default file not found, try to create it
  if(!file ){
    // Normally this would be run on the command line
    cout <<"will run standard hist2workspace example"<<endl;
    gROOT->ProcessLine(".! prepareHistFactory .");
    gROOT->ProcessLine(".! hist2workspace config/example.xml");
    cout <<"\n\n---------------------"<<endl;
    cout <<"Done creating example input"<<endl;
    cout <<"---------------------\n\n"<<endl;
  }

  // now try to access the file again
  file = TFile::Open(filename);
  if(!file){
    // if it is still not there, then we can't continue
    cout << "Not able to run hist2workspace to create example input" <<endl;
    return;
  }

  
  /////////////////////////////////////////////////////////////
  // Tutorial starts here
  ////////////////////////////////////////////////////////////

  // get the workspace out of the file
  RooWorkspace* w = (RooWorkspace*) file->Get(workspaceName);
  if(!w){
    cout <<"workspace not found" << endl;
    return;
  }

  // get the modelConfig out of the file
  ModelConfig* mc = (ModelConfig*) w->obj(modelConfigName);

  // get the modelConfig out of the file
  RooAbsData* data = w->data(dataName);

  // make sure ingredients are found
  if(!data || !mc){
    w->Print();
    cout << "data or ModelConfig was not found" <<endl;
    return;
  }

  //////////////////////////////////////////////
  // now use the profile inspector
  ProfileInspector p;
  TList* list = p.GetListOfProfilePlots(*data,mc);
  
  // now make plots
  TCanvas* c1 = new TCanvas("c1","ProfileInspectorDemo"); //,800,200);
  c1->Divide(4,4);

  //  const RooArgSet* nuis_params = mc->GetNuisanceParameters();
  
  for(int i=0; i<list->GetSize(); ++i){
    c1->cd(i+1);
    //RooRealVar* nuis = (RooRealVar*) nuis_params->At(i);
    TGraph* graph = (TGraph*) list->At(i);

    std::string y_title = graph->GetYaxis()->GetTitle();
    y_title = "Profiled value of: " + y_title;
    graph->GetYaxis()->SetTitle(y_title.c_str());
    graph->GetYaxis()->SetTitleSize(0.05);
    graph->GetYaxis()->SetTitleOffset(0.8);
    //std::string poi_name = graph->GetXaxis()->GetTitle();
    //graph->GetYaxis()->SetTitle(var->GetName());
    graph->GetXaxis()->SetTitleSize(0.05);
    graph->GetXaxis()->SetTitleOffset(0.8);
    graph->Draw("al");

    //list->At(i)->Draw("al");
  }

  c1->Print("ProfileInspector.eps");
  c1->Print("ProfileInspector.pdf");
  cout << endl;
}


int main() {
  
  StandardProfileInspectorDemo("../results/dilep_combined_allsys_model.root");

}
