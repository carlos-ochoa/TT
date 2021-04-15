from sklearn.externals import joblib

class ClasificadorBajas:

    def __init__(self):
        self.model = joblib.load('dt_bajas_model.pkl')

    def predict()