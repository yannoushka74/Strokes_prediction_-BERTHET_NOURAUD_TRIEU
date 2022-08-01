from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ML import generate_ml, perf_ml, stroke_predict
import pandas as pd

api = FastAPI(
    title='My API ML',
    description="My own API ML powered by FastAPI.",
    version="1.0.1")

# fichier dans lequel le modèle de ML est sauvegardé une fois généré
saved_ml_file = 'regression_model_saved.joblib'


class Patient(BaseModel):
    """ Classe comportant les données utiles d'un patient pour déterminer son stroke
        - age
        - problème d'hypertension : 0 (non), 1 (oui)
        - Maladie du coeur : 0 (non), 1 (oui)
        - Déjà marié ? : 0 (non), 1 (oui)
        - Type de résidence : 0 (rural), 1 (urbain)
        - Taux de glucose
        - bmi : indice de masse corporel
    """
    age: float
    hypertension: int
    heart_disease: int
    ever_married: int
    Residence_type: int
    avg_glucose_level: float
    bmi: float


@api.get('/status')
def get_status():
    """ Retourne 1 si l'API fonctionne correctement
    """
    return "1"


@api.get('/save_ML')
def get_generate_ml():
    """Si le ML n'a pas encore été sauvegardé dans un fichier, génère le ML et sauvegarde dans saved_ml_file.
    Retourne le nom du fichier dans lequel le ML est sauvegardé
    """
    try:
        with open(saved_ml_file):
            # pass
            return 'Modèle déjà sauvegardé dans {smf}.'.format(smf=saved_ml_file)
    except IOError:
        print(generate_ml('stroke_clean.csv', saved_ml_file))
        return 'Modèle sauvegardé dans {smf}.'.format(smf=saved_ml_file)


@api.get('/perf_ML')
def get_perf_ml():
    """
    Si le ML n'a pas encore été sauvegardé dans un fichier, génère le ML et sauvegarde dans saved_ml_file.
    Retourne la précision du modèle de ML
    """
    get_generate_ml()
    return 'performance du modèle :{perf}'.format(perf=perf_ml(saved_ml_file))


@api.post('/stroke')
def post_predict_patient(patient: Patient):
    """
    Prédit à partir du ML si le patient aura une crise cardiaque ou pas
    :param patient : patient pour lequel on veut prédire le stroke
    :return : la prédiction pour la variable stoke
    """
    try:
        get_generate_ml()
        data = [patient.age, patient.hypertension, patient.heart_disease, patient.ever_married,
                patient.Residence_type, patient.avg_glucose_level, patient.bmi]
        x_patient = pd.DataFrame([data], columns=['age', 'hypertension', 'heart_disease', 'ever_married',
                                                  'Residence_type', 'avg_glucose_level', 'bmi'])
        stroke = stroke_predict(x_patient, saved_ml_file)
        if stroke == 1:
            return 'Le patient aura une crise cardiaque'
        else:
            return "Le patient n'aura pas de crise cardiaque"
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='bad Type')
