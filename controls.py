import requests
from save_token import *
import json
from datetime import datetime
import locale
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
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def getReformados():
    url = 'http://192.168.1.62:8000/emp/reformados/'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []
        

def getDeletedEmployers():
    url = 'http://192.168.1.62:8000/removido/'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def getDeathEmployers():
    url = 'http://192.168.1.62:8000/emp/falecidos/'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def getReformado():
    url = 'http://192.168.1.62:8000/emp/reformados'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def getTrasferidoEmployers():
    url = 'http://192.168.1.62:8000/emp/transferidos/'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def getSuspensedEmployers():
    url = 'http://192.168.1.62:8000/emp/suspensos'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def getEmployerLicenca():
    url = 'http://192.168.1.62:8000/emp/licencas'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        if data:   
            return data
    except requests.ConnectionError:
        print("Erro de conexão. Verifique a sua rede.")
    except requests.Timeout:
        print("A solicitação expirou. Tente novamente mais tarde.")
    except requests.RequestException as e:   
        print(f"Ocorreu um erro: {e}")
    return []

def GetEmployerByID(id):
    url = f'http://192.168.1.62:8000/employer/{id}'
    return requests.get(url, headers=headers)
    
def getFuncionariosByQuery(query):
    url = f'http://192.168.1.62:8000/getbysearch/?name={query}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:   
            return data
    return []

def addEmployer(data):
    url = 'http://192.168.1.62:8000/employers/'
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

def UpdateEmployer(data,id):
    url = f'http://192.168.1.62:8000/employer/{id}'
    response = requests.put(url, headers=headers,json=data)
    if response.status_code == 200:
        data = response.json()
        if data:   
            return response.status_code
    return response.status_code

def getEmployerByGenre(genre):
    url = f'http://192.168.1.62:8000/employers/genre/{genre}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:   
            return data
    return []

def getEmployerByProvince(p):
    url = f'http://192.168.1.62:8000/employers/province/{p}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:   
            return data
    return []

def getEmployerByReparticao(r):
    url = f'http://192.168.1.62:8000/employers/reparticao/{r}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:   
                return data
    except:
        return []
def getEmployerBySector(s):
    url = f'http://192.168.1.62:8000/employers/sector/{s}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:   
                return data
    except:
        return []
def DeleteEmployerByID(id):
    url = f'http://192.168.1.62:8000/employers/{id}'
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        data = response.status_code
        if data:   
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
                if data:   
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
            


def getFerias():
    url='http://192.168.1.62:8000/ferias'
    res=requests.get(url)
    if res.status_code==200:
        return res.json()
    else:
        []



# Função para calcular quantos dias faltam até o fim das férias
def getRestante(data_inicio, data_fim):
    # Converter strings para objetos datetime
    inicio = datetime.fromisoformat(data_inicio)
    fim = datetime.fromisoformat(data_fim)
    # Pegar a data atual
    agora = datetime.now()
    
    # Se as férias ainda não começaram, retornar a diferença entre o início e agora
    if agora < inicio:
        return (inicio - agora).days
    # Se as férias começaram mas não terminaram, retornar a diferença entre o fim e agora
    elif inicio <= agora <= fim:
        return (fim - agora).days + 1  # +1 para incluir o dia final
    # Se as férias já terminaram, retornar 0
    else:
        return 0

# Função para calcular a duração total das férias
def getDays(data_inicio, data_fim):
    # Converter strings para objetos datetime
    inicio = datetime.fromisoformat(data_inicio)
    fim = datetime.fromisoformat(data_fim)
    # Calcular a diferença em dias
    diferenca = fim - inicio
    return diferenca.days





def formatar_data(data_str):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    try:
        # Tenta primeiro com o formato ISO completo com milissegundos
        data = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        try:
            # Tenta com o formato ISO sem milissegundos
            data = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            try:
                # Tenta com o formato sem o tempo
                data = datetime.strptime(data_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Formato de data inválido: {data_str}")
    
    # Retorna a data no formato desejado
    return data.strftime("%d de %B de %Y")


def getCustomFerias():
    ferias = getEmployerLicenca()
    customFerias = []

    for feria in ferias:
        for item in feria['ferias']:  # Itera sobre a lista 'ferias'
            customFerias.append({
                "funcionario": feria['nome'],
                'dias_restantes': getRestante(data_inicio=item['data_inicio_ferias'], data_fim=item['data_fim_ferias']),
                'dias': getDays(data_inicio=item['data_inicio_ferias'], data_fim=item['data_fim_ferias']),
                'inicio': item['data_inicio_ferias'],
                'fim': item['data_fim_ferias']
            })

    return customFerias
            
    
def licenca_to_active(id):
    dados = {
        "status": 'ACTIVO',
    }
    res = UpdateEmployer(data=dados, id=id)
    return res