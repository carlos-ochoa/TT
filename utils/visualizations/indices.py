# Distribuciones es una lista de diccionarios con el total de cada grupo a graficar
'''
Ejemplo :
[
    {"value": 235, "name": "Video Ad"},
    {"value": 274, "name": "Affiliate Ad"},
    {"value": 310, "name": "Email marketing"},
    {"value": 335, "name": "Direct access"},
    {"value": 400, "name": "Search engine"},
]
'''

def graficar_indice(title,distribuciones,name,color):
    pie_options = {
        "backgroundColor": "#FFFFFF",
        "title": {
            "text": title,
            "left": "center",
            "top": 20,
            "textStyle": {"color": "#952F57"},
        },
        "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b} : {c} ({d}%)"},
        "visualMap": {
            "show": False,
            "min": 0,
            "max": 600,
            "inRange": {"colorLightness": [0, 1]},
        },
        "series": [
            {
                "name": name,
                "type": "pie",
                "radius": "55%",
                "center": ["50%", "50%"],
                "data": distribuciones,
                "roseType": "radius",
                "label": {"color": "#952F57"},
                "labelLine": {
                    "lineStyle": {"color": "#952F57"},
                    "smooth": 0.2,
                    "length": 10,
                    "length2": 20,
                },
                "itemStyle": {
                    "color": color,
                    "shadowBlur": 200,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                },
                "animationType": "scale",
                "animationEasing": "elasticOut",
            }
        ],
    }
    return pie_options

def graficar_indice2(title,subtitle,distribuciones,name,color):
    options = {
        "title": {"text": title, "subtext": subtitle, "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left",},
        "series": [
            {
                "name": name,
                "type": "pie",
                "radius": "50%",
                "data": distribuciones,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                        "color" : "#952F57"
                    }
                },
            }
        ],
    }
    return options

def graficar_radar(data):
    option = {
        "title": {"text": "Comparativa"},
        "legend": {"data": ["Semestre anterior", "Predicciones del semestre actual"]},
        "radar": {
            "indicator": [
                {"name": "Reprobación", "max": 100},
                {"name": "Deserción", "max": 100},
                {"name": "Eficiencia terminal", "max": 100}
            ]
        },
        "series": [
            {
                "name": "（Semestre anterior vs Predicción actual）",
                "type": "radar",
                "data": [
                    {
                        "value": [23,5.2,80],
                        "name": "Semestre anterior",
                    },
                    {
                        "value": data,
                        "name": "Predicciones del semestre actual",
                    },
                ],
            }
        ],
    }
    return option

def graficar_rose(data):
    option = {
        "legend": {"top": "bottom"},
        "toolbox": {
            "show": True,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": False},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
            },
        },
        "series": [
            {
                "name": "Impacto por nivel",
                "type": "pie",
                "radius": [50, 250],
                "center": ["50%", "50%"],
                "roseType": "area",
                "itemStyle": {"borderRadius": 8},
                "data": data
            }
        ],
    }
    return option