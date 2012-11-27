
import math
import StringIO
import ROOT

from fitModel import get_model


def minos(var):
    return ROOT.RooCmdArg("Minos",True,0,0,0,"","",ROOT.RooArgSet(var),0)


def print_error(poi, tot_err_up, tot_err_down):
    
    val = poi.getVal()
    
    sys_err_up = poi.getErrorHi()
    sys_err_down = poi.getErrorLo()

    err_up_sqr = tot_err_up*tot_err_up - sys_err_up*sys_err_up
    err_up = math.sqrt(abs(err_up_sqr))

    err_down_sqr = tot_err_down*tot_err_down - sys_err_down*sys_err_down
    err_down = math.sqrt(abs(err_down_sqr))

    string1 = "+{:.3f}/-{:.3f}".format(err_up, err_down)
    string2 = "(+{:.2%} / -{:.2%})".format(err_up/val, err_down/val)
    return "{:>10} {:>10}".format(string1, string2)


def main():

    (wspace, model, data, poi) = get_model()
    systematic_list = ["DY_ee", "DY_mumu", "EleEff", "FakeRate", "MuonEff", \
                           "PDF", "Xsec", "ees", "isrfsr", "jes", "mes", "met", "model"]

    # Do an initial fit and get the uncertainty
    model.fitTo(data, minos(poi))
    err_up = poi.getErrorHi()
    err_down = poi.getErrorLo()

    result_string = StringIO.StringIO()

    # Get the Lumi Error
    wspace.var("Lumi").setConstant(True)
    model.fitTo(data, minos(poi))
    print >>result_string,  "Error On Lumi: ".rjust(30), print_error(poi, err_up, err_down)

    # Get the errors with lumi fixed
    err_up = poi.getErrorHi()
    err_down = poi.getErrorLo()

    # Get the errors for other systematics
    for sys in systematic_list:
        sys = "alpha_" + sys
        model.fitTo(data)
        wspace.var(sys).setConstant(True)
        model.fitTo(data, minos(poi))
        wspace.var(sys).setConstant(False)
        print >>result_string, ("Error On %s: " % sys).rjust(30), print_error(poi, err_up, err_down)
        
    print result_string.getvalue()

if __name__ == "__main__":
    main()
