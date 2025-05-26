#Este programa se crea asumiendo un día de análisis que se hace, no análisis de más de un día: es decir, toda una semana, un mes o más tiempo. De ahí que su eficiencia es medida solo diariamente y para de contar.


import random as rd
import tkinter as tk
import math
from PIL import ImageTk
import FuncionesParaElParcial as fpp
from tkinter.scrolledtext import ScrolledText
import io
import os
import pandas as pd
from tkinter import messagebox
from tkinter import ttk

ventana = tk.Tk()
ventana.geometry("700x414")
ventana.resizable(False, False)
ventana.title("Calidad de la mano de obra")

ficheros = ttk.Notebook(ventana)
ficheros.pack()

dict_producido= {
    "Id operario":[],
    "Nombre del operario":[],
    "Pan Francés":[],
    "Random Francés":[],
    "Pan de queso":[],
    "Random queso":[],
    "Croissants":[],
    "Random croissant":[],
    "Complejidad final":[],
    "Cumple meta":[]
}

#Estadísticas diarias

def registrar_usuario():

  global dict_producido

  dict_producido["Id operario"].append(id_operario.get().strip()) #"-- #####################3
  dict_producido["Nombre del operario"].append(nombre_operario.get().strip()) ##--#####################
  dict_producido["Pan Francés"].append(pan_frances.get())#--####################
  dict_producido["Pan de queso"].append(pan_queso.get()) #--####################
  dict_producido["Croissants"].append(croissants.get()) #--#######################

  random_pan_frances=rd.uniform(1.0, 1.5)
  random_pan_queso=rd.uniform(1.0, 1.5)
  random_croissants=rd.uniform(1.0, 1.5)

  dict_producido["Random Francés"].append(random_pan_frances)#--####################
  dict_producido["Random queso"].append(random_pan_queso) #--####################
  dict_producido["Random croissant"].append(random_croissants) #--#######################

  lista_random=[random_pan_frances, random_pan_queso, random_croissants]

  calculo_eficiencia=((pan_frances.get()*random_pan_frances)+(pan_queso.get()*random_pan_queso)+(croissants.get()*random_croissants))/sum(lista_random)

  dict_producido["Complejidad final"].append(round(calculo_eficiencia))

  if calculo_eficiencia <300:
    dict_producido["Cumple meta"].append("No cumple")
  else:
    dict_producido["Cumple meta"].append("Sí cumple")

  


def mostrar_imagenes(pil_img):
  image_tk = ImageTk.PhotoImage(pil_img)
  frame_imagen.configure(image=image_tk) #--######################
  frame_imagen.image = image_tk #--##########################

def mostrar_imagenes_pie(pil_img):
  image_tk = ImageTk.PhotoImage(pil_img)
  frame_imagen_pie.configure(image=image_tk) #--######################
  frame_imagen_pie.image = image_tk #--##########################



def buscar_usuario():

  try:
    indice=dict_producido["Id operario"].index(id_operario_buscar.get())
    etiqueta_eficiencia.set(dict_producido["Complejidad final"][indice]) ##--########################
    etiqueta_cumple.set(dict_producido["Cumple meta"][indice]) #--#########################

    dict_temporal={
        "Tipo de pan": ["Pan Francés", "Pan de queso", "Croissants"],
        "C. producida": [dict_producido["Pan Francés"][indice], dict_producido["Pan de queso"][indice], dict_producido["Croissants"][indice]],
        "Eficiencia": [dict_producido["Random Francés"][indice], dict_producido["Random queso"][indice], dict_producido["Random croissant"][indice]]
        }  

    data_frame_pan=pd.DataFrame(dict_temporal)    

    img_barras = fpp.AnalizarConBarras(data_frame_pan).graficar_barras()
    mostrar_imagenes(img_barras)

  except IndexError:
    messagebox.showerror("No se encontró el usuario")
    

  
def actualizar_reporte_gen():

    global dict_producido

    try:
        table_area.delete("1.0", tk.END) ##--#####################
        buffer = io.StringIO()
        DataFrame = pd.DataFrame(dict_producido)
        texto_imprimir = DataFrame.to_string()
        buffer.write(texto_imprimir)
        imprimir = buffer.getvalue()
        table_area.insert(tk.END, imprimir)

        data_frame_general = pd.DataFrame(dict_producido)

        img_pastelisimo = fpp.AnalizarConPastelisimo(data_frame_general).graficar_pastelisimo()
        mostrar_imagenes_pie(img_pastelisimo)


        label_promedio.set(DataFrame["Complejidad final"].mean())

    except ValueError:
        messagebox.showerror("¿Qué pretendes amix? No hay nada que mostrar todavía")


######################################################################################################

ficha_registrar_prod = tk.Frame(ficheros, width=427, height=414)


ficha_estadisticas = tk.Frame(ficheros, width=700, height=414 )

ficheros.add(ficha_registrar_prod, text= "Registrar producción")
ficheros.add(ficha_estadisticas, text= "Estadísticas")

frame_lateral_izquierdo = tk.Frame(ficha_registrar_prod, width=273, height=414)#superior
frame_lateral_izquierdo.pack(side=tk.LEFT, fill= tk.Y)

frame_registro= tk.Frame(frame_lateral_izquierdo, width=273, height=227) #subframe menor
frame_registro.pack(side=tk.TOP)

frame_report_indiv = tk.Frame(frame_lateral_izquierdo, width=273, height=187) #subframe menor
frame_report_indiv.pack(side=tk.BOTTOM)

frame_lateral_derecho_big = tk.Frame(ficha_registrar_prod, width=427, height=414) #superior
frame_lateral_derecho_big.pack(side=tk.RIGHT)

frame_lat_inf_der = tk.Frame(frame_lateral_derecho_big, width=427, height=187) #Subframe menor
frame_lat_inf_der.pack(side=tk.BOTTOM)

frame_lat_sup_der = tk.Frame(frame_lateral_derecho_big, width=427, height=227) #Subframe menor
frame_lat_sup_der.pack(side=tk.TOP)

########### campo de ingreso de registros

label_frame_registro = tk.LabelFrame(frame_registro, text="Registrar producción", width=260, height=198)
label_frame_registro.pack(padx=5, pady=5)
label_frame_registro.pack_propagate(False)

frame_boton_regis = tk.Frame(label_frame_registro, width=257, height=35)
frame_boton_regis.pack(side=tk.BOTTOM)
frame_boton_regis.pack_propagate(False)

boton_registro = tk.Button(frame_boton_regis, text="Registrar producción", width=30, command=registrar_usuario)
boton_registro.pack(pady=3)

###______________________________________

frame_reg_izquier=tk.Frame(label_frame_registro, width=130, height=133)
frame_reg_izquier.pack(side=tk.LEFT, anchor="n", pady=2)

frame_reg_derec=tk.Frame(label_frame_registro, width=129, height=133)
frame_reg_derec.pack(side=tk.RIGHT, anchor="n", pady=1)

etiq_nombre_oper = tk.Label(frame_reg_izquier, text= "Id. operario:")
etiq_nombre_oper.pack(anchor="w")

id_operario = tk.StringVar()
id_operario_entry=tk.Entry(frame_reg_derec, textvariable=id_operario, width=110)
id_operario_entry.pack(anchor="e",padx=4, pady=3)

etiq_nombre_operario = tk.Label(frame_reg_izquier, text="Nombre operario:")
etiq_nombre_operario.pack(anchor="w", pady=2)

nombre_operario = tk.StringVar()
nombre_operario_entry=tk.Entry(frame_reg_derec, textvariable=nombre_operario, width=110)
nombre_operario_entry.pack(anchor="e",padx=4, pady=3)

etiq_pan_frances = tk.Label(frame_reg_izquier, text="Pan francés:")
etiq_pan_frances.pack(anchor="w", pady=2)

pan_frances = tk.DoubleVar()
pan_frances_entry=tk.Entry(frame_reg_derec, textvariable=pan_frances, width=110)
pan_frances_entry.pack(anchor="e",padx=3)

etiq_pan_queso = tk.Label(frame_reg_izquier, text="Pan queso:")
etiq_pan_queso.pack(anchor="w", pady=1)

pan_queso = tk.DoubleVar()
pan_queso_entry=tk.Entry(frame_reg_derec, textvariable=pan_queso, width=110)
pan_queso_entry.pack(anchor="e",padx=4, pady=3)

etiq_croissant = tk.Label(frame_reg_izquier, text="Croissant:")
etiq_croissant.pack(anchor="w")

croissants = tk.DoubleVar()
croissant_entry=tk.Entry(frame_reg_derec, textvariable=croissants, width=110)
croissant_entry.pack(anchor="e",padx=4, pady=2)


########## campo de búsqueda individual

label_frame_busqueda = tk.LabelFrame(frame_report_indiv, text="Reporte individual", width=260, height=170)
label_frame_busqueda.pack(padx=5, pady=5)
label_frame_busqueda.pack_propagate(False)

fram_bus_inf = tk.Frame(label_frame_busqueda, width=259, height=107)
fram_bus_inf.pack(side=tk.BOTTOM)
fram_bus_inf.pack_propagate(False)

frame_bus_sup = tk.Frame(label_frame_busqueda, width=259, height=80)
frame_bus_sup.pack(side=tk.TOP)
frame_bus_sup.pack_propagate(False)

fram_b_inf_iz = tk.Frame(fram_bus_inf, width=129, height=107)
fram_b_inf_iz.pack(side=tk.LEFT, fill=tk.Y)

etiq_eficiencia = tk.Label(fram_b_inf_iz, text="Eficiencia final:")
etiq_eficiencia.pack(side=tk.TOP, anchor="w")

etiqueta_eficiencia=tk.DoubleVar()
etiq_eficiencia=tk.Label(fram_b_inf_iz, text="", textvariable=etiqueta_eficiencia)
etiq_eficiencia.pack(side=tk.TOP, pady=4)

etiqueta_cumple=tk.StringVar()
etiq_cumple=tk.Label(fram_b_inf_iz, text="", textvariable=etiqueta_cumple)
etiq_cumple.pack(side=tk.LEFT)

fram_b_inf_der = tk.Frame(fram_bus_inf, width=129, height=107)
fram_b_inf_der.pack(side=tk.RIGHT, fill=tk.Y)

boton_buscar= tk.Button(fram_b_inf_der, text="Buscar", command=buscar_usuario)
boton_buscar.pack(side=tk.TOP, anchor="e", padx=4)

fram_b_sup_iz = tk.Frame(frame_bus_sup, width=129, height=75)
fram_b_sup_iz.pack(side=tk.LEFT, fill=tk.Y)

fram_b_sup_der = tk.Frame(frame_bus_sup, width=129, height=75)
fram_b_sup_der.pack(side=tk.LEFT, fill=tk.Y)

etiq_buscar_operario= tk.Label(fram_b_sup_iz, text="Busc. id. Operario:")
etiq_buscar_operario.pack(side=tk.LEFT)

id_operario_buscar=tk.StringVar()
operario_buscar_entry=tk.Entry(fram_b_sup_der, textvariable=id_operario_buscar)
operario_buscar_entry.pack(side=tk.RIGHT, anchor="e", padx=4)


#tk.Label(fram_b_inf_iz, text="Nombre del buscado").pack() #Prueba
#tk.Label(label_frame_busqueda, text="Nombre del buscado").pack() #Prueba

######## Campo del gráfico

label_frame_grafico = tk.LabelFrame(frame_lat_inf_der, text="Medidores del operario", width=415, height=171)
label_frame_grafico.pack(padx=5, pady=5)
label_frame_grafico.pack_propagate(False)


frame_imagen= tk.Label(label_frame_grafico)
frame_imagen.pack()

######### campo de reporte general

label_frame_reporte = tk.LabelFrame(frame_lat_sup_der, text="Reporte general", width=415, height=199)
label_frame_reporte.pack(padx=5, pady=5)
label_frame_reporte.pack_propagate(False)

frame_rep_izq = tk.Frame(label_frame_reporte, width=213, height=198)
frame_rep_izq.pack(side=tk.LEFT, fill=tk.Y)
frame_rep_izq.pack_propagate(False)

boton_actualizar=tk.Button(frame_rep_izq, text="Actualizar listado", command=actualizar_reporte_gen)
boton_actualizar.pack(side=tk.TOP, anchor="w", padx=3, pady=3)

table_area=ScrolledText(frame_rep_izq, width=192, height=167)
table_area.pack(side=tk.BOTTOM, anchor="s", pady=5, padx=5)

frame_rep_der = tk.Frame(label_frame_reporte, width=212, height=198)
frame_rep_der.pack(side=tk.RIGHT, fill=tk.Y, padx=2, pady=2)
frame_rep_der.pack_propagate(False)

fra_rep_der_izq_sup =tk.Frame(frame_rep_der, width=103, height=40)
fra_rep_der_izq_sup.pack(side=tk.TOP, anchor="w")
fra_rep_der_izq_sup.pack_propagate(False)

etiq_promedio = tk.Label(fra_rep_der_izq_sup, text="Promedio:")
etiq_promedio.place(x=4, y=3)

fra_rep_der_inf = tk.Frame(frame_rep_der, width=212, height=202)
fra_rep_der_inf.pack(side=tk.BOTTOM, anchor="s")
fra_rep_der_inf.pack_propagate(False)

frame_imagen_pie =tk.Label(fra_rep_der_inf) ###Grafico circular
frame_imagen_pie.pack()

fra_rep_der_der_sup=tk.Frame(frame_rep_der, width=107, height=40)
fra_rep_der_der_sup.place(x=105, y=0)
fra_rep_der_der_sup.pack_propagate(False)

label_promedio=tk.DoubleVar()
etiq_label_promedio=tk.Label(fra_rep_der_der_sup, text="", textvariable=label_promedio)
etiq_label_promedio.place(x=0, y=2)






ventana.mainloop()
