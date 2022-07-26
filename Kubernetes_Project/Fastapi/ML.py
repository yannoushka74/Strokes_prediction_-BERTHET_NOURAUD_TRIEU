from imblearn.over_sampling import RandomOverSampler
import warnings
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from joblib import dump, load


# génération du ML à partir de fichier_csv et enregistrement dans saved_ml_file
def generate_ml(fichier_csv, saved_ml_file):
    df = pd.read_csv(fichier_csv, index_col="id")

    # On ne conserve que les variables d'observation les plus corrélées.
    df = df.drop(["gender", "work_type", "smoking_status"], axis=1)

    # On remplace les valeurs NA par le mean de la colonne bmi
    df_new = df.copy()
    df_new.loc[:, "bmi"] = df["bmi"].fillna(df["bmi"].mean())

    # On remplace également les valeurs Unknown par le mode de la colonne
    df_new = df_new.replace("Unknown", np.NaN)
    # df_new["smoking_status"] = df_new["smoking_status"].fillna(df_new["smoking_status"].mode()[0])

    # Numérisation des variables catégorielle pour les utiliser dans un algo de ML
    # binarisation des variables catégorielles non hiérarchisées avec plus de 2 valeurs possibles
    #df_rl = pd.get_dummies(df_new, prefix=['g', 'wt', 'ss'], columns=['gender', 'work_type', 'smoking_status'],
    #                       drop_first=True)

    # Numérisation des variables catégorielles binaires
    df_new.ever_married.replace(['Yes', 'No'], [0, 1], inplace=True)
    df_new.Residence_type.replace(['Rural', 'Urban'], [0, 1], inplace=True)

    # Séparation des données en variables explicatives et variable cible
    X = df_new.drop("stroke", axis=1)
    y = df_new.stroke

    # Standardisation des données
    # On instancie StandardScaler
    scaler = StandardScaler()
    X_scaled_ = scaler.fit(X).transform(X)
    X_scaled = pd.DataFrame(X_scaled_)

    # Séparation des données en jeu de d'entrainement et de test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
    # Sur-échantillonnage
    rOs = RandomOverSampler(sampling_strategy='minority')
    X_ro, y_ro = rOs.fit_resample(X_train, y_train)

    # Régression Logistique
    warnings.filterwarnings('ignore')

    # Détermination des hyperparamètres du modèle les plus optimum
    parameters = {
        'penalty': ['l1', 'l2'],  # l1 lasso l2 ridge
        'C': np.logspace(-3, 3, 7),
        'solver': ['newton-cg', 'lbfgs', 'liblinear'],
    }

    logreg = LogisticRegression()
    lr1 = GridSearchCV(logreg, param_grid=parameters, scoring='accuracy', cv=7)

    # Entraînement du modèle de régression logistique
    lr1.fit(X_ro, y_ro)

    # Sauvegarde du modèle de ML dans saved_ml_file
    dump(lr1, saved_ml_file)


# Retourne les performances du ML stocké dans saved_ml_file
def perf_ml(saved_ml_file):
    reg_loaded = load(saved_ml_file)
    return reg_loaded.best_score_


# Prédiction de la variable stroke pour un patient à partir du ML enregistré dans saved_ml_file
def stroke_predict(x_patient, saved_ml_file):
    reg_loaded = load(saved_ml_file)
    y_pred = reg_loaded.predict(x_patient)
    return y_pred[0]
