from os.path import exists
import pytest
import requests

# 1 Tester si fichier CSV est bien présent
# On vérifie que le CSV est bien présent dans le répertoire (indispensable pour faire tourner le modèle)


def test_needed_files():
    strokes_csv = exists(
        "/home/ubuntu/Strokes_prediction_BERTHET_NOURAUD_TRIEU/strokes.csv")
    strokes_clean_csv = exists(
        "/home/ubuntu/Strokes_prediction_BERTHET_NOURAUD_TRIEU/Kubernetes_Project/Fastapi/stroke_clean.csv")
    sml = exists(
        "/home/ubuntu/Strokes_prediction_BERTHET_NOURAUD_TRIEU/Kubernetes_Project/Fastapi/regression_model_saved.joblib")
    # 1 Tester si fichier CSV est bien présent
    assert exists(strokes_csv) == True
    assert exists(strokes_clean_csv) == True
    # 2 Si fichier dans lequel on sauvegarde le modèle n'existe pas à la base ?
    assert exists(sml) == True

    # if file_exists == True:
    #     test_status = "SUCCESS"
    # else:
    #     test_status = "FAILURE"

    # output = '''
    #     =================================
    #         CHECK IF CSV IS AVAILABLE
    #     =================================
    #     test date = {test_date}
    #     tested file = {filename}

    #     expected result = True
    #     actual restult = {file_exists}

    #     ==>  {test_status}

    #     '''
    # print(output.format(filename=filename, file_exists=file_exists,
    #       test_status=test_status, test_date=test_date))
    # # Impression dans le fichier de log
    # with open("api_test.log", 'a')as file:
    #     file.write(output.format(
    #         filename=filename,
    #         file_exists=file_exists,
    #         test_status=test_status,
    #         test_date=test_date
    #     ))

# 3 Si on demande les performances avant de générer le modèle ?


def test_perf_avant_model():
    url = 'http://localhost:8000/perf_ML'
    r = requests.get(url)
    assert r.status_code == 200


# 4 Tester si données fausses (text au lieu d'int)
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
