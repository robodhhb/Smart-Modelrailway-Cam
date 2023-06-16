# Beispiel: Annotation der Trainingsdaten
In diesem Ordenr sind die für das Training ausgewählten Bilder abgelegt. Sie müssen für das Training entpackt werden. Alle Dateien dieses Ordners müssen auf einer Ebene in ihr Google-Drive Ordner /content/drive/MyDrive/TrainData hochgeladen werden (ohne Unterordner). 
Die Annotation erfolgt mit [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/).

(Klassen-)Namen von Lokomotiven beginnen mit einem ":". 

Weitere Dateien für dieses Beipiel sind:
|Dateiname | Beschreibung |
|---------------- | -----------------------------------|
|VIA_SMRC.json    | Projekt-Datei für den VGG Image Annotator |
|VIA_SMRC_json.json | Exportierte Datei mit Annotationen |
|VIAjson2ModelMaker.py | Programm zur Generierung der Datei "training.csv" |
|training.csv | Trainingsdatei für das Transfer-Learning mit dem Google ModelMaker API|
|train.py| Code für das Training mit Google ModelMaker API (wird vom jupyter notebook aufgerufen)|

# Example: Annotation of the training data
In this folder the selected traing data is stored. They have to be unzipped for the training without creating a subfolder. All files of this folder have to be uploaded in your google-drive folder: /content/drive/MyDrive/TrainData. 
The annotation has been done with [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/).

(Class)Names of Lokomotives start with a ":". 

Files in this example are:
|Filename | Description |
|---------------- | -----------------------------------|
|VIA_SMRC.json    | Project-file for the  VGG Image Annotator |
|VIA_SMRC_json.json | Exported annotation file |
|VIAjson2ModelMaker.py | Program for generation the file "training.csv" |
|training.csv | Training file for the  Google ModelMaker API|
|train.py| Code for the training with Google ModelMaker API (is called by the jupyter notebook)|
