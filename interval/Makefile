CXX=`root-config --cxx`
CXXFLAGS=`root-config --cflags`
LDFLAGS=`root-config --ldflags`
LDLIBS=`root-config --glibs`
ROOTLIBS=-lRooFit -lHtml -lMinuit -lRooFitCore -lRooStats -lHistFactory

all: StandardBayesianMCMCDemo StandardProfileInspectorDemo

% : %.C
	g++ -g -Wall `root-config --cflags --libs` -L$(ROOTSYS)/lib $(ROOTLIBS) $? -o $@ 
