from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import backtrader as bt
from .strategy import ThreeCandlePatternStrategy
import pandas as pd


# Create your views here.

def ejecutar_backtest(request):
    #if __name__ == "__main__":
        cerebro = bt.Cerebro()

    # Agregar un feed de datos (puedes usar tus propios datos aquí)
        archivo_csv = 'dataaa.csv'

    # Cargar los datos en un DataFrame de pandas
        df = pd.read_csv(archivo_csv, sep=';', header=None, names=['datetime', 'open', 'high', 'low', 'close', 'volume'])

    # Añadir milisegundos a la columna 'datetime'
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d%m%Y %H%M%S')

    # Establecer la columna 'datetime' como índice de tiempo
        df.set_index('datetime', inplace=True)
        df = df[::-1]

    # Convertir las columnas numéricas a tipo float
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        data_feed = bt.feeds.PandasData(dataname=df)

        cerebro.adddata(data_feed)

    # Agregar la estrategia al cerebro
        cerebro.addstrategy(ThreeCandlePatternStrategy)
        broker = bt.brokers.BrokerBack()
        broker.setcash(10000000.00)
        cerebro.setbroker(broker)
    
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='misanalisis')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='midrawdown')
        #print(data_feed)

    

    # Ejecutar el backtest
        thestrats = cerebro.run()
        thestrat = thestrats[0]
    
    
        print("Picos detectados:")
        

        for peak in cerebro.runstrats[0][0].resistenciaBuy:
            print(f"Pico: {peak:.2f}")

        print(cerebro.runstrats[0][0].valorInicialCartera)
        print(cerebro.runstrats[0][0].valorFinalCartera)

        calculo = (cerebro.runstrats[0][0].valorFinalCartera - cerebro.runstrats[0][0].valorInicialCartera) / cerebro.runstrats[0][0].valorInicialCartera * 100
        print(calculo)
    
        print('estadisticas:', thestrat.analyzers.misanalisis.print())
        print('drawdown:', thestrat.analyzers.midrawdown.print())

        #cerebro.plot(style="candlestick")
        return render(request, 'resultados.html',{'valorfinal': cerebro.runstrats[0][0].valorFinalCartera,
                                                  'valorinicial': cerebro.runstrats[0][0].valorInicialCartera,
                                                  'calculo': calculo,     
                                                   'drawdown': thestrat.analyzers.midrawdown.get_analysis(), 
                                                   'misanalisis': thestrat.analyzers.misanalisis.get_analysis()})

def home(request):
      return render(request, 'home.html')