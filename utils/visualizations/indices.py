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

def graficar_indice(title,distribuciones):
    pie_options = {
        "backgroundColor": "#2c343c",
        "title": {
            "text": title,
            "left": "center",
            "top": 20,
            "textStyle": {"color": "#ccc"},
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
                "name": "Estado de baja",
                "type": "pie",
                "radius": "55%",
                "center": ["50%", "50%"],
                "data": distribuciones,
                "roseType": "radius",
                "label": {"color": "rgba(255, 255, 255, 0.3)"},
                "labelLine": {
                    "lineStyle": {"color": "rgba(255, 255, 255, 0.3)"},
                    "smooth": 0.2,
                    "length": 10,
                    "length2": 20,
                },
                "itemStyle": {
                    "color": "#c23531",
                    "shadowBlur": 200,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                },
                "animationType": "scale",
                "animationEasing": "elasticOut",
            }
        ],
    }
    return pie_options
