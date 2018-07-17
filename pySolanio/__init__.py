"""
    Ce package est une transcription python de la librairie Solanio développée en C# par Y. Linard.
    La transcription a été réalisée par l'auteur en 2016. 
    Ce package permet de manipuler des documents Solanio et de les convertir sous différents formats.
"""
 
__version__ = "0.0.1"

name = "pySolanio"

from solanio import ErrorType
from solanio import ActionType
from solanio import BusinessInfo
from solanio import SampleInfo
from solanio import LinkInfo
from solanio import Extract
from solanio import FileFormat
from solanio import AnalyticalTechnic
from solanio import BusinessData
from solanio import SampleData
from solanio import Isotopic_Dependency
from solanio import Measurement
from solanio import InDat
from solanio import Analysis
from solanio import ConversionContext
from solanio import DataConverter
from solanio import Document
