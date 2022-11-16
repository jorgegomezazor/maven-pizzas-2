import pandas as pd
import numpy as np
def extract():
    order_details = pd.read_csv('order_details.csv', encoding='latin1', sep=';')
    orders = pd.read_csv('orders.csv', encoding='latin1',sep=';')
    pizza_types = pd.read_csv('pizza_types.csv',encoding='latin1',sep=',')
    return  order_details, orders, pizza_types
def analisis_nulls(order_details, orders, pizza_types):
    analisis = [order_details, orders, pizza_types]
    for df in analisis:
        df.info()
    return
def limpiar_datos(order_details, orders):
    order_details = order_details.dropna()
    order_details = order_details.drop(columns=['order_details_id','order_id'])
    pd.set_option('mode.chained_assignment', None)
    for i in range(1,len(order_details['pizza_id'])):
        try:
            # input(order_details['pizza_id'][i])
            m = order_details['pizza_id'][i]
            palabra = ''
            for l in range(len(m)):
                if m[l] =='@':
                    palabra += 'a'
                elif m[l] == '0':
                    palabra += 'o'
                elif m[l] == '-':
                    palabra += '_'
                elif m[l] == ' ':
                    palabra += '_'
                elif m[l] == '3':
                    palabra += 'e'
                else:
                    palabra += m[l]
            order_details['pizza_id'][i] = order_details['pizza_id'][i].replace(m,palabra)
            # input(order_details['pizza_id'][i])
        except:
            #elimino la fila que no se pudo limpiar
            try:
                order_details = order_details.drop(i)
            except:
                pass
    print(order_details.head())
    return order_details, orders
def transform(order_details, orders, pizza_types):
    pizza = {}
    for i in range(len(pizza_types)):
        pizza[pizza_types['pizza_type_id'][i]] = pizza_types['ingredients'][i]
    pedidos = []
    for p in range(1,len(order_details)-1):
        try:
            for i in range(int(order_details['quantity'][p])):
                pedidos.append(order_details['pizza_id'][p])
        except:
            pass
    ingredientes_anuales = {}
    for i in range(len(pizza_types)):
        ingreds = pizza_types['ingredients'][i]
        ingreds = ingreds.split(', ')
        for ingrediente in ingreds:
            ingredientes_anuales[ingrediente] = 0      
    print(len(pedidos))
    for p in pedidos:
        ing = 0
        tamano = 0
        if p[-1] == 's':
            ing = 1
            tamano = 2
        elif p[-1] == 'm':
            ing = 2
            tamano = 2
        elif p[-1] == 'l':
            if p[-2] == 'x':
                if p[-3] == 'x':
                    ing = 5
                    tamano = 4
                else:
                    ing = 4
                    tamano = 3
            else:
                ing = 3
                tamano = 2
        ings = pizza[p[:-tamano]].split(', ')
        for ingrediente in ings:
            ingredientes_anuales[ingrediente] += ing
    prediccion_semanal = []
    p_s = ingredientes_anuales
    for i in p_s:
        p_s[i] = int(np.ceil(p_s[i]/52))
    for _ in range(52):
        prediccion_semanal.append(p_s)
    return prediccion_semanal
def load(diccs):
    df = pd.DataFrame(diccs)
    print(df)
    df.to_csv('prediccion_semanal.csv')

if __name__ == '__main__':
    order_details, orders, pizza_types = extract()
    analisis_nulls(order_details,orders,pizza_types)
    order_details, orders = limpiar_datos(order_details,orders)
    diccs = transform(order_details, orders,pizza_types)
    load(diccs)
