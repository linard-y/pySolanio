# pySolanio.HydroisotopAnalysis
import pandas
import pySolanio as solanio

class Converter(solanio.DataConverter) :
    
    def __init__(self) :
        self.FileFormat = solanio.FileFormat()
        self.FileFormat.Load('./Data/HydroIsotopXLSX2008Format.xml')
        self.Name="HydroIsotop XLSX File Converter"   

    def Import(cls, context) :
        
        DB = []
        Datatable = pandas.read_excel(context.Input, sheetname = 'Water', index_col = False)
        iCol = cls.FileFormat.iAnalysis-1
        

        while iCol < Datatable.shape[1] and Datatable.iat[cls.FileFormat.sampleInfo.iSample_ID, iCol] != '' : 

            DBAn = solanio.Analysis()
            
            if cls.FileFormat.iOperator != 0 :
                DBAn.Operator = Datatable.iat[cls.FileFormat.iOperator, iCol]
            if cls.FileFormat.iReference != 0 :
                DBAn.Reference = Datatable.iat[cls.FileFormat.iReference, iCol]
            if cls.FileFormat.iComment != 0 :
                DBAn.Comments = Datatable.iat[cls.FileFormat.iComment, iCol]

            ###### BUSINESS ######
            DBAn.Business.Load(Datatable, iCol, cls.FileFormat.businessInfo)

            ###### SAMPLE ######
            DBAn.Sample.Load(Datatable, iCol, cls.FileFormat.sampleInfo)
                    
            iRow = cls.FileFormat.iParameter
            
            ###### CHEMISTRY ###### 
            n=-1
            while iRow < Datatable.shape[0] and Datatable.iat[iRow, cls.FileFormat.iParName1] != "" :

                dat = solanio.InDat()
                dat.Load(Datatable, iRow, iCol, cls.FileFormat)
                #print "Row: {}, Col: {}, {}".format(iRow, iCol, dat)
                n+=1
                targetParameter = cls.FileFormat.GetCorrespondingParameter(dat.Name1)
                #print "Row: {}, Col: {}, LinkInfo -- Name: {}, Dependency: {}".format(iRow, iCol, targetParameter.Name, targetParameter.Dependency)

                if (targetParameter.Name != '') : 

                    meas = solanio.Measurement()

                    if (targetParameter.Dependency==0): #Parametre, Element, Cation ou Anion,
                        if targetParameter.Name in DBAn.Measurement : 
                            meas = DBAn.Measurement[targetParameter.Name]
                            #print("j'efface temprairement %s" % targetParameter.Name)
                            del DBAn.Measurement[targetParameter.Name]
                            
                        meas.name = targetParameter.Name
                        meas.analyticaltechnic = targetParameter.AnalyticalTechnic
                        meas.error =targetParameter.Error
                        meas.errortype = str(targetParameter.ErrorType)
                        meas.value = dat.Value
                        meas.unit = dat.Unit 

                        if dat.ErrType != solanio.ErrorType.Unknown :
                            meas.errortype = str(dat.ErrType)

                        if dat.Technic.Name != "unknown" : 
                            meas.analyticaltechnic = dat.Technic.Name 
                            
                        DBAn.Measurement[meas.name] = meas
                        #print "Row: {}, Col: {}, {}".format(iRow, iCol, meas.name)

                    elif targetParameter.Dependency in [1,2,3]: #Isotope, Isotopic_Ratio or Delta_Isotopic_Ratio
                        if targetParameter.Name in DBAn.Measurement : 
                            meas = DBAn.Measurement[targetParameter.Name]
                            del DBAn.Measurement[targetParameter.Name]
                        else :
                            targetParameter2 = solanio.LinkInfo()
                            targetParameter2= cls.FileFormat.GetCorrespondingParameter(targetParameter.Name)
                            meas.name = targetParameter2.Name
                            meas.analyticaltechnic = targetParameter2.AnalyticalTechnic
                            meas.error = str(targetParameter2.Error)
                            meas.errortype = str(targetParameter2.ErrorType) 

                        isot = solanio.Isotopic_Dependency()
                        isot.name = targetParameter.Complete
                        isot.analyticaltechnic = targetParameter.AnalyticalTechnic
                        isot.error = targetParameter.Error
                        isot.errortype = str(targetParameter.ErrorType)
                        isot.type = int(targetParameter.Dependency)
                        isot.value = dat.Value
                        isot.unit = dat.Unit;

                        if (dat.Error != "unknown") :
                            isot.error = str(dat.Error)

                        if (dat.ErrType != solanio.ErrorType.Unknown) :
                            isot.errortype = str(dat.ErrType)

                        if (dat.Technic.Name != "unknown") :
                            isot.analyticaltechnic = dat.Technic.Name
                        meas.isotop.append(isot)
                        DBAn.Measurement[meas.name] = meas
                        #print "Row: {}, Col: {}, {}".format(iRow, iCol, meas.name)
                    # end if
                # end if                       
                iRow += 1
                if iRow in cls.FileFormat.RowToSkip:
                    while iRow in cls.FileFormat.RowToSkip:
                        iRow += 1
            # end while loop
                    
            DB.append(DBAn)

            iCol += 1
        # end while loop 
        return DB                                     
    
    def Export(cls, context) :
        return None
