#!/usr/bin/env python

import sys
sys.argv.append( '-b' )
import ROOT

from collections import OrderedDict
from PlotMaker.PlotMaker import PlotMaker

from common import color_map


def hist_name(channel, systematic="default", name="Jet_N_0_6i_20GeV"):
    return "%s/{{Sample}}/%s/%s" % (channel, systematic, name)


def top_plot_maker():
    """ Create, configure, and return a PlotMaker
    
    Add the Data, signal, and backgrounds
    """

    pm = PlotMaker("PlotMaker", "Plot Maker")
    pm.SetLegendBoundaries( .75, .55, .95, .90 )

    input_file = "data/TopHistograms.root"

    # Add the samples for data, signal, and background
    pm.AddDataSample(files=input_file, name="Data", title="data10 (7TeV)")

    pm.AddMCSample(files=input_file, name="tbart", title="t #bar{t}", signal=True, Scale=200)
    pm.AddMCSample(files=input_file, name="Zll", title="Z #rightarrow ll", color=color_map['Zll'])
    pm.AddMCSample(files=input_file, name="Ztautau", title="Z #rightarrow #tau #tau", color=color_map['Ztautau'])
    pm.AddMCSample(files=input_file, name="Diboson", title="Diboson", color=color_map['Diboson'])
    pm.AddMCSample(files=input_file, name="SingleTop", title="Single Top", color=color_map['SingleTop'])
    pm.AddMCSample(files=input_file, name="Fake", title="Fake", color=color_map['Fake'])

    return pm


def main():

    # Get the PlotMaker
    pm = top_plot_maker()

    # Make the nominal MC/Data comparisons
    for channel in ['ee', 'emu', 'mumu']:
        input_name = hist_name(channel)
        output_name = input_name.replace("{{Sample}}/","").replace('/','_')
        output_name = "Plots/" + output_name + ".pdf"
        pm.MakeMCDataStack(input_name, output_name)

    # Make plots showing the effects of systematic uncertainties
    sample_sys_map = OrderedDict()
    sample_sys_map["tbart"] = ['jes', 'ees', 'mcmodel']
    sample_sys_map["Ztautau"] = ['jes', 'ees']
    sample_sys_map["Diboson"] = ['jes', 'ees', 'mcmodel']
    sample_sys_map["Fake"] = ['jes', 'ees']

    # Draw the systematic shifts for each sample
    for channel in ['ee', 'emu', 'mumu']:

        # Create a canvas with 6 sub-pads
        canvas = ROOT.TCanvas("Canvas", "Canvas")
        canvas.Divide(2, 2)
        objects_on_canvas = []

        # Draw the 6 samples on the subpads with their systematic shifts
        for itr, (sample, sys_list) in enumerate(sample_sys_map.iteritems()):
            canvas.cd(itr+1)
            default_name = hist_name(channel)
            hist_list = [default_name]
            name_list = ['default']
            color_list = [1]
            for systematic in sys_list:
                for suffix in ['_minus', '_plus']:        
                    input_name = hist_name(channel, systematic+suffix)
                    hist_list.append(input_name)
                    name_list.append(systematic+suffix)
                    color_list.append(34 + len(color_list))
            objects = pm.MakeMultipleVariablePlot(hist_list, sample, 
                                                  nameList=name_list, colorList=color_list,
                                                  UseCurrentCanvas=True, RatioPlot=True)
            title = pm.DrawText(sample)
            objects_on_canvas.append((objects, title))
            #objects_on_canvas.append(title)

        # Save and clear the canvas
        canvas.Print("Plots/" + channel + "_systematics.pdf")
        canvas.Clear()
        del canvas


if __name__ == "__main__":
    main()
