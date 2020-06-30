import requests
import decimal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

IMP_PAIS = decimal.Decimal(1.3)

def calculateDifference(amount, buenbit_daiars, buenbit_daiusd, bank_cot):
  result = amount / buenbit_daiusd
  result = result * buenbit_daiars

  bankResult = amount * bank_cot * IMP_PAIS

  return decimal.Decimal(result - bankResult)

# print('<hr/>')
# print('Cotizacion Santander:' + str(santander_price))
# print('Diferencia Buenbit - Santander 200usd: ' + str(calculateDifference(200,daiars,daiusd,santander_price)))
# print('<hr/>')
# print('Cotizacion Galicia:' + str(galicia_price))
# print('Diferencia Buenbit - Galicia 200usd: ' + str(calculateDifference(200,daiars,daiusd,galicia_price)))
# print('<hr/>')
# print('Cotizacion BBVA:' + str(bbva_price))
# print('Diferencia Buenbit - BBVA 200usd: ' + str(calculateDifference(200,daiars,daiusd,bbva_price)))
# print('<hr/>')

def getDifferencesMessage():
  buenbit_api_url = "https://be.buenbit.com/api/market/tickers/"
  bancos_api_url = "https://www.dolarsi.com/api/api.php?type=capital"

  bancos_req = requests.get(bancos_api_url)
  buenbit_req = requests.get(buenbit_api_url)

  daiusd = decimal.Decimal(buenbit_req.json()['object']['daiusd']['selling_price'])
  daiars = decimal.Decimal(buenbit_req.json()['object']['daiars']['purchase_price'])

  santander_price = 0
  bbva_price = 0
  galicia_price = 0

  for bank in bancos_req.json():
    bank_name = bank['casa']['nombre']
    sell_price = decimal.Decimal(bank['casa']['venta'].replace(',', '.'))
    if bank_name == "Banco Santander":
      santander_price = sell_price
    elif bank_name == "Banco Galicia":
      galicia_price = sell_price
    elif bank_name == "Banco BBVA":
      bbva_price = sell_price

  message = MIMEMultipart("alternative")
  message["Subject"] = "Diferencias cotizaciones"
  message["From"] = 'Diferencia buenbit'
  body = """\
    Diferencia buenbit

    <html>
      <body>
        <h3> Diferencias </h3>
        <hr>
        Cotizacion Santander: <b>%.2f</b>
        Diferencia Buenbit - Santander 200usd: <b>%.2f</b>
        <hr>
        Cotizacion Galicia: <b>%.2f</b>
        Diferencia Buenbit - Galicia 200usd: <b>%.2f</b>
        <hr>
        Cotizacion BBVA: <b>%.2f</b>
        Diferencia Buenbit - BBVA 200usd: <b>%.2f</b>
        <hr>
      </body>
    </html>
    """ % (
      santander_price,
      calculateDifference(200,daiars,daiusd,santander_price),
      galicia_price,
      calculateDifference(200,daiars,daiusd,galicia_price),
      bbva_price,
      calculateDifference(200,daiars,daiusd,bbva_price)
    )

  message.attach(MIMEText(body, "html"))
  return message.as_string().encode('UTF-8')


def getDifferences():
  buenbit_api_url = "https://be.buenbit.com/api/market/tickers/"
  bancos_api_url = "https://www.dolarsi.com/api/api.php?type=capital"

  bancos_req = requests.get(bancos_api_url)
  buenbit_req = requests.get(buenbit_api_url)

  daiusd = decimal.Decimal(buenbit_req.json()['object']['daiusd']['selling_price'])
  daiars = decimal.Decimal(buenbit_req.json()['object']['daiars']['purchase_price'])

  dolar_buenbit = 1/daiusd*daiars
  santander_price = 0
  bbva_price = 0
  galicia_price = 0

  for bank in bancos_req.json():
    bank_name = bank['casa']['nombre']
    sell_price = decimal.Decimal(bank['casa']['venta'].replace(',', '.'))
    if bank_name == "Banco Santander":
      santander_price = sell_price
    elif bank_name == "Banco Galicia":
      galicia_price = sell_price
    elif bank_name == "Banco BBVA":
      bbva_price = sell_price
  return {
    "dolar_buenbit": dolar_buenbit,
    "santander_price": santander_price,
    "bbva_price": bbva_price,
    "galicia_price": galicia_price,
    "santander_difference": calculateDifference(200,daiars,daiusd,santander_price),
    "bbva_difference": calculateDifference(200,daiars,daiusd,bbva_price),
    "galicia_difference": calculateDifference(200,daiars,daiusd,galicia_price)
  }

def getConsoleDifferences():
  data = getDifferences()
  return """\
    Diferencia buenbit
-----------------------------------------------------------------
        Dolar Buenbit: %.2f
-----------------------------------------------------------------
        Cotizacion Santander: %.2f
        Diferencia Buenbit - Santander 200usd: %.2f
-----------------------------------------------------------------
        Cotizacion Galicia: %.2f
        Diferencia Buenbit - Galicia 200usd: %.2f
-----------------------------------------------------------------
        Cotizacion BBVA: %.2f
        Diferencia Buenbit - BBVA 200usd: %.2f
-----------------------------------------------------------------
    """ % (
      data["dolar_buenbit"],
      data["santander_price"],
      data["santander_difference"],
      data["galicia_price"],
      data["galicia_difference"],
      data["bbva_price"],
      data["bbva_difference"]
      
    )


def getHtmlDifferences():
  data = getDifferences()
  message = MIMEMultipart("alternative")
  message["Subject"] = "Diferencias cotizaciones"
  message["From"] = 'Diferencia buenbit'
  body = """\
    Diferencia buenbit

    <html>
      <body>
        <h3> Diferencias </h3>
        <hr>
        Cotizacion Santander: <b>%.2f</b>
        Diferencia Buenbit - Santander 200usd: <b>%.2f</b>
        <hr>
        Cotizacion Galicia: <b>%.2f</b>
        Diferencia Buenbit - Galicia 200usd: <b>%.2f</b>
        <hr>
        Cotizacion BBVA: <b>%.2f</b>
        Diferencia Buenbit - BBVA 200usd: <b>%.2f</b>
        <hr>
        <h2> Cotizacion buenbit: <b>%.2f</b> </h2>
        <hr>
      </body>
    </html>
    """ % (
      data["santander_price"],
      data["santander_difference"],
      data["galicia_price"],
      data["galicia_difference"],
      data["bbva_price"],
      data["bbva_difference"],
      data["dolar_buenbit"]
      
    )

  message.attach(MIMEText(body, "html"))
  return message.as_string().encode('UTF-8')