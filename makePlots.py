#!/usr/bin/env python

import sys
sys.argv.append( '-b' )
import ROOT

from PlotMaker.PlotMaker import PlotMaker


def hist_name(channel, systematic="default", name="Jet_N_0_6i_20GeV"):
    """ A quick helper to return the name of a histogram
    
    This name is based on the format of the current ROOT file
    """
    return "%s/{{Sample}}/%s/%s" % (channel, systematic, name)


def main():

    pm = PlotMaker("PlotMaker", "Plot Maker")
    pm.SetLegendBoundaries( .75, .65, .95, .90 )

    input_file = "dilepton2010_modified/data/TopHistograms.root"

    pm.AddDataSample(files=input_file, name="Data", title="data10 (7TeV)")

    pm.AddMCSample(files=input_file, name="tbart", title="t #bar{t}", signal=True, Scale=200)
    pm.AddMCSample(files=input_file, name="Zll", title="Z #rightarrow ll", color=37)
    pm.AddMCSample(files=input_file, name="W", title="W", color=38)
    pm.AddMCSample(files=input_file, name="Wbb", title="W #rightarrow bb", color=39)
    pm.AddMCSample(files=input_file, name="Ztautau", title="Z #rightarrow #tau #tau", color=40)
    pm.AddMCSample(files=input_file, name="Diboson", title="Diboson", color=41)
    pm.AddMCSample(files=input_file, name="SingleTop", title="Single Top", color=42)
    pm.AddMCSample(files=input_file, name="Fake", title="Fakes", color=43)

    # Make the nominal MC/Data comparisons
    for channel in ['ee', 'emu', 'mumu']:
        input_name = hist_name(channel)
        output_name = input_name.replace("{{Sample}}/","").replace('/','_')
        output_name = "Plots/" + output_name + ".pdf"
        pm.MakeMCDataStack(input_name, output_name)

    # Make plots showing the effects of systematic uncertainties
    sample_sys_map = {}
    all_sys = ['jes', 'ees'] # 'isrfsr',, 'mcmodel' 
    for sample in ['tbart', 'Zll', 'Ztautau', 'SingleTop']:
        sample_sys_map[sample] = all_sys
    sample_sys_map["Diboson"] = ['jes', 'ees', 'mcmodel']
    sample_sys_map["Fake"] = ['jes', 'ees']

    # Draw the systematic shifts for each sample
    for channel in ['ee', 'emu', 'mumu']:
        canvas = ROOT.TCanvas("Canvas", "Canvas")
        canvas.Divide(2, 3)
        print "Total Canvas: ", canvas
        objects_on_canvas = []
        for itr, (sample, sys_list) in enumerate(sample_sys_map.iteritems()):
            canvas.cd(itr+1)
            #pad_cd = ROOT.gPad.cd()
            #print "Current Pad: ", ROOT.gPad, " Selected: ", ROOT.gPad.GetSelected(), " Canvas: ", ROOT.gPad.GetCanvas(), " after cd: ", pad_cd
            hist_list = []
            name_list = []
            default_name = hist_name(channel)
            hist_list.append(default_name)
            name_list.append("default")
            for systematic in sys_list:
                for suffix in ['_minus', '_plus']:        
                    input_name = hist_name(channel, systematic+suffix)
                    hist_list.append(input_name)
                    name_list.append(systematic+suffix)
            objects = pm.MakeMultipleVariablePlot(hist_list, sample, nameList=name_list,
                                                UseCurrentCanvas=True, RatioPlot=True)
            title = ROOT.TPaveText(0.4,0.75, 0.6,0.90, "NDC")
            title.SetFillColor(0);
            title.SetBorderSize(0)
            title.SetTextSize(0.08);
            title.AddText(sample)
            title.Draw();
            objects_on_canvas.append(objects)
            objects_on_canvas.append(title)
        canvas.Print("Plots/" + channel + "_systematics.pdf")
        canvas.Clear()


if __name__ == "__main__":
    main()
