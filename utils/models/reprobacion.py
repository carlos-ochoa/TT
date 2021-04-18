from sklearn.externals import joblib

class ClasificadorBajas:

    def __init__(self):
        self.model = joblib.load('ClasificadorKnnIndiceReprobacion.pkl')

    def predict()
