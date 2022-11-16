import pandas as pd
import numpy as np
def extract(): # Función que extrae los datos
    order_details = pd.read_csv('order_details.csv', encoding='latin1', sep=';') # Leo el archivo order_details.csv
    orders = pd.read_csv('orders.csv', encoding='latin1',sep=';') # Leo el archivo orders.csv
    pizza_types = pd.read_csv('pizza_types.csv',encoding='latin1',sep=',') # Leo el archivo pizza_types.csv
    return  order_details, orders, pizza_types
def analisis_nulls(order_details, orders, pizza_types): # Función que analiza los nulls
    analisis = [order_details, orders, pizza_types] # Creo una lista con los dataframes
    for df in analisis:
        df.info() # Imprimo la información de cada dataframe
    return
def limpiar_datos(order_details, orders):
    order_details = order_details.dropna() # Elimino los nulls de order_details
    order_details = order_details.drop(columns=['order_details_id','order_id']) # Elimino las columnas que no me sirven
    pd.set_option('mode.chained_assignment', None) # Deshabilito el warning SettingWithCopyWarning
    for i in range(1,len(order_details['pizza_id'])):
        try:
            m = order_details['pizza_id'][i]
            palabra = ''
            for l in range(len(m)):
                if m[l] =='@':
                    palabra += 'a' # Reemplazo las @ por a
                elif m[l] == '0':
                    palabra += 'o' # Reemplazo los 0 por o
                elif m[l] == '-':
                    palabra += '_' # Reemplazo los - por _
                elif m[l] == ' ':
                    palabra += '_' # Reemplazo los espacios por _
                elif m[l] == '3':
                    palabra += 'e' # Reemplazo los 3 por e
                else:
                    palabra += m[l] # Si no es ninguna de las anteriores, la agrego tal cual
            order_details['pizza_id'][i] = order_details['pizza_id'][i].replace(m,palabra)  # Reemplazo la palabra por la nueva
        except:
            #elimino la fila que no se pudo limpiar
            try:
                order_details = order_details.drop(i)
            except:
                pass
    return order_details, orders
def transform(order_details, orders, pizza_types):
    pizza = {}
    for i in range(len(pizza_types)):
        pizza[pizza_types['pizza_type_id'][i]] = pizza_types['ingredients'][i] # Creo un diccionario con los ingredientes de cada pizza
    pedidos = []
    for p in range(1,len(order_details)-1):
        try:
            for i in range(int(order_details['quantity'][p])):
                pedidos.append(order_details['pizza_id'][p]) # Creo una lista con los pedidos anuales teniendo en cuenta la cantidad de cada uno
        except:
            pass
    ingredientes_anuales = {} # Creo un diccionario con los ingredientes anuales
    for i in range(len(pizza_types)):
        ingreds = pizza_types['ingredients'][i]  
        ingreds = ingreds.split(', ') # Separo los ingredientes por comas
        for ingrediente in ingreds:
            ingredientes_anuales[ingrediente] = 0 # Agrego los ingredientes al diccionario   
    for p in pedidos:
        ing = 0
        tamano = 0
        if p[-1] == 's': #Si la pizza es s hay un ingrediente de cada
            ing = 1
            tamano = 2
        elif p[-1] == 'm': #Si la pizza es m hay dos ingredientes de cada
            ing = 2
            tamano = 2
        elif p[-1] == 'l':
            if p[-2] == 'x': 
                if p[-3] == 'x': #Si la pizza es xxl hay cinco ingredientes de cada
                    ing = 5
                    tamano = 4
                else: #Si la pizza es xl hay cuatro ingredientes de cada
                    ing = 4
                    tamano = 3
            else: #Si la pizza es l hay tres ingredientes de cada
                ing = 3
                tamano = 2
        ings = pizza[p[:-tamano]].split(', ')
        for ingrediente in ings:
            ingredientes_anuales[ingrediente] += ing # Agrego los ingredientes al diccionario
    prediccion_semanal = [] # Creo una lista con los ingredientes que se van a pedir en la semana
    p_s = ingredientes_anuales
    for i in p_s:
        p_s[i] = int(np.ceil(p_s[i]/52)) # Redondeo para arriba y divido por 52 para saber cuantos ingredientes se van a pedir por semana
    for _ in range(52):
        prediccion_semanal.append(p_s)
    return prediccion_semanal
def load(diccs):
    df = pd.DataFrame(diccs) # Creo un dataframe con los diccionarios
    print(df) 
    df.to_csv('prediccion_semanal.csv') # Guardo el dataframe en un archivo csv

if __name__ == '__main__':
    order_details, orders, pizza_types = extract()
    analisis_nulls(order_details,orders,pizza_types)
    order_details, orders = limpiar_datos(order_details,orders)
    diccs = transform(order_details, orders,pizza_types)
    load(diccs)
'''
Mi predicción se basa en que se va a pedir la misma cantidad de ingredientes que se pidió en el año anterior,
por lo tanto divido la cantidad de ingredientes entre 52 para saber cuantos ingredientes se van a pedir por semana.
'''