"""
    Implémentation des classes de base.
"""
import datetime as dt
from datetime import datetime as dt2
from IPython.core.display import HTML
import pandas
from enum import Enum
from lxml import etree
import os
import os.path
import math
from itertools import takewhile

__all__ = ['ErrorType', 'ActionType', 'BusinessInfo', 'SampleInfo', 'LinkInfo', 'FileFormat', 'AnalyticalTechnic', 'BusinessData', 'SampleData', 'Isotopic_Dependency', 'Measurement', 'InDat', 'Analysis', 'ConversionContext', 'DataConverter', 'Document']

def closest(list, Number):
    aux = []
    for valor in list:
        aux.append(abs(Number-valor))

    return aux.index(min(aux))

def GetIndex(t, tf, ti=0):
    index = len([x for x in takewhile(lambda x: x[1] <= tf, enumerate(t))])
    if index>0:
        return index-1
    else:
        return -1

def Subset(variable, i_start, i_end):
    result=[]
    for i in range(i_start,i_end):
        result.append(variable[i])
    return result
    
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def isnan(value):
    try:
        import math
        return math.isnan(float(value))
    except:
        return False

class ErrorType(Enum):
    Absolute = 0
    Relative = 1
    Unknown = 2

class ActionType(Enum):
    Import = 0
    Export = 1
    
class BusinessInfo:
    """Structure stockant les infos contractuelles"""
    def __init__(self):
        self.iOrder_No=0
        self.iDate_of_order=0
        self.iReception_of_sample=0
        self.iResults_waited=0
        self.iReturn_of_container=0
        self.iDate_of_invoice=0
        
    def Load(cls, tree):
        cls.iOrder_No = Extract(tree,"/Format/Business/Order_No", 'i')
        cls.iDate_of_order = Extract(tree,"/Format/Business/Date_of_order_Row", 'i')
        cls.iReception_of_sample = Extract(tree,"/Format/Business/Reception_of_sample", 'i')
        cls.iResults_waited = Extract(tree,"/Format/Business/Results_waited", 'i')
        cls.iReturn_of_container = Extract(tree,"/Format/Business/Return_of_container", 'i')
        cls.iDate_of_invoice = Extract(tree,"/Format/Business/Date_of_invoice_Row", 'i')  
	
class SampleInfo:
    """Structure stockant les infos d'identification et d'echantillonnage"""
    def __init__(self):
        self.iSample_ID=0
        self.iSampling_place=0
        self.iOperation_code=0
        self.iSampling_time=0
        self.iContainer_number=0
        self.iSampling_date=0
        self.iType=0
        self.iTotal_sample_volume=0
        self.iDescription=0
        self.iTreatment=0
        self.iStart_of_measurment=0
        self.iSampling_Conditions_informations=0
        
    def Load(cls, tree):
        cls.iSample_ID = Extract(tree,"/Format/Sample/Id", 'i')
        cls.iSampling_place = Extract(tree,"/Format/Sample/Sampling_Place", 'i')
        cls.iOperation_code = Extract(tree,"/Format/Sample/Operation_Code", 'i')
        cls.iContainer_number = Extract(tree,"/Format/Sample/Container_number", 'i')
        cls.iDescription = Extract(tree,"/Format/Sample/Description", 'i')
        cls.iSampling_Conditions_informations = Extract(tree,"/Format/Sample/Sampling_Conditions_informations", 'i')
        cls.iSampling_date = Extract(tree,"/Format/Sample/Sampling_date", 'i')
        cls.iSampling_time = Extract(tree,"/Format/Sample/Sampling_time", 'i')
        cls.iStart_of_measurment = Extract(tree,"/Format/Sample/Start_of_measurment", 'i')
        cls.iTotal_sample_volume = Extract(tree,"/Format/Sample/Total_sample_volume", 'i')
        cls.iTreatment = Extract(tree,"/Format/Sample/Treatment", 'i')
        cls.iType = Extract(tree,"/Format/Sample/Type", 'i')
        
    def __str__(self):
        """Methode permettant d'afficher plus joliment notre objet"""
        return '-- SampleInfo --\nID: {0}\nBorehole: {1}\nOperation: {2}\nContainer: {3}\nDescription: {4}\nSampling conditions: {5}\nSampling date: {6}\nSampling time: {7}\nStart of measurments: {8}\nVolume : {9}\nTreatment : {10}\nType : {11}'.format(self.iSample_ID, self.iSampling_place, self.iOperation_code,self.iContainer_number, self.iDescription, self.iSampling_Conditions_informations,self.iSampling_date, self.iSampling_time, self.iStart_of_measurment,self.iTotal_sample_volume, self.iTreatment, self.iType)
        
class LinkInfo:
    """Structure definissant les liens de conversion entre les paramètres d'une source exterieure et ceux d'un document Solanio """
    def __init__(self):
        self.Dependency=0
        self.Name=''
        self.Complete=''
        self.AnalyticalTechnic=''
        self.Error=float(0.0)
        self.ErrorType=ErrorType.Unknown
        
    def Load(cls, XMLelement):
            cls.Name = XMLelement.attrib['name']#.encode('ascii','ignore')
            cls.Dependency = int(XMLelement.attrib['dependency'])
            cls.Complete = XMLelement.attrib['complete']#.encode('ascii','ignore')
            cls.AnalyticalTechnic = XMLelement.attrib['analyticaltechnic']#.encode('ascii','ignore')
            if isinstance(XMLelement.attrib['error'], float): 
                cls.Error = float(XMLelement.attrib['error'])
            else:
                cls.Error=0
            if isinstance(XMLelement.attrib['error_type'], int):                        
                cls.ErrorType = int(XMLelement.attrib['error_type'])
            else:
                cls.ErrorType = ErrorType.Unknown
                
    def __str__(self):
        """Methode permettant d'afficher plus joliment notre objet"""
        return 'LinkInfo -- Name: %s, Dependency: %i, Complete: %s, AnalyticalTechnic: %s, Error: %f, ErrorType: %s' % (self.Name, self.Dependency, self.Complete, self.AnalyticalTechnic, self.Error, self.ErrorType)

def Extract(tree, data, outformat = 's'):
        extraction = tree.xpath(data)
        if outformat == 'i':
            if len(extraction)>0:
                try:
                    return int(tree.xpath(data)[0].text)
                except :
                    return None
            else:
                return None
        else:
            if len(extraction)>0:
                return tree.xpath(data)[0].text
            else:
                return None

class FileFormat(dict):
    """Structure stockant la facon dont est organise une fichier de donnees d'entree"""
    def __init__(self):
        self.iReference=0
        self.iOperator=0
        self.iComment=0

        self.businessInfo = BusinessInfo()
        self.sampleInfo = SampleInfo()
        
        self.iAnalysis=0               #  indique le numero de la ligne ou figure la premiere quantite d'espece chimique constitutive de la solution
        self.iParameter=0              #  indique le numero de la ligne ou figure le premier parametre
        
        self.iParName1=0               #  indique le numero de la colonne ou figurent les noms des parametres ou des especes chimiques constitutives de la solution
        self.iParName2=0               #  indique le numero de la colonne ou figurent les noms simplifies des parametres ou des especes chimiques constitutives de la solution
        self.iParUnit=0                #  indique le numero de la colonne ou figurent les unites des parametres ou des quantites d'especes chimiques constitutives de la solution
        self.iParError=0               #  indique le numero de la colonne ou figurent les erreurs associes a la mesure des parametres ou des quantites d'especes chimiques constitutives de la solution
        self.iParErrorType=0           #  indique le numero de la colonne ou figure le type d'erreur (absolu ou relative) associe a chaque parametre ou chaque quantite d'espece chimique constitutives de la solution
        self.iParAnalyticalTechnic=0   #  indique le numero de la colonne ou figurent les techniques analystiques utilises pour la mesure des parametres ou celle des quantite d'espece chimique constitutive de la solution
        self.iParComment=0             #  indique le numero de la colonne ou figure le commentaire sur la mesure du parametre ou sur celle de la quantite d'espece chimique

        self.Extension=''
        self.RowToSkip = []
            
    def Load(cls, path):
        tree = etree.parse(path)
     
        cls.Extension = Extract(tree,"/Format/Extension")
        cls.iReference = Extract(tree,"/Format/Reference_Row", 'i')
        cls.iOperator = Extract(tree,"/Format/Operator_Row", 'i')
        cls.iComment = Extract(tree,"/Format/Comment_Row", 'i')

        cls.businessInfo.Load(tree)
        cls.sampleInfo.Load(tree)
        
        cls.iAnalysis = Extract(tree,"/Format/First_Solution_Column", 'i')
        cls.iParameter = Extract(tree,"/Format/First_Parameter_Row", 'i')
        cls.iParName1 = Extract(tree,"/Format/Parameter_Name_Column", 'i')
        cls.iParName2 = Extract(tree,"/Format/Parameter_QuickName_Column", 'i')
        cls.iParUnit = Extract(tree,"/Format/Parameter_Unit_Column", 'i')
        cls.iParError = Extract(tree,"/Format/Parameter_Error_Column", 'i')
        cls.iParErrorType = Extract(tree,"/Format/Parameter_Error_Type_Column", 'i')
        cls.iParAnalyticalTechnic = Extract(tree,"/Format/Parameter_Technic_Column", 'i')
        cls.iParComment = Extract(tree,"/Format/Parameter_Comment_Column", 'i')
        try:
            cls.RowToSkip = map(int, Extract(tree,"/Format/RowToSkip").split(","))
        except:
            cls.RowToSkip = None
        
        link = tree.findall('.//key')
        #Loop through all the <key> items.
        for keyitem in link:
            lki = LinkInfo()
            lki.Load(keyitem)
            cls[keyitem.text] = lki #cls[keyitem.text.encode('ascii','ignore')] = lki

    def GetCorrespondingParameter(cls, par):
        target = LinkInfo()
        if (par.strip() in cls):
            target.Name = cls[par.strip()].Name
            target.Dependency = cls[par.strip()].Dependency
            target.Complete = cls[par.strip()].Complete
            target.AnalyticalTechnic = cls[par.strip()].AnalyticalTechnic
            target.Error = cls[par.strip()].Error
            target.ErrorType = cls[par.strip()].ErrorType
            return target
        else:
            return target
        
    def FindCorrespondingLabel(cls, meas, depend, isotop):
        res=""
        for key in cls.keys():
            #print(cls[key].Name, meas.name, cls[key].Name == meas.name)
            if (cls[key].Name == meas.name):
                #print(cls[key].Dependency, depend, cls[key].Dependency == depend)
                if (cls[key].Dependency == depend):
                    #print('cls[key].Complete: %s, isotop: %s, test: %r' % (cls[key].Complete, isotop, cls[key].Complete == isotop))
                    if (cls[key].Complete == isotop):
                        res = key
        #if res :
        #    print ('%s --> %s' % (meas.name, res))
        #else:
        #    print ('%s --> %s' % (meas.name, "??"))
        return res

class AnalyticalTechnic:
    """Classe definissant une technique analytique caracterisee par :
    - son identifiant
    - sa limite de detection
    - sa precision
    - le pre-traitement"""
    def __init__(self): # Notre methode constructeur
        self.Name = 'Unknown'
        self.DetectionLimit = float('nan')
        self.PreTreatment = 'Unknown'
        self.Precision = float('nan')

class BusinessData:
    def __init__(self):
        self.order=''
        self.date_of_order=''
        self.reception_of_sample=''
        self.results_waited=''
        self.return_of_container=''
        self.date_of_invoice=''
        
    def Load(cls, Datatable, iCol, BI):
        if BI.iOrder_No != 0 :
            cls.order = Datatable.iat[BI.iOrder_No, iCol]
        if BI.iDate_of_invoice != 0 :
            cls.date_of_invoice = Datatable.iat[BI.iDate_of_invoice, iCol]
        if BI.iDate_of_order != 0 :
            cls.date_of_order = Datatable.iat[BI.iDate_of_order, iCol]
        if BI.iReception_of_sample != 0 :
            cls.reception_of_sample = Datatable.iat[BI.iReception_of_sample, iCol]
        if BI.iResults_waited != 0 :
            cls.results_waited = Datatable.iat[BI.iResults_waited, iCol]
        if BI.iReturn_of_container != 0 :
            cls.return_of_container = Datatable.iat[BI.iReturn_of_container, iCol]
        
class SampleData:
    def __init__(self):
        self.sample_ID=''
        self.sampling_place=''
        self.operation_code=''
        self.sampling_date=''
        self.sampling_time=''
        self.container_number=0
        self.type=''
        self.total_sample_volume=0
        self.description=''
        self.treatment=''
        self.start_of_measurment=''
        self.conditionning_informations=''
        
    def Load(cls, Datatable, iCol, SI):
        if SI.iContainer_number != 0 :
            cls.container_number = float(Datatable.iat[SI.iContainer_number, iCol])
        if SI.iDescription != 0 :
            cls.description = Datatable.iat[SI.iDescription, iCol]
        if SI.iSampling_Conditions_informations != 0 :
            cls.conditionning_informations = Datatable.iat[SI.iSampling_Conditions_informations, iCol]
        if SI.iSampling_date != 0 :
            cls.sampling_date = Datatable.iat[SI.iSampling_date, iCol]
        if SI.iSampling_time != 0 :
            cls.sampling_time = Datatable.iat[SI.iSampling_time, iCol]
        if SI.iStart_of_measurment != 0 :
            cls.start_of_measurment = Datatable.iat[SI.iStart_of_measurment, iCol]
        if SI.iTotal_sample_volume != 0 :
            cls.total_sample_volume = float(Datatable.iat[SI.iTotal_sample_volume, iCol])
        if SI.iTreatment != 0 :
            cls.treatment = Datatable.iat[SI.iTreatment, iCol]
        if SI.iType != 0 :
            cls.type = Datatable.iat[SI.iType, iCol]
        if SI.iSample_ID != 0 :
            cls.sample_ID = Datatable.iat[SI.iSample_ID, iCol]
        if SI.iSampling_place != 0 :
            cls.sampling_place = Datatable.iat[SI.iSampling_place, iCol]
        if SI.iOperation_code != 0 :
            cls.operation_code = Datatable.iat[SI.iOperation_code, iCol]
            
    def __str__(self):
        """Methode permettant d'afficher plus joliment notre objet"""
        return 'Sample -- ID: {0}, Borehole: {1}, Operation: {2}, Date: {3}'.format(self.sample_ID, self.sampling_place, self.operation_code, dt2.combine(self.sampling_date,self.sampling_time))

class Isotopic_Dependency:
    def __init__(self):
        self.name = ''
        self.unit = 'Unknown'
        self.value = float('nan')
        self.type = 1
        self.error=float('nan')
        self.errortype = ErrorType.Unknown
        self.analyticaltechnic = AnalyticalTechnic()

class Measurement:
    def __init__(self):
        self.isotop = []
        self.name = 'newMeasurement'
        self.unit = 'Unknown'
        self.value = float('nan')
        self.error = float('nan')
        self.errortype=ErrorType.Unknown
        self.analyticaltechnic = AnalyticalTechnic()
        
    #def __str__(self):
    #    """Methode permettant d'afficher plus joliment notre objet"""
    #    return 'Measurement -- Name: %s, Value: %f, Unit: %s'%(self.name, self.value, self.unit)

class InDat:
    def __init__(self):
        self.Name1 = ''
        self.Name2 = ''
        self.Value = float('nan')
        self.Unit = 'Unknown'
        self.Error = float('nan')
        self.ErrType = ErrorType.Unknown
        self.Technic = AnalyticalTechnic()
        self.Comment = 'None'
        
    def Load(self, Datatable, iRow, iCol, FF):
        
            if FF.iParName1 != 0 :
                self.Name1 = Datatable.iat[iRow, FF.iParName1-1]#.encode('ascii','ignore')
                
            if FF.iParName2 != 0 :
                if isfloat(Datatable.iat[iRow, FF.iParName2-1]):
                    self.Name2 = ''
                else:
                    self.Name2 = Datatable.iat[iRow, FF.iParName2-1]#.encode('ascii','ignore')
                    
            try:           
                self.Value = float(Datatable.iat[iRow, iCol])
            except ValueError:
                self.Value = float('nan')
            except Exception:
                self.Value = float('nan')
                
            if FF.iParUnit != 0 :
                if isfloat(Datatable.iat[iRow, FF.iParUnit-1]):
                    self.Unit = 'Unknown'
                else:
                    self.Unit = Datatable.iat[iRow, FF.iParUnit-1]#.encode('ascii','ignore')
                    
            if FF.iParError != 0 :
                try:
                    self.Error = int(Datatable.iat[iRow, FF.iParError-1])
                except ValueError:
                    self.Error = float('nan')
            else:
                self.Error = float('nan')
                
            if FF.iParErrorType != 0 :
                self.ErrType = int(Datatable.iat[iRow, FF.iParErrorType-1]) 
            else:
                self.ErrType = ErrorType.Unknown;
                
            if FF.iParAnalyticalTechnic != 0 :
                self.Technic.Name = Datatable.iat[iRow, FF.iParAnalyticalTechnic-1]#.encode('ascii','ignore')
            else:
                self.Technic.Name = "unknown"
                
            if FF.iParComment != 0 :
                self.Comment = Datatable.iat[iRow, FF.iParComment-1]#.encode('ascii','ignore')
            else:
                self.Comment = "none"

    
    def __repr__(self):
        """Quand on entre notre objet dans l'interpreteur"""
        return 'InDat -- Name1: {0}, Name2: {1}, Value: {2}, Unit: {3}'.format(self.Name1, self.Name2, self.Value, self.Unit)
    def __str__(self):
        """Methode permettant d'afficher plus joliment notre objet"""
        return 'InDat -- Name1: {0}, Name2: {1}, Value: {2}, Unit: {3}'.format(self.Name1, self.Name2, self.Value, self.Unit)

class Analysis:
    def __init__(self):
        self.Business = BusinessData()
        self.Sample = SampleData()
        self.Measurement = dict()

        self.Operator=''
        self.Reference=''
        self.Comments=''
        
    def ExperimentTime(self, t0):
        return(dt2.combine(self.Sample.sampling_date, self.Sample.sampling_time) - t0).total_seconds()/(24*60*60)
        
    def __str__(self):
        """Methode permettant d'afficher plus joliment notre objet"""
        return '--Analysis -- \n{0}\n Number of measurements {1}'.format(self.Sample, len(self.Measurement))

class ConversionContext :
    def __init__(self):
        self.CurrentDB = []
        self.Input = ''
        self.Output = ''
        self.ActionType = ActionType.Import

class DataConverter:
    def __init__(self):
        self.FileFormat = FileFormat()
        self.Name =''
        
    def PerformAction(self, ctxt):
        if ctxt.ActionType == ActionType.Import:
            ctxt.CurrentDB = self.Import(ctxt)
        elif ctxt.ActionType == ActionType.Export:
            ctxt.CurrentDB = self.Export(ctxt)

    def Import(cls, ctxt):
        pass
    
    def Export(cls, ctxt):
        pass    

class Document :
    """
    Implemantation de la classe Document. 
    """
    def __init__(self) :
        self.Name = 'newDocument'
        self.Data = list()
        self.IgnoredData = list()
        self.ExperimentStart=0
               
    def Count(self, all_data = False): 
        if all_data == True :
            return len(self.Data)
        else:
            return len(self.Data)-len(self.IgnoredData)
        
    def SampleIDs(self, all_data = False):
        sampleIDs= list()
        for An in self.Data :
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                sampleIDs.append(An.Sample.sample_ID)
        return sampleIDs
    
    def Times(self, all_data = False):
        times = list()
        for An in self.Data :
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                times.append(An.ExperimentTime(self.ExperimentStart))
        return times
    
    def TimeAt(self, i, all_data = False):
        return self.Times(all_data)[i]
    
    def Volumes(self, all_data = False):
        volumes = list()
        for An in self.Data :
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                volumes.append(An.Sample.total_sample_volume)
        return volumes
    
    def VolumeAt(self, i, all_data = False):
        V=0.0
        for idx in range(0, i):
            V+=self.Volumes(all_data)[idx]
        return V
    
    def Chemicals(self, name, all_data = False):
        chemicals = list()
        for An in self.Data :
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                chemicals.append(An.Measurement[name])
        return chemicals
    
    def V_Chemicals(self, name, all_data = False):
        chemicals = list()
        for An in self.Data :
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                chemicals.append(An.Measurement[name].value)
        return chemicals
    
    def Isotops(self, name, itype, isot, all_data = False):
        isotops = list()
        for An in self.Data :
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                isotops.append(float('NaN'))
                index = len(isotops)-1
                if len(An.Measurement[name].isotop)>0 :
                    for Is in An.Measurement[name].isotop :
                        if Is.type == itype :
                            if Is.name == isot :
                                isotops[index]=Is
        return isotops
    
    def V_Isotops(self, name, itype, isot, all_data = False):
        isotops = list()
        for An in self.Data :
            #print(An.Sample.sample_ID, An.Sample.sample_ID in self.IgnoredData)
            if all_data == True or not An.Sample.sample_ID in self.IgnoredData:
                isotops.append(float('NaN'))
                index = len(isotops)-1
                if len(An.Measurement[name].isotop)>0 :
                    for Is in An.Measurement[name].isotop :
                        if Is.type == itype :
                            if Is.name == isot :
                                isotops[index]=Is.value
            #elif An.Sample.sample_ID in self.IgnoredData:
                #print(An.Sample.sample_ID + ' is ignored')
        return isotops
    
    def ChemicalAt(self, name, i, all_data = False):
        return self.Chemicals(name, all_data)[i] 
    
    def IsotopAt(self, name, itype, isot, i, all_data = False):
        return self.Isotops(name, itype, isot, all_data)[i]
    

    
