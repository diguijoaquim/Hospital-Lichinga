import flet as ft
from controls import *
from datetime import datetime
import re
import requests
from time import sleep
import math
from pdf_printer import *

selected_id = 0
funcionario=None

def home(page):
    return ft.Column()

def getChart():
    normal_radius = 100
    hover_radius = 110
    normal_title_style = ft.TextStyle(
        size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=16,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()
    chart = ft.PieChart(height=200,
        sections=[
            ft.PieChartSection(
                40,
                title="40%",
                title_style=normal_title_style,
                color=ft.colors.BLUE,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                30,
                title="30%",
                title_style=normal_title_style,
                color=ft.colors.YELLOW,
                radius=normal_radius,
                
            ),
            ft.PieChartSection(
                15,
                title="15%",
                title_style=normal_title_style,
                color=ft.colors.PURPLE,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                15,
                title="15%",
                title_style=normal_title_style,
                color=ft.colors.GREEN,
                radius=normal_radius,
            ),
        ],
        sections_space=0,
        center_space_radius=0,
        expand=True,
        on_chart_event=on_chart_event
    )
    return chart

def employer(page):
    return ft.Container()

nome_update = ft.TextField(label="Nome do Funcionario")
apelido_update = ft.TextField(label="Apelido do Funcionario")
bi_update = ft.TextField(label="Numero de BI")
especialidade_update=ft.TextField(label="Especialidade" )
faixa_etaria_update=ft.TextField(label="Faixa Etaria" )
categoria_update=ft.TextField(label="Categoria" )
nuit_update=ft.TextField(label="Nuit" )
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
        resposta = requests.post(url="https://hospital-fast-api.onrender.com/dina", json=pergunta)
        chatList.controls.append(ft.Text(f"Assistente: >>>{resposta.json()}", size=20, weight="bold", no_wrap=False,color=ft.colors.GREY_600)),
        page.update()

    def enviar(e):
        chatList.controls.clear()
        chatList.controls.append(ft.Text(f"Usuario: >>> {input.value}", color=ft.colors.GREEN_700, size=24, weight="bold")),
        input.value=''
        page.update()
        responder(input.value)

    chatList = ft.ListView(height=500, width=400)
    input = ft.TextField(label="fale com assistente do hospital", on_submit=enviar)
    chat_input = ft.Row(
        controls=[
            input, ft.CupertinoButton("Enviar", on_click=enviar, bgcolor=ft.colors.GREEN_700)
        ]
    )
    return ft.Row(
        controls=[
            ft.Card(content=ft.Container(padding=30,content=ft.Column(controls=[
                ft.Text("ASSISTENTE INTELIGENTE - POWERED BY LLAMA3",weight="bold"),
                ft.Column(controls=[
                    chatList, chat_input
                ])
            ])))
        ],alignment=ft.MainAxisAlignment.CENTER
    )

def tabela(data, page, update_app):
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
        nome_update.value=''
        apelido_update.value=''
        nuit_update.value=''
        bi_update.value=''
        provincia_update.value=''
        naturalidade_update.value=''
        carreira_update.value=''
        reparticao_update.value=''
        sexo_update.value=''
        especialidade_update.value=''
        nuit_update.value=''
        categoria_update.value=''
        faixa_etaria_update.value=''
        
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
            #print(res)
            show_success_dialog()
            progressBar_update.visible = False
            atualizar_dialogo.open = False
            update_app(page,True)
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
                    nome_update, apelido_update, bi_update, nuit_update,faixa_etaria_update,provincia_update, naturalidade_update,
                ]),
                ft.Column(controls=[
                    residencia_update, sexo_update,especialidade_update,categoria_update, carreira_update, sector_update, reparticao_update
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
        selected_id = e.control.data
        #print(selected_id)
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
    funcionario=None
    show_dlg=ft.AlertDialog(title=ft.Text(''),content=ft.Container(ft.ProgressRing()),actions=[
        ft.ElevatedButton("fechar",bgcolor=ft.colors.RED_700,color='white',on_click=fecha),
        ft.ElevatedButton("Imprimir",bgcolor=ft.colors.GREEN_700,color='white',on_click=lambda e:print_employer(funcionario))
    ])
    input_to=ft.TextField(label="Foi Trasferido para que hospital?")
    def show_input_t(e):
        status_dlg.content=ft.Column(height=200,controls=[
        ft.Text("Atualizar a Disponiblidade",weight="bold"),
        status,input_to,
        progressBar_status,
        ft.CupertinoButton(text="Atualizar o status",bgcolor=ft.colors.GREEN_700,on_click=addTransferencia)
        ])
        page.update()
    progressBar_status=ft.ProgressBar(color="amber", bgcolor="#eeeeee",visible=False)
    
    erro_status_dlg=ft.AlertDialog(title=ft.Text("Ocorreu um erro"), content=ft.Row(controls=[
        ft.Icon(ft.icons.INFO,color=ft.colors.RED_500),
        ft.Text("nao foi possivel atualizar o STATUS")
    ]))

    sucess_status_dlg=ft.AlertDialog(title=ft.Text("FEITO"), content=ft.Row(controls=[
        ft.Icon(ft.icons.INFO,color=ft.colors.GREEN_500),
        ft.Text("O STATUS foi atualizado\n com sucesso")
    ]))


    def addFerias(e):
        progressBar_status.visible=True
        page.update()
        dados={
            "funcionario_id": selected_id,
            "data_inicio_ferias": str(inicio_l.value),
            "data_fim_ferias": str(fim_l.value)
            }
        url="https://hospital-fast-api.onrender.com/add_ferias"
        res=requests.post(url=url,json=dados)
        if res.status_code==200:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=sucess_status_dlg
            sucess_status_dlg.open=True
            update_app(page)
            page.update()
        else:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=erro_status_dlg
            erro_status_dlg.open=True
            page.update()

    def addFalecido(e):
        progressBar_status.visible=True
        page.update()
        dados={
            "funcionario_id": selected_id,
            "data_falecimento": "2024-08-07T13:14:43.172Z",
            "idade": 0
            }
        url="https://hospital-fast-api.onrender.com/add_falecido"
        res=requests.post(url=url,json=dados)
        if res.status_code==200:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=sucess_status_dlg
            sucess_status_dlg.open=True
            update_app(page)
            page.update()
        else:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=erro_status_dlg
            erro_status_dlg.open=True
            page.update()

    def addAposentado(e):
        progressBar_status.visible=True
        page.update()
        dados={
            "funcionario_id": selected_id,
            "data_reforma": "2024-08-07T13:19:47.729Z",
            "idade_reforma": 0
            }
        url="https://hospital-fast-api.onrender.com/add_reforma"
        res=requests.post(url=url,json=dados)
        if res.status_code==200:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=sucess_status_dlg
            sucess_status_dlg.open=True
            update_app(page)
            page.update()
        else:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=erro_status_dlg
            erro_status_dlg.open=True
            page.update()
    def addTransferencia(e):
        progressBar_status.visible=True
        page.update()
        dados={
            "funcionario_id": selected_id,
            "data_transferido": "2024-08-07T13:06:28.092Z",
            "lugar_transferido": input_to.value
            }
        url="https://hospital-fast-api.onrender.com/add_transferencia"
        res=requests.post(url=url,json=dados)
        if res.status_code==200:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=sucess_status_dlg
            sucess_status_dlg.open=True
            update_app(page)
            page.update()
        else:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=erro_status_dlg
            erro_status_dlg.open=True
            page.update()
    def addSuspenco(e):
        progressBar_status.visible=True
        page.update()
        dados={
            "funcionario_id":selected_id,
            "data_suspenso": "2024-08-07T13:29:23.725Z",
            "motivo": motivo.value
            }
        url="https://hospital-fast-api.onrender.com/add_suspenso"
        res=requests.post(url=url,json=dados)
        if res.status_code==200:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=sucess_status_dlg
            sucess_status_dlg.open=True
            update_app(page)
            page.update()
        else:
            status_dlg.open=False
            progressBar_status.visible=False
            page.dialog=erro_status_dlg
            erro_status_dlg.open=True
            page.update()

    #licenca
    def done_i(e):
        inicio_l.open=False
        inicio_licenca_demo.content=ft.Text(inicio_l.value)
        page.update()
    def done_f(e):
        fim_l.open=False
        fim_licenca_demo.content=ft.Text(inicio_l.value)

        page.update()

    def open_start(e):
        inicio_l.open=True
        page.update()

    def open_end(e):
        fim_l.open=True
        page.update()

    
    inicio_l=ft.DatePicker(
                    first_date=datetime(year=2000, month=1, day=1),
                    last_date=datetime(year=datetime.now().year+1, month=datetime.now().month, day=datetime.now().day),
                    open=False,
                    on_change=done_i         

                )
    fim_l=ft.DatePicker(
                   first_date=datetime(year=2000, month=1, day=1),
                    last_date=datetime(year=datetime.now().year+3, month=datetime.now().month, day=datetime.now().day),
                    open=False,
                    on_change=done_f
                )
    inicio_licenca_demo=ft.Container(content=ft.Text("Inicio das ferias"))
    fim_licenca_demo=ft.Container(content=ft.Text("Fim das ferias"))
    start=ft.Row(controls=[
        ft.IconButton(icon=ft.icons.CALENDAR_MONTH,on_click=open_start),inicio_licenca_demo
    ])
    end=ft.Row(controls=[
        ft.IconButton(icon=ft.icons.CALENDAR_MONTH,on_click=open_end),fim_licenca_demo
    ])
    

    
    def show_input_l(e):
        status_dlg.content=ft.Column(height=260,controls=[
        ft.Text("Atualizar a Disponiblidade",weight="bold"),
        status,start,end,inicio_l,fim_l,
        progressBar_status,
        ft.CupertinoButton(text="Atualizar o status",bgcolor=ft.colors.GREEN_700,on_click=addFerias)
        ])
        page.update()
        

    motivo=ft.TextField(label="Motivos do Suspenso")

        #suspenso
    def show_input_s(e):
        status_dlg.content=ft.Column(height=200,controls=[
        ft.Text("Atualizar a Disponiblidade",weight="bold"),
        status,motivo,
        progressBar_status,
        ft.CupertinoButton(text="Atualizar o status",bgcolor=ft.colors.GREEN_700,on_click=addSuspenco)
        ])
        page.update()

        #falecido
    def show_input_d(e):
        status_dlg.content=ft.Column(height=180,controls=[
        ft.Text("Atualizar a Disponiblidade",weight="bold"),
        status,
        progressBar_status,
        ft.CupertinoButton(text="Atualizar o status",bgcolor=ft.colors.GREEN_700,on_click=addFalecido)
        ])
        page.update()  

        #reforma     
    def show_input_a(e):
        status_dlg.content=ft.Column(height=180,controls=[
        ft.Text("Atualizar a Disponiblidade",weight="bold"),
        status,
        progressBar_status,
        ft.CupertinoButton(text="Atualizar o status",bgcolor=ft.colors.GREEN_700,on_click=addAposentado)
        ])
        page.update()  
    
    status=ft.Dropdown(label="Status",options=[
        ft.dropdown.Option(text="Activo",on_click=show_input_d),
        ft.dropdown.Option(text="Transferido",on_click=show_input_t),
        ft.dropdown.Option(text="Falecido",on_click=show_input_d),
        ft.dropdown.Option(text="Aposentado",on_click=show_input_a),
        ft.dropdown.Option(text="Licença/Dispensado",on_click=show_input_l),
        ft.dropdown.Option(text="Suspenso",on_click=show_input_s)

    ])
    status_dlg=ft.AlertDialog(title=ft.Text(''),content=ft.Container(content=ft.Column(height=180,controls=[
        ft.Text("Atualizar a Disponiblidade",weight="bold"),
        status,progressBar_status,
        ft.CupertinoButton(text="Atualizar o status",bgcolor=ft.colors.GREEN_700)

    ])),actions=[
        
    ])
    def open_status(e):
        global selected_id
        selected_id = e.control.data
        page.dialog = status_dlg
        status_dlg.open = True
        funcionario=GetEmployerByID(selected_id).json()
        status_dlg.title=ft.Text(f"Estado do: {funcionario['nome']}")
        page.update()
        

    def salvar_para_pdf(e):
        global selected_id
        selected_id = e.control.data
        global funcionario
        funcionario=GetEmployerByID(selected_id).json()
        print_employer(funcionario)

    def open_show(e):
        global selected_id
        selected_id = e.control.data
        page.dialog = show_dlg
        show_dlg.open = True
        global funcionario
        funcionario=GetEmployerByID(selected_id).json()
        nascimento = re.split("-", funcionario['nascimento'])
        idade = datetime.now().year - int(nascimento[0])
        show_dlg.title=ft.Text(f"Dados do funcionario: {funcionario['nome']}")
        show_dlg.content=ft.Column(height=400,controls=[
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
        selected_id = e.control.data
        page.dialog = delete_dlg
        delete_dlg.open = True
        page.update()
        
    def deletar(e):
        progressBar_status.visible=True
        page.update()
        res = DeleteEmployerByID(selected_id)
        if res==200:
            page.dialog=sucess_status_dlg
            delete_dlg.open = False
            sucess_status_dlg.open=True
            progressBar_status.visible=False
            update_app(page)
            page.update()
        else:
            page.dialog=erro_status_dlg
            erro_status_dlg.open=True
            delete_dlg.open = False
            progressBar_status.visible=False
            update_app(page)
            page.update()
    
        

    def cancela(e):
        delete_dlg.open = False
        delete_dlg.actions.clear()
        page.update()

    delete_dlg = ft.AlertDialog(title=ft.Text("Aviso"), 
                          content=ft.Column(height=50,controls=[
                              ft.Text("Tens Certeza que queres Deletar \n o funcionario?"),
                              progressBar_status
                          ]), actions=[
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
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        border_radius=10,
        border=ft.border.all(1, ft.colors.GREY_300),
        
        
    )
    def return_active(e):
        res=licenca_to_active(e.control.data)
        if res == 200:
            update_app(page)

    for funcionario in data:
        nascimento = re.split("-", funcionario['nascimento'])
        idade = datetime.now().year - int(nascimento[0])
        if funcionario['status']=="ACTIVO":
            sinal=ft.Container(width=100,height=25,bgcolor=ft.colors.GREEN_600,border_radius=5,
                                       content=ft.Row(controls=[ft.Text(funcionario['status'],color="white",weight='bold')]
                                                      ,alignment=ft.MainAxisAlignment.CENTER))
            
        elif funcionario['status'] =="LICENCA":
            sinal=ft.Container(border=ft.border.all(1),width=100,height=25,bgcolor=ft.colors.GREEN_200,border_radius=5,
                                       content=ft.Row(controls=[ft.Text(funcionario['status'],color="white",weight='bold')]
                                                      ,alignment=ft.MainAxisAlignment.CENTER))
        elif funcionario['status'] =="Removido":
            sinal=ft.Container(width=100,height=25,bgcolor=ft.colors.RED_500,border_radius=5,
                                       content=ft.Row(controls=[ft.Text(funcionario['status'],color="white",weight='bold')]
                                                      ,alignment=ft.MainAxisAlignment.CENTER))
        elif funcionario['status'] =="TRANSFERIDO":
            sinal=ft.Container(width=100,height=25,bgcolor=ft.colors.PURPLE_500,border_radius=5,
                                       content=ft.Row(controls=[ft.Text(funcionario['status'],color="white",weight='bold')]
                                                      ,alignment=ft.MainAxisAlignment.CENTER))

        else:
            sinal=ft.Container(width=100,height=25,bgcolor=ft.colors.ORANGE_500,border_radius=5,
                                       content=ft.Row(controls=[ft.Text(funcionario['status'],color="white",weight='bold')]
                                                      ,alignment=ft.MainAxisAlignment.CENTER))
        
        if funcionario['status']=="Removido":
            butoes=[
                ft.PopupMenuItem(text="Restaura",on_click=return_active,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Ver Dados",on_click=open_show,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Salvar em PDF",on_click=salvar_para_pdf,data=f"{funcionario['id']}")
            ] 
        elif funcionario['status']=="FALECIDO":
            butoes=[
                ft.PopupMenuItem(text="Ver Dados",on_click=open_show,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Salvar em PDF",on_click=salvar_para_pdf,data=f"{funcionario['id']}"),
            ]
        elif funcionario['status']=="APOSENTADO":
            butoes=[
                ft.PopupMenuItem(text="Ver Dados",on_click=open_show,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Salvar em PDF",on_click=salvar_para_pdf,data=f"{funcionario['id']}"),
            ]
        elif funcionario['status']=="SUSPENSO":
            butoes=[
                ft.PopupMenuItem(text="Restaura",on_click=open_update,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Ver Dados",on_click=open_show,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Salvar em PDF",on_click=salvar_para_pdf,data=f"{funcionario['id']}"),
            ]
        elif funcionario['status']=="TRANSFERIDO":
            butoes=[
                ft.PopupMenuItem(text="Restaura",on_click=return_active,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Ver Dados",on_click=open_show,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Salvar em PDF",on_click=salvar_para_pdf,data=f"{funcionario['id']}"),
            ]

        else:
            butoes=[
                ft.PopupMenuItem(text="Atualizar",on_click=open_update,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Ver Dados",on_click=open_show,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Salvar em PDF",on_click=salvar_para_pdf,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Disponiblidade",on_click=open_status,data=f"{funcionario['id']}"),
                ft.PopupMenuItem(text="Deletar",on_click=open_delete,data=f"{funcionario['id']}")
            ] 

        t.rows.append(

            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"{funcionario['nome']} {funcionario['apelido']}")),
                    ft.DataCell(ft.Text(f"{funcionario['naturalidade']}/{funcionario['provincia']}")),
                    ft.DataCell(ft.Text(idade)),
                    ft.DataCell(ft.Text(funcionario['sector'])),
                    ft.DataCell(ft.Text(funcionario['reparticao'])),
                    ft.DataCell(ft.Text(formatar_data(funcionario['inicio_funcoes']))),
                    ft.DataCell(sinal),
                    ft.DataCell(ft.Row(controls=[
                        ft.PopupMenuButton(items=butoes)
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
                    ft.Text("Laboratório", size=20, weight="bold",color='white'),
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
