from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pyautogui import *
from time import sleep
from tkinter import messagebox
import pandas as pd


def inicio_automacao():
  sleep(1)
  #  Clica dentro da caixa
  click(x,(y + 100))

  #  Seleciona o primeio campo, Marca do Veículo
  press('tab')
  
  #  Seleciona a Marca
  press('down')
  press('enter')

  #  Seleciona o Ano
  press('tab')
  press('tab')
  press('down')
  press('enter')

  sleep(1)


def pega_montadoras(navegador):
  #  Pega uma lista com todas as montadoras
  montadoras = navegador.find_element(By.ID, 'selectMarcamoto').find_elements(By.TAG_NAME, 'option')

  #  Limpa a lista de elementos em branco
  montadoras = montadoras[1:]

  return montadoras


def pega_anos(navegador):
  #  Pega uma lista com todos os anos da montadora selecionada
  ano = navegador.find_element(By.ID, 'selectAnomoto').find_elements(By.TAG_NAME, 'option')

  #  Limpa a lista de elementos em branco
  ano = ano[1:]

  return ano


def pega_modelos(navegador):
  #  Pega todos os modelos do ano selecionado
    modelos = navegador.find_element(By.ID, 'selectAnoModelomoto').find_elements(By.TAG_NAME, 'option')

    #  Limpa a lista de elementos em branco
    modelos = modelos[1:]

    return modelos

def seleciona_ano_seguinte():
    keyDown('shift')
    press('tab')
    keyUp('shift')
    press('tab')
    press('down')
    press('enter')
    sleep(1)


caminho = r'C:\Users\wellington\Desktop\Suporte Atendimento\projetos\APIFipe\APIFipe\chromedriver-win64\chromedriver.exe'

servico = Service(caminho)

navegador = webdriver.Chrome(service=servico)

navegador.set_window_size(930,1014)

navegador.get('https://veiculos.fipe.org.br/#carro-comum')

messagebox.showinfo(title='Início', message='Ao iniciar o sistema, não poderá utilizar a máquina até terminar.')

localizacao = locateOnScreen('fipe/imagens/moto.png')

x,y = center(localizacao)

click(x,y)

montadoras_lista = []
anos_lista = []
modelos_lista = []

inicio_automacao()

montadoras = pega_montadoras(navegador)

ciclo = 0
while ciclo < len(montadoras):
  ano = pega_anos(navegador)

  for ciclo_ano in range(len(ano)):
    modelos = pega_modelos(navegador)
    
    for carro in range(len(modelos)):
      montadoras_lista.append(montadoras[ciclo].text)  #  Adiciona a montadora na lista de montadoras
      anos_lista.append(ano[ciclo_ano].text)  #  Adiciona o ano na lista de anos
      modelos_lista.append(modelos[carro].text)  #  Adiciona o modelo na lista de modelos
    
    seleciona_ano_seguinte()
  
  if ciclo%2 == 0:
     messagebox.showinfo(title='Pausa', message='Pausa para descansar. Clique em "ok" para continuar.')
     
  inicio_automacao()
  
  ciclo += 1

montadoras_ano_carros = {
        'Montadrora': montadoras_lista,
        'Ano': anos_lista,
        'Modelo': modelos_lista
        }

veiculos = pd.DataFrame(montadoras_ano_carros)

veiculos.to_excel('FIPE-Moto.xlsx')