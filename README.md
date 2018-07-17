# pySolanio - SOLution ANalysis Input/Output
========================================================

Ce package est une transcription python de la librairie Solanio développée en C# par Y. Linard.
La transcription a été réalisée par l'auteur en 2016. 
Ce package permet de manipuler des documents Solanio et de les convertir sous différents formats.

Les documents Solanio contiennent des résultats d'analyse chimique (en général des analyses de solutions fluides) qui peuvent être importés depuis différents formats de fichier ( par ex., report de laboratoire d'analyses) et exportés vers d'autres formats (par ex., fichier d'entrée phreeqC).

Vous pouvez l'installer avec pip:

    pip install pySolanio

Exemple d'usage:

    >>> import pySolanio as solanio
    >>> doc = solanio.Document()

Ce code est sous licence MIT.
