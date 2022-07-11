# Annotation Ihrer Trainingsdaten
In diesem Ordenr werden die für das Training ausgewählten Bilder auf dem PC abgelegt. Sie müssen für das Training entpackt auf dieser Ebene liegen (ohne Unterordner). 
Die Annotation erfolgt mit [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/).
Im VGG Image Annotator öffnen Sie die Projekt-Datei "VIA_SMRC.json" auf dem PC. In den Projekt-Settings setzen sie den Default-Path auf den Pfad 
mit den Trainingsdaten (muss mit "\\" enden). 

Nach der Annotation exportieren Sie das Ergebnis als JSON-Datei und generieren die trainings.csv Datei.

|Dateiname | Beschreibung |
|---------------- | -----------------------------------|
|VIA_SMRC.json    | Projekt-Datei für den VGG Image Annotator |
|VIAjson2ModelMaker.py | Programm zur Generierung der Datei "training.csv" nach dem Annotieren |


# Annotation of your training data
In this folder the selected training data is stored on a PC. They have to be unzipped for the training without creating a subfolder.
The annotation has to be done with [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/).
Open the project file "VIA_SMRC.json" with VGG Image Annotator on the PC. Change the default path in the project settings to the path with 
the training data on youtr PC. Don't forget a closing "\\". 

After having done the annotation export the result as JSON-file and generate training.csv.

|Filename | Description |
|---------------- | -----------------------------------|
|VIA_SMRC.json    | Project-file for the  VGG Image Annotator |
|VIAjson2ModelMaker.py | Program for generation the file "training.csv" |
