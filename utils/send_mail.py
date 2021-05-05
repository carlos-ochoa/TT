import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send(destinatario, password):
    message = Mail(
        from_email='neurokratos.electoral@gmail.com',
        to_emails=destinatario,
        subject='Acceso',
        html_content="<!DOCTYPE html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>   <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>   <title>Acceso al Sitio</title>   <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css' integrity='sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l' crossorigin='anonymous'>   <link rel='stylesheet' href='https://unpkg.com/leaflet@1.0.1/dist/leaflet.css' />   <script type='text/javascript' src='https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js'></script><style>body{  background-color: #FFFFFF;} .colorM{    background-color: #7887C6;}.Wcard{    width: 40em;}.img{    width: 100px;}.cardT{    font-size: 1.8rem;}.cardText{    font-size: 1.2rem;}.cardSub{    font-size: 1.5rem;}.textColor{    color: #7887C6;}.colCard{    display: flex;    flex-direction: column;}.espDatos{    line-height: 2.5rem;}.btnRegistro{    border-radius: 6px;    width: 20rem;}.btnContraseña{    border-radius: 6px;    width: 25rem;}.iconos{    width: 100px;    height: 100px;}.d-Contraseña{    display: flex;    flex-direction: column;    align-items: center;}.newPass{    font-size: 2rem;    color: #7887C6;}.newSuccess{    font-size: 1.3rem;}</style></head><body>          <!-- Nueva contraseña -->          <div>            <div class='card mx-auto Wcard'>              <div class='card-header d-flex justify-content-between colorM'>                                     </div>              <div class='card-body p-4 d-Contraseña'>                                <h5 class='card-title font-weight-bold pt-2 cardText'>¡Bienvenido!</h5>                <p class='card-text text-center newSuccess'>                    Su contraseña es:                </p>                <p class='card-text text-center font-weight-bolder newPass'>"+ password +"</p>                <a                     class='btn text-white mt-2 font-weight-bold btnContraseña colorM'                    >                      Ir al Sitio     </a>              </div>            </div>          </div></body></html>")
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)