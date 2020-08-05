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

def getDifferences():
  buenbit_api_url = "https://be.buenbit.com/api/market/tickers/"
  bancos_api_url = "https://www.dolarsi.com/api/api.php?type=capital"
  pluscambio_api_url = "https://api.pluscambio.com.ar/currencies"

  bancos_req = requests.get(bancos_api_url)
  buenbit_req = requests.get(buenbit_api_url)
  pluscambio_req = requests.get(pluscambio_api_url)

  daiusd = decimal.Decimal(buenbit_req.json()['object']['daiusd']['selling_price'])
  daiars = decimal.Decimal(buenbit_req.json()['object']['daiars']['purchase_price'])

  pluscambio_price = decimal.Decimal(pluscambio_req.json()[0]['sell'])

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
  dolares_vender_buenbit_santander = 200* IMP_PAIS * decimal.Decimal(73.75) / daiars * daiusd
  return {
    "dolar_buenbit": dolar_buenbit,
    "santander_price": santander_price,
    "bbva_price": bbva_price,
    "galicia_price": galicia_price,
    "pluscambio_price": pluscambio_price,
    "santander_difference": calculateDifference(200,daiars,daiusd,santander_price),
    "bbva_difference": calculateDifference(200,daiars,daiusd,bbva_price),
    "galicia_difference": calculateDifference(200,daiars,daiusd,galicia_price),
    "pluscambio_difference": calculateDifference(200,daiars,daiusd,pluscambio_price),
    "vender_santander": dolares_vender_buenbit_santander,
  }

def getConsoleDifferences():
  data = getDifferences()
  return """\
    Diferencia buenbit
-----------------------------------------------------------------
        Dolar Buenbit: %.2f
        Dolares a vender para 200 usd Santander: %.2f
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
        Cotizacion PlusCambio: %.2f
        Diferencia Buenbit - PlusCambio 200usd: %.2f
-----------------------------------------------------------------
    """ % (
      data["dolar_buenbit"],
      data["vender_santander"],
      data["santander_price"],
      data["santander_difference"],
      data["galicia_price"],
      data["galicia_difference"],
      data["bbva_price"],
      data["bbva_difference"],
      data["pluscambio_price"],
      data["pluscambio_difference"]
      
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
        Cotizacion PlusCambio: <b>%.2f</b>
        Diferencia Buenbit - PlusCambio 200usd: <b>%.2f</b>
        <hr>
        <h2> Cotizacion buenbit: <b>%.2f</b> </h2>
        <h2> Dolares a vender para 200 usd Santander: <b>%.2f</b> </h2>
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
      data["pluscambio_price"],
      data["pluscambio_difference"],
      data["dolar_buenbit"],
      data["vender_santander"]
      
    )

  message.attach(MIMEText(body, "html"))
  return message.as_string().encode('UTF-8')