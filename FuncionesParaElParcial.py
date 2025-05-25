#documento FuncionesParaElParcial

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

sns.set_theme()

def pasar_a_pil(grafico):
  buffer = io.BytesIO() #Vincula a un método de io
  canvas = FigureCanvasAgg(grafico) #vincaula a un método de FigureCanvas y usará la figura para crear un canvas
  canvas.draw()
  canvas.print_png(buffer)
  buffer.seek(0)
  return Image.open(buffer) #abre lo que hay en el buffer


class AnalizarConBarras:

  #variables de trabajo (obligatorias): 
  def __init__(self, data_frame_pan):
    self.df=data_frame_pan

  def graficar_barras(self):

    grafico, ax = plt.subplots(1, 2, figsize=(4.0,1.6), dpi=100) #start
  
    sns.barplot(data= self.df, x="C. producida" , y="Tipo de pan", ax=ax[0])
    ax[0].set_title("Producción del operario por tipo de pan")
    ax[0].set_xlabel("C. producida")
    ax[0].set_ylabel("Tipo de pan")

    sns.barplot(data= self.df, x="Eficiencia" , y="Tipo de pan", ax=ax[1])
    ax[1].set_title("Eficiencia por tipo de pan")
    ax[1].set_xlabel("Eficiencia")
    ax[1].set_ylabel("Tipo de pan")
    grafico.tight_layout()    ################!!!!!!!!!!!!!!!!!!!!!!!!!

    return pasar_a_pil(grafico)

class AnalizarConPastelote:
  #Varialbes de trabajo:
  def __init__(self, data_frame_general):
    self.df=data_frame_general

  def graficar_pastelisimo(self):

    grafico, ax = plt.subplots(1, 1, figsize=(1.88,1.08), dpi=100) #start

    resumen = self.df["Cumple meta"].value_counts
    colores = ["Red","green"]

    plt.pie(data=resumen, labels= resumen.index, colors=colores, ax=ax, shadow=True)
    ax.set_title("¿Cuántos cumplen?")
    grafico.tight_layout()    ################!!!!!!!!!!!!!!!!!!!!!!!!!

    return pasar_a_pil(grafico)