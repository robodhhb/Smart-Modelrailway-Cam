# Training auf Google Colab durchführen
Vor dem Training müssen alle Trainingsdaten und die Datei training.csv in den Ordner "TrainData" auf Ihrem Google Drive ohne Unterordner hochgeladen werden. 
Das Training findet hier mit einem Jupyter notebook statt: [Open Colab notebook trainSMRC.ipynb](https://colab.research.google.com/github/robodhhb/Smart-Modelrailway-Cam/blob/main/30_Your_Training/30_Training/trainSMRC.ipynb)

Die möglichen Fehlermeldungen und weitere Warnungen im Abschnitt "Import the required packages" können **ignoriert** werden:
- "ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts datascience 0.10.6 requires folium==0.2.1, but you have folium 0.8.3 which is incompatible".

- "ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts. xarray 2022.12.0 requires packaging>=21.3, but you have packaging 20.9 which is incompatible" 

- Warnung: /usr/local/lib/python3.8/dist-packages/tensorflow_addons/utils/ensure_tf_install.py:53: UserWarning: Tensorflow Addons supports using Python ops for all Tensorflow versions above or equal to 2.9.0 and strictly below 2.12.0 (nightly versions are not supported). 
 The versions of TensorFlow you are currently using is 2.8.4 and is not supported. 

# Run training on Google Colab
Before the training all training data and the file training.csv have to be uploaded into your Google Drive in the folder "TrainData". This folder must not have any subfolder. 
Follow the link for the training: [Open Colab notebook trainSMRC.ipynb](https://colab.research.google.com/github/robodhhb/Smart-Modelrailway-Cam/blob/main/30_Your_Training/30_Training/trainSMRC.ipynb)

The possible error messages and warnings in section "Import the required packages" can be **ignored**:
- "ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts datascience 0.10.6 requires folium==0.2.1, but you have folium 0.8.3 which is incompatible".

- "ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts. xarray 2022.12.0 requires packaging>=21.3, but you have packaging 20.9 which is incompatible"

- Warnung: /usr/local/lib/python3.8/dist-packages/tensorflow_addons/utils/ensure_tf_install.py:53: UserWarning: Tensorflow Addons supports using Python ops for all Tensorflow versions above or equal to 2.9.0 and strictly below 2.12.0 (nightly versions are not supported). 
 The versions of TensorFlow you are currently using is 2.8.4 and is not supported. 
