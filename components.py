import flet as ft
from controls import getFuncionarios, DeleteEmployerByID, UpdateEmployer, GetEmployerByID,getSectoresCount
from datetime import datetime
import re
import requests
from time import sleep
import math

selected_id = 0

def home(page):
    return ft.Column()



def employer(page):
    return ft.Container()

nome_update = ft.TextField(label="Nome do Funcionario")
apelido_update = ft.TextField(label="Apelido do Funcionario")
bi_update = ft.TextField(label="Numero de BI")
sexo_update = ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Feminino"),
        ]
    )

def assistente(page):
    def responder(p):
        pergunta = {
            "text": p
        }
        resposta = requests.post(url="http://192.168.1.62:8000/dina", json=pergunta)
        chatList.controls.append(ft.Text(f"Assistente: >>>{resposta.json()}", color="black", size=20, weight="bold", no_wrap=False)),
        page.update()

    def enviar(e):
        chatList.controls.clear()
        chatList.controls.append(ft.Text(f"Usuario: >>> {input.value}", color=ft.colors.GREEN_700, size=24, weight="bold")),
        page.update()
        responder(input.value)

    chatList = ft.ListView(height=500, width=800)
    input = ft.TextField(label="fale com assistente do hospital", on_submit=enviar)
    chat_input = ft.Row(
        controls=[
            input, ft.CupertinoButton("Enviar", on_click=enviar, bgcolor=ft.colors.GREEN_700)
        ]
    )
    return ft.Column(
        controls=[
            ft.Text("ASSISTENTE INTELIGENTE - POWERED BY LLAMA2"),
            ft.Column(controls=[
                chatList, chat_input
            ])
        ]
    )

def tabela(data, page, update_app):
    demo_erro = ft.Container()
    progressBar_update = ft.ProgressBar(width=600, color="amber", bgcolor=ft.colors.GREEN_700, visible=False)
    
    def ok(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title = ft.Text("Cadastro Concluído"),
        content = ft.Text("O funcionário foi Atualizado com sucesso!"),
        actions = [
            ft.TextButton("OK", on_click=ok)
        ],
    )

    def show_success_dialog():
        page.dialog = dlg
        dlg.open = True
        page.update()

    def atualizar(e):
        dados = {
            "nome": nome_update.value,
            "apelido": apelido_update.value,
            "bi": bi_update.value,
            "provincia": provincia_update.value,
            "naturalidade": naturalidade_update.value,
            "residencia": residencia_update.value,
            "sexo": sexo_update.value,
            "sector": sector_update.value,
            "reparticao": reparticao_update.value
        }
        demo_erro_update.content = ft.Text("")
        page.update()
        progressBar_update.visible = True
        page.update()
        sleep(3)
        res = UpdateEmployer(data=dados, id=selected_id)

        if res == 200:
            print(res)
            show_success_dialog()
            progressBar_update.visible = False
            atualizar_dialogo.open = False
            update_app(page)
            page.update()

        elif res == 422:
            demo_erro_update.content = ft.Text(f"Erro ao atualizar. codigo:{res}, \nVerifique se os dados que inseriu sao validos")
            progressBar_update.visible = False

        page.update()

    reparticao_update = ft.Dropdown(
        label="Repartição",
        options=[
            ft.dropdown.Option("Nenhuma reparticao"),
            ft.dropdown.Option("Assistência Jurídica"),
            ft.dropdown.Option("Assistência Social"),
            ft.dropdown.Option("Patrimônio"),
            ft.dropdown.Option("Transporte"),
            ft.dropdown.Option("Aprovisionamento"),
            ft.dropdown.Option("Serviços Gerais"),
            ft.dropdown.Option("Consultas Externas"),
            ft.dropdown.Option("Prestação de Contas"),
            ft.dropdown.Option("Legalidade e Classificação de Processos Contratuais"),
            ft.dropdown.Option("Vigilância Epidemiológica"),
            ft.dropdown.Option("Material Médico Cirúrgico"),
            ft.dropdown.Option("Planejamento e Estatísticas")
        ]
    )
    sector_update = ft.Dropdown(
        label="Setor",
        options=[
            ft.dropdown.Option("Laboratório"),
            ft.dropdown.Option("Maternidade"),
            ft.dropdown.Option("Cirurgia"),
            ft.dropdown.Option("Pediatria"),
            ft.dropdown.Option("Ortopedia"),
            ft.dropdown.Option("Reanimação"),
            ft.dropdown.Option("Psiquiatria"),
            ft.dropdown.Option("Medicina 1"),
            ft.dropdown.Option("Medicina 2"),
            ft.dropdown.Option("Oftalmologia"),
            ft.dropdown.Option("Berçário"),
            ft.dropdown.Option("Quimioterapia"),
            ft.dropdown.Option("Centro de Urgência"),
            ft.dropdown.Option("Bloco Operatório"),
            ft.dropdown.Option("Serviço Farmacêutico"),
            ft.dropdown.Option("Banco de Sangue"),
            ft.dropdown.Option("Radiologia")
        ]
    )
    demo_erro_update = ft.Container()
    
    provincia_update = ft.Dropdown(
        label="Província",
        options=[
            ft.dropdown.Option("Maputo"),
            ft.dropdown.Option("Gaza"),
            ft.dropdown.Option("Inhambane"),
            ft.dropdown.Option("Sofala"),
            ft.dropdown.Option("Manica"),
            ft.dropdown.Option("Tete"),
            ft.dropdown.Option("Zambézia"),
            ft.dropdown.Option("Nampula"),
            ft.dropdown.Option("Cabo Delgado"),
            ft.dropdown.Option("Niassa")
        ]
    )
    
    naturalidade_update = ft.TextField(label="Naturalidade")
    residencia_update = ft.TextField(label="Residencia")
    
    carreira_update = ft.TextField(label="Carreira")
    progressBar_update = ft.ProgressBar(width=600, color="amber", bgcolor=ft.colors.GREEN_700, visible=False)
    
    atualizar_dialogo = ft.AlertDialog(
        title = ft.Text("Atualizar dados do funcionario"),
        content = ft.Column(controls=[
            ft.Row(controls=[
                ft.Column(controls=[
                    nome_update, apelido_update, bi_update, provincia_update, naturalidade_update,
                ]),
                ft.Column(controls=[
                    residencia_update, sexo_update, carreira_update, sector_update, reparticao_update
                ]),
            ]), 
            progressBar_update, demo_erro_update
        ]),
        actions = [
            ft.CupertinoButton("Atualizar o Funcionario", bgcolor=ft.colors.GREEN_700, width=600, on_click=atualizar)
        ],
    )
    
    def open_update(e):
        global selected_id
        global sexo_update
        selected_id = e.control.key
        print(selected_id)
        atualizar_dialogo.open = True
        page.update()
        dados = GetEmployerByID(selected_id).json()
        page.dialog = atualizar_dialogo

        if dados:
            nome_update.value = dados["nome"]
            apelido_update.value = dados["apelido"]
            bi_update.value = dados["bi"]
            sexo_update.value=dados["sexo"]
            carreira_update.value = dados["careira"]
            sector_update.value = dados["sector"]
            residencia_update.value = dados["residencia"]
            naturalidade_update.value = dados["naturalidade"]
            provincia_update.value = dados["provincia"]
            reparticao_update.value = dados["reparticao"]


        page.update()

    def fecha(e):
        show_dlg.open=False
        page.update()
        
    show_dlg=ft.AlertDialog(title=ft.Text(''),content=ft.Container(),actions=[
        ft.ElevatedButton("fechar",bgcolor=ft.colors.RED_700,color='white',on_click=fecha),
        ft.ElevatedButton("Imprimir",bgcolor=ft.colors.GREEN_700,color='white')
    ])
    def open_show(e):
        global selected_id
        selected_id = e.control.key
        page.dialog = show_dlg
        show_dlg.open = True
        page.update()
        funcionario=GetEmployerByID(selected_id).json()
        nascimento = re.split("-", funcionario['nascimento'])
        idade = datetime.now().year - int(nascimento[0])
        show_dlg.title=ft.Text(f"Dados do funcionario: {funcionario['nome']}")
        show_dlg.content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("Nome: ",weight="bold"),
                ft.Text(f"{funcionario['nome']} {funcionario['apelido']}"),
            ]),
            ft.Row(controls=[
                ft.Text("Bi: ",weight="bold"),
                ft.Text(f"{funcionario['bi']}"),
            ]),
            ft.Row(controls=[
                ft.Text("Data de nacimento: ",weight="bold"),
                ft.Text(f"{funcionario['nascimento']}"),
            ]),
            ft.Row(controls=[
                ft.Text("Sexo: ",weight="bold"),
                ft.Text(funcionario['sexo']),
            ]),
            ft.Row(controls=[
                ft.Text("Naturadidade: ",weight="bold"),
                ft.Text(f"{funcionario['naturalidade']}/{funcionario['provincia']}"),
            ]),
            ft.Row(controls=[
                ft.Text("Enfirmaria: ",weight="bold"),
                ft.Text(funcionario['sector']),
            ]),
            ft.Row(controls=[
                ft.Text("Reparticao: ",weight="bold"),
                ft.Text(funcionario['reparticao']),
            ]),
            ft.Row(controls=[
                ft.Text("Comecou a trabalhar em: ",weight="bold"),
                ft.Text(funcionario['inicio_funcoes']),
            ]),
            ft.Row(controls=[
                ft.Text("Idade: ",weight="bold"),
                ft.Text(f"Tem {idade} anos de idade"),
            ]),
            ft.Row(controls=[
                ft.Text("Careirra: ",weight="bold"),
                ft.Text(funcionario['careira']),
            ]),


        ])
        page.update()
        

    def open_delete(e):
        global selected_id
        selected_id = e.control.key
        page.dialog = delete_dlg
        delete_dlg.open = True
        page.update()
        
    def deletar(e):
        print(selected_id)
        res = DeleteEmployerByID(selected_id)
        print(res)
        delete_dlg.open = False
        update_app(page)
    
        

    def cancela(e):
        delete_dlg.open = False
        delete_dlg.actions.clear()
        page.update()

    delete_dlg = ft.AlertDialog(title=ft.Text("Aviso"), 
                          content=ft.Text("Tens Certeza que queres Deletar \n o funcionario?"), actions=[
                              ft.ElevatedButton("Cancelar", on_click=cancela),
                              ft.ElevatedButton("Eliminar", bgcolor=ft.colors.RED_700, color="white", on_click=deletar)
                          ])
    
    t = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Naturalidade")),
            ft.DataColumn(ft.Text("Idade"), numeric=True),
            ft.DataColumn(ft.Text("Enfermaria")),
            ft.DataColumn(ft.Text("Repartição")),
            ft.DataColumn(ft.Text("Ano de Início")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        border_radius=10,
        border=ft.border.all(1, ft.colors.GREY_300),
        
        
    )
    
    for funcionario in data:
        nascimento = re.split("-", funcionario['nascimento'])
        idade = datetime.now().year - int(nascimento[0])
        t.rows.append(

            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"{funcionario['nome']} {funcionario['apelido']}")),
                    ft.DataCell(ft.Text(f"{funcionario['naturalidade']}/{funcionario['provincia']}")),
                    ft.DataCell(ft.Text(idade)),
                    ft.DataCell(ft.Text(funcionario['sector'])),
                    ft.DataCell(ft.Text(funcionario['reparticao'])),
                    ft.DataCell(ft.Text(funcionario['inicio_funcoes'])),
                    ft.DataCell(ft.Row(controls=[
                        ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.GREEN_700, on_click=open_update, key=f"{funcionario['id']}"),
                        ft.IconButton(ft.icons.VISIBILITY, icon_color=ft.colors.BLUE_700, on_click=open_show, key=f"{funcionario['id']}"),
                        ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=open_delete, key=f"{funcionario['id']}"),
                    ])),
                
                ],
            ),
        )
    
    return t
def medicina(valor):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Medicina 1", size=20, weight="bold",color='white'),
                    ft.Text(valor,size=40,color='white'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            bgcolor=ft.colors.BLUE_200,
            border_radius=10,
        ),
        
        height=150,
    )

def laboratorio(valor):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Laboratorio", size=20, weight="bold",color='white'),
                    ft.Text(valor,size=40,color='white'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            bgcolor=ft.colors.GREEN_200,
            border_radius=10,
        ),
        col={"sm": 6, "md": 4, "xl": 2},
        
        height=150,
    )

def maternidade(valor):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Maternidade", size=20, weight="bold",color='white'),
                    ft.Text(valor,size=40,color='white'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            bgcolor=ft.colors.PURPLE_200,
            border_radius=10,
        ),
        
        height=150,
        col={"sm": 6, "md": 4, "xl": 2},
    )

def psiquiatria(valor):
    return  ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Psiquiatria", size=20, weight="bold",color='white'),
                    ft.Text(valor,size=40,color='white'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                    "0xffca485c",
                    "0xffe16b5c",
                    "0xfff39060",
                    "0xffffb56b",
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
            ),
            border_radius=10,
        ),
        col={"sm": 6, "md": 4, "xl": 2},
        
        height=150,
    )
