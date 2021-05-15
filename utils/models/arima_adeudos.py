import statsmodels.api as sm

def modelo_materia(datos_agrupados):
     modelo = sm.tsa.ARIMA(datos_agrupados, order=(1, 0, 0))  
     resultados = modelo.fit(disp=-1)
     forecast=resultados.forecast(steps=1, exog=None, alpha=0.05)
     return forecast[0]
