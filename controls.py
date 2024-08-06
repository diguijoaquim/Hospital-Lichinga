import requests
from save_token import *
import json
#aqui sao controlers do app main.py
token=get_token()




def login(n, s):
    global token, headers
    data = {
        'username': n,
        'password': s
    }
    res = requests.post("http://192.168.1.62:8000/token", data=data)
    if res.status_code == 200:
        token = res.json()['access_token']
        save_token(token)
        # Atualizar os cabeçalhos após login
        headers['Authorization'] = f"Bearer {token}"
    return res.json()

def getUser():
    url = 'http://192.168.1.62:8000/users/me'
    res=requests.get(url=url,headers=headers)
    return res.json()
# Controlador para as requisições
headers = {
    'accept': 'application/json',
    'Authorization': f"Bearer {token}"
}


def getFuncionarios():
    url = 'http://192.168.1.62:8000/employers/'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta uma exceção para status codes 4xx/5xx
        data = response.json()
        if data:  # Verifica se a resposta não está vazia
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:  # Captura outras exceções relacionadas a requests
        print(f"Ocorreu um erro: {e}")
    
    return []
def GetEmployerByID(id):
    url = f'http://192.168.1.62:8000/employer/{id}'
    return requests.get(url, headers=headers)
    
def getFuncionariosByQuery(query):
    url = f'http://192.168.1.62:8000/employers/?search={query}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:  # Verifica se a resposta não está vazia
            return data
    return []

def addEmployer(data):
    url = 'http://192.168.1.62:8000/employers/'
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

def UpdateEmployer(data,id):
    url = f'http://192.168.1.62:8000/employers/{id}'
    response = requests.put(url, headers=headers,json=data)
    if response.status_code == 200:
        data = response.json()
        if data:  # Verifica se a resposta não está vazia
            return response.status_code
    return response.status_code

def getEmployerByGenre(genre):
    url = f'http://192.168.1.62:8000/employers/genre/{genre}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:  # Verifica se a resposta não está vazia
            return data
    return []

def getEmployerByProvince(p):
    url = f'http://192.168.1.62:8000/employers/province/{p}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:  # Verifica se a resposta não está vazia
            return data
    return []

def getEmployerByReparticao(r):
    url = f'http://192.168.1.62:8000/employers/reparticao/{r}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:  # Verifica se a resposta não está vazia
                return data
    except:
        return []
def getEmployerBySector(s):
    url = f'http://192.168.1.62:8000/employers/sector/{s}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:  # Verifica se a resposta não está vazia
                return data
    except:
        return []
def DeleteEmployerByID(id):
    url = f'http://192.168.1.62:8000/employers/{id}'
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:  # Verifica se a resposta não está vazia
            return data
    return []
def check_token(t):
    for i in range(5):
        if i !=None:
            header = {
            'accept': 'application/json',
            'Authorization': f"Bearer {t}"
        }
            global headers
            headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {t}"
        }

            url = 'http://192.168.1.62:8000/employers/'
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                data = response.json()
                if data:  # Verifica se a resposta não está vazia
                    return data
                
def getSectores():
    try:
        res=requests.get("http://192.168.1.62:8000/employers/sectors")
        return res.json()
    except:
        return "network_error"



def NovoUsuario(data):
    url = 'http://192.168.1.62:8000/users/' 
    res=requests.post(url,json=data)   

    return res.status_code 
            