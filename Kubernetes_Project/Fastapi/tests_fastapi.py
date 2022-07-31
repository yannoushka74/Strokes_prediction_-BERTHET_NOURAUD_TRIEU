from os.path import exists
from datetime import date
import pytest
import requests

# 1 Tester si fichier CSV est bien présent
# On vérifie que le CSV est bien présent dans le répertoire (indispensable pour faire tourner le modèle)


def is_csv_here(filename):
    file_exists = exists(filename)
    test_date = date.today()
    if file_exists == True:
        test_status = "SUCCESS"
    else:
        test_status = "FAILURE"

    output = '''
        =================================
            CHECK IF CSV IS AVAILABLE
        =================================
        test date = {test_date}
        tested file = {filename}

        expected result = True
        actual restult = {file_exists}

        ==>  {test_status}

        '''
    print(output.format(filename=filename, file_exists=file_exists,
          test_status=test_status, test_date=test_date))
    # Impression dans le fichier de log
    if exists("api_test.log") == True:
        with open("api_test.log", 'a')as file:
            file.write(output.format(
                filename=filename,
                file_exists=file_exists,
                test_status=test_status,
                test_date=test_date
            ))

# 2 Tester si données fausses (text au lieu d'int)


def test_bad_data_type():
    url = 'http://localhost:8000/stroke'
    # On teste de passer du texte pour l'âge là où un float est attendu
    headers = {
        "age": "abc",
        "hypertension": "1",
        "heart_disease": "1",
        "ever_married": "1",
        "Residence_type": "1",
        "avg_glucose_level": "100",
        "bmi": "40"
    }
    r = requests.get(url, headers=headers)
    assert r.status_code == 405

# 3 Si fichier dans lequel on sauvegarde le modèle n'existe pas à la base ?
# def test_exists_saved_ml_file():
#    url = 'http://localhost:8000/'

# 4 Si on demande les performances avant de générer le modèle ?
