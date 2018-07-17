#pySolanio.PhreeqCInput
import os
import os.path
from datetime import datetime as dt2
import solanio


class Builder(dict):
    
    def __init__(self, charge, pH, alk, C) :
        self.FileFormat = solanio.FileFormat()
        self.FileFormat.Load('./Data/PhreeqCFormat.xml')
        self.Charge = charge
        self.pH = pH
        self.alk = alk
        self.C = C
        
    def CreateFromScratch(cls, DB, firstdate):
        n=0
        for solut in DB:
            n+=1
            cls.DefineSolutionBloc(solut, firstdate, n)
     
        
    def Concat(cls, txt, samples):
        output = txt
        for s in samples:
            output += cls[s]
        return output
          
    def ChargeComplete(cls, bloc, label):
        res = bloc
        if cls.Charge==label:
            res += "    charge\n"
        else:
            res += "\n"
        return res
    

    def DefineSolutionBloc(cls, solut, firstdate, n):
        bloc = """
CALCULATE_VALUES
    temps
    -start
    10 save	%f                  
    -end

SOLUTION %i %s
    units      mg/L
""" % (solut.ExperimentTime(firstdate), n, solut.Sample.sample_ID)

        for name, meas in solut.Measurement.items():
            label = cls.FileFormat.FindCorrespondingLabel(meas, 0, "")
            if (label != "" and not solanio.isnan(meas.value) and solanio.isfloat(meas.value)):                  
                if (label == "Alkalinity"):
                    if not cls.alk:
                        bloc += "#"
                    bloc += "    {0}      {1}".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label == "Redox"):
                    bloc += "    {0}      {1}\n".format("pe", -2.9)
                    bloc += "    {0}      {1}\n".format("redox", "pe")
                elif (label == "S(6)"):
                    bloc += "    {0}      {1} as SO4".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label == "N(-3)"):
                    bloc += "    {0}      {1} as NH4+".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label == "N(5)"):
                    bloc += "    {0}      {1} as NO3".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label == "N(3)"):
                    bloc += "    {0}      {1} as NO2".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label =="C2H6"):
                    bloc += "#    {0}      {1} #{2}".format(label, meas.value, meas.unit)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label =="C3H8"):
                    bloc += "#    {0}      {1} #{2}".format(label, meas.value, meas.unit)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label =="CH4"):
                    bloc += "#    {0}      {1} #{2}".format(label, meas.value, meas.unit)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label =="H"):
                    bloc += "#    {0}      {1} #{2}".format(label, meas.value, meas.unit)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label == "C(4)"):
                    if not cls.C:
                        bloc += "#"
                    bloc += "    {0}      {1} {2}".format(label, meas.value, meas.unit)
                    bloc = cls.ChargeComplete(bloc, label)
                elif (label == "pH"):
                    if not cls.pH:
                        bloc += "#"
                    bloc += "    {0}      {1}".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)
                else:
                    bloc += "    {0}      {1}".format(label, meas.value)
                    bloc = cls.ChargeComplete(bloc, label)

                if (len(meas.isotop) > 0):
                    for isot in meas.isotop:
                        label = cls.FileFormat.FindCorrespondingLabel(meas, isot.type, isot.name);
                        if (label !="" and not solanio.isnan(isot.value) and solanio.isfloat(isot.value)):
                            bloc += "    #-isotop {0}      {1} e-6 # VSMOW\n".format(label, isot.value)

        bloc += "END\n\n"
        cls[solut.Sample.sample_ID]=bloc
