# Annotation Ihrer Trainingsdaten
In diesem Ordenr werden die für das Training ausgewählten Bilder auf dem PC abgelegt. Sie müssen für das Training entpackt auf dieser Ebene liegen (ohne Unterordner). 
Die Annotation erfolgt mit [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/).
Im VGG Image Annotator öffnen Sie die Projekt-Datei "VIA_SMRC.json" auf dem PC. In den Projekt-Settings setzen sie den Default-Path auf den Pfad 
mit den Trainingsdaten (muss mit "\\" enden). 

Danach müssen die Klassennamen der Loks bzw. Waggons unter "Attributes" im Attribute "classname" mit "Add new option id" eingetragen werden. Loks müssen mit ":" beginnen.

Nach der Annotation exportieren Sie das Ergebnis als JSON-Datei und generieren die trainings.csv Datei. Für das Training müssen alle Dateien dieses Ordners in ihr Google-Drive Verzeichnis /content/drive/MyDrive/TrainData hochgeladen werden.

|Dateiname | Beschreibung |
|---------------- | -----------------------------------|
|VIA_SMRC.json    | Projekt-Datei für den VGG Image Annotator |
|VIAjson2ModelMaker.py | Programm zur Generierung der Datei "training.csv" nach dem Annotieren |
|train.py| Code für das Training mit Google ModelMaker API (wird vom jupyter notebook aufgerufen)|


# Annotation of your training data
In this folder the selected training data is stored on a PC. They have to be unzipped for the training without creating a subfolder.
The annotation has to be done with [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/).
Open the project file "VIA_SMRC.json" with VGG Image Annotator on the PC. Change the default path in the project settings to the path with 
the training data on youtr PC. Don't forget a closing "\\". 

Then the class names of the locomotives or wagons must be entered under "Attributes" in the "classname" attribute with "Add new option id". Locomotives must begin with ":"

After having done the annotation export the result as JSON-file and generate training.csv. For the training all files of this folder have to be uploaded to your google-drive folder: /content/drive/MyDrive/TrainData.

|Filename | Description |
|---------------- | -----------------------------------|
|VIA_SMRC.json    | Project-file for the  VGG Image Annotator |
|VIAjson2ModelMaker.py | Program for generation the file "training.csv" |
|train.py| Code for the training with Google ModelMaker API (is called by a jupyter notebook)|
