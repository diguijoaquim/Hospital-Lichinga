import flet as ft
from controls import*
from datetime import datetime
import time
from components import*
import sys
import os
from pdf_printer import create_pdf

token=''


        
def salvar_pdf(e):
    dados=getFuncionarios()
    create_pdf(dados)
    
def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main(page: ft.Page):
    page.title = "Hospital de Lichinga"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    demo_erro=ft.Container()
    page.padding = 0
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.ProgressRing(height=100,width=100,bgcolor=ft.colors.RED_200),
                    ft.Text("Aguarde um segundo..."),
                    ft.ResponsiveRow()
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    ft.colors.WHITE10,
                    ft.colors.AMBER_100,
                    ft.colors.RED_100,
                    ft.colors.BLUE_100,
                    ft.colors.WHITE,
                ],
                tile_mode=ft.GradientTileMode.CLAMP,
                rotation=math.pi / 3,
            ),
            expand=True
        )
    )
    page.update()
    # Criação dos campos de entrada e botões
    username_input = ft.TextField(label="Usuário ou telefone", autofocus=True)
    password_input = ft.TextField(label="Senha", password=True)
    result_text = ft.Text("")

    psiquiatria_card=psiquiatria(getSectoresCount()['psiquiatria'])
    medicina1_card=medicina(getSectoresCount()['medicina'])
    laboratorio_card=laboratorio(getSectoresCount()['laboratorio'])
    maternidade_card=maternidade(getSectoresCount()['maternidade'])


    def atualizar_app(page):
        print(check_isLoged())
        login_dialog.open=False
        global psiquiatria_card,medicina1_card,laboratorio_card,maternidade_card
        username_input.value=''
        password_input.value=''
        nome.value = ''
        nome_update.value = ''
        apelido.value = ''
        apelido_update.value = ''
        sector.value = ''
        sexo_update.value = ''
        sexo.value = ''
        reparticao.value = ''
        provincia.value = ''
        naturalidade.value = ''
        bi.value = ''
        nascimento.value = ''
        inicio_funcoes.value = ''
        nascimento_demo.content=ft.Text('')
        funcoes_demo.content=ft.Text('')
        
        if check_isLoged()==True:
            psiquiatria_card=psiquiatria(getSectoresCount()['psiquiatria'])
            medicina1_card=medicina(getSectoresCount()['medicina'])
            laboratorio_card=laboratorio(getSectoresCount()['laboratorio'])
            maternidade_card=maternidade(getSectoresCount()['maternidade'])
            funcionarios=getFuncionarios()
            body.content=page_home
            update_employer(funcionarios)
            update_home(funcionarios)
        else:
            psiquiatria_card=psiquiatria(0)
            medicina1_card=medicina(0)
            laboratorio_card=laboratorio(0)
            maternidade_card=maternidade(0)
            page.dialog=login_dialog
            login_dialog.open=True
            body.content=ft.Container(content=ft.Text("Voce nao esta Autenticado no Sistema!",weight='bold',size=18))
            page_employers.content=ft.Container()
            page_home.content=ft.Container()
            page.update()
        

    def _check(e):
        atualizar_app(page)
    

    def _login(e):
        login(username_input.value,password_input.value)
        atualizar_app(getFuncionarios())

    login_dialog = ft.AlertDialog(
        title=ft.Text("Entrar no sistema"),
        content=ft.Column(controls=[
            username_input,
            password_input,
            result_text
        ]),
        actions=[
            
            ft.ElevatedButton(text="Entar no Sistema",bgcolor=ft.colors.GREEN_700,width=340,color="white",on_click=_login),
        ],on_dismiss=_check,
    )
    def find_filtered(e):
        if filtrar.value =="Provincia":
            update_employer(getEmployerByProvince(provincia_s.value))
            page.update()
        if filtrar.value =="Naturalidade":
            pass
        if filtrar.value =="Sector":
            update_employer(getEmployerBySector(sector_s.value))
            page.update()
        if filtrar.value =="Genero":
            update_employer(getEmployerByGenre(sexo_filter.value))
            page.update()
        if filtrar.value =="Reparticao":
            update_employer(getEmployerByReparticao(reparticao_s.value))
            page.update()
    provincia_s = ft.Dropdown(
            label="Província",
            width=200,
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
    def update_employer(data):
        page_employers.content=ft.Column(controls=[
        ft.Row(controls=[
            filtrar,provincia_s,sector_s,reparticao_s,sexo_filter,ft.FloatingActionButton(icon=ft.icons.FIND_IN_PAGE,on_click=find_filtered),
            search_input,ft.Container(content=ft.Row(controls=[
                ft.IconButton(icon=ft.icons.PRINT),
                ft.IconButton(icon=ft.icons.DOWNLOAD,on_click=salvar_pdf),
                ft.IconButton(icon=ft.icons.REFRESH)
            ])),
        ]),
        ft.Container(expand=True,
                     content=ft.ResponsiveRow(controls=[
                        ft.Column(controls=[
                           ft.ResponsiveRow(controls=[
                                tabela(data,page,atualizar_app),
                           ])
                        ],scroll=ft.ScrollMode.AUTO,height=600)
                    ],)
        
        ),nascimento,funcoes])
        
    def update_home(data=getFuncionarios()):
        psiquiatria_card=psiquiatria(getSectoresCount()['psiquiatria'])
        medicina1_card=medicina(getSectoresCount()['medicina'])
        laboratorio_card=laboratorio(getSectoresCount()['laboratorio'])
        maternidade_card=maternidade(getSectoresCount()['maternidade'])
        
        page_home.controls.clear()
        page_home.controls.append(ft.Column(controls=[
            ft.ResponsiveRow([
            ft.Container(col=3,content=laboratorio_card),
            ft.Container(col=3,content=maternidade_card),
            ft.Container(col=3,content=medicina1_card),
            ft.Container(col=3,content=psiquiatria_card)
        ]),
        ft.Container(expand=True,
                     content=ft.ResponsiveRow(controls=[
                        ft.Column(controls=[
                           ft.ResponsiveRow(controls=[
                                tabela(data,page,atualizar_app),
                           ])
                        ],scroll=ft.ScrollMode.AUTO,height=600)
                    ],)),nascimento,funcoes   
                    ]))
        page.update()
        
            
            

    def open_nascimento(e):
        nascimento.open=True
        page.update()

    def open_funcoes(e):
        funcoes.open=True
        page.update()
    
    def done_f(e):
        value=re.split(" ",str(funcoes.value))
        print(value[0])
        funcoes_demo.content=ft.Text(value[0])
        page.update()

    def done(e):
        value=re.split(" ",str(nascimento.value))
        print(value[0])
        nascimento_demo.content=ft.Text(value[0])
        page.update()
    nascimento_demo=ft.Container()
    nascimento=ft.DatePicker(
                    first_date=datetime(year=1950, month=1, day=1),
                    last_date=datetime(year=2010, month=1, day=1),
                    open=False,
                    on_change=done

                )
    funcoes_demo=ft.Container()
    funcoes=ft.DatePicker(
                    first_date=datetime(year=1990, month=10, day=1),
                    last_date=datetime(year=2024, month=10, day=1),
                    open=False,
                    on_change=done_f

                )


    provincia = ft.Dropdown(
        label="Província",
        width=200,
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
    sexo_filter=ft.Dropdown(
        label="Sexo",
        width=130,
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino"),
        ]
    )
    sector_s = ft.Dropdown(
    label="Setor",
    width=220,
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

    reparticao_s = ft.Dropdown(
    label="Repartição",
    width=220,
    options=[
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
    sector = ft.Dropdown(
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

    reparticao = ft.Dropdown(
    label="Repartição",
    options=[
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

    def find_searching(e):
        update_employer(getFuncionariosByQuery(e.control.value))
        page.update()

    #telas
    page_home=home(page)
    page_employers=employer(page)
    page_assistente=assistente(page)

    search_input=ft.TextField(label="Pesquisar",on_submit=find_searching,width=170)
    filtrar=ft.Dropdown(
        label="filtrar por",
        width=150,
        options=[
            
            ft.dropdown.Option("Provincia"),
            ft.dropdown.Option("Sector"),
            ft.dropdown.Option("Genero"),
            ft.dropdown.Option("Naturalidade"),
            ft.dropdown.Option("Reparticao"),

        ]
    )

    
    if check_isLoged():
        update_home(getFuncionarios())
   

    def ok(e):
        dlg.open=False
        page.update()
        page.update()

    def change_page(e):
        index=e.control.selected_index
        if index==0:
            body.content=page_home
            page.update()
        elif index==1:
            if getFuncionarios():
                body.content=page_employers
                page.update()
            else:
                body.content=page_employers
                page.update()
                
           
        elif index==2:
            body.content=page_assistente
            page.update()
        elif index==3:
            atualizar_app(page)
            pass
        elif index==4:
            atualizar_app(page)
            pass
        elif index==6:
            remove_token()
            atualizar_app(page)
        else:
            page.window_close()

    dlg = ft.AlertDialog(
            title=ft.Text("Cadastro Concluído"),
            content=ft.Text("O funcionário foi cadastrado com sucesso!"),
            actions=[
                ft.TextButton("OK", on_click=ok)
            ],
        )
    def show_success_dialog():
        page.dialog = dlg
        dlg.open = True
        page.update()
    def add(e):
        
        dados={
            "nome": nome.value,
            "apelido": apelido.value,
            "nascimento": str(nascimento.value),
            "bi": bi.value,
            "provincia": provincia.value,
            "naturalidade": naturalidade.value,
            "residencia": residencia.value,
            "sexo": sexo.value,
            "inicio_funcoes": str(funcoes.value),
            "sector": sector.value,
            "reparticao":reparticao.value
        }
        demo_erro.content=ft.Text("")
        page.update()
        progressBar.visible=True
        page.update()
        time.sleep(3)
        res=addEmployer(data=dados)

        if res ==200:
            show_success_dialog()
            progressBar.visible=False
            cadastro_dialogo.open=False
            atualizar_app(page=page)
            page.update()

        elif res ==422:
            demo_erro.content=ft.Text(f"Erro ao cadastrar. codigo:{res}, \nVerifique se os dados que inseriu sao validos")
            progressBar.visible=False
        

        page.update()

    #variaves do cadastro
    nome=ft.TextField(label="Nome do Funcionario" )
    apelido=ft.TextField(label="Apelido do Funcionario" )
    nascimento_btn=ft.ElevatedButton(icon=ft.icons.CALENDAR_MONTH,text="nascimento",on_click=open_nascimento)
    funcoes_btn=ft.ElevatedButton(icon=ft.icons.CALENDAR_MONTH,text="Inicio das funcoes",on_click=open_funcoes)
    
   
    
    bi=ft.TextField(label="Numero de BI" )
    provincia = ft.Dropdown(
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
    provincia_s = ft.Dropdown(
            label="Província",
            width=200,
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

    naturalidade=ft.TextField(label="Natualidade")
    residencia=ft.TextField(label="Residencia"  )
    sexo=ft.Dropdown(
        label="Sexo",
        options=[
            ft.dropdown.Option("Masculino"),
            ft.dropdown.Option("Femenino"),
        ]
    )
    inicio_funcoes=ft.TextField(label="Inicio das funcoes")
    careira=ft.TextField(label="Careira"  )
    
    
    progressBar= ft.ProgressBar(width=600, color="amber", bgcolor=ft.colors.GREEN_700,visible=False)

    cadastro_dialogo=ft.AlertDialog(
        title=ft.Text("Novo Funcionario"),
        content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Column(controls=[
                nome,apelido,ft.Row(controls=[nascimento_btn,nascimento_demo]),bi,provincia,naturalidade,
            ]),
            ft.Column(controls=[
                residencia,sexo,ft.Row(controls=[funcoes_btn,funcoes_demo]),careira,sector,reparticao
            ]),
            ]), progressBar,demo_erro
           ,
           
        ]),
        actions=[
            ft.CupertinoButton("Cadsatrar o Funcionario",bgcolor=ft.colors.GREEN_700,width=600,on_click=add)
        ],
    
    )

    def open_cadastro_dialogo(e):
        page.dialog=cadastro_dialogo
        cadastro_dialogo.open=True
        page.update()


    # Ações do AppBar
    search_action = ft.IconButton(icon=ft.icons.SEARCH, on_click=search_function)
    settings_action = ft.IconButton(icon=ft.icons.SETTINGS, on_click=settings_function)
    notifications_action = ft.IconButton(icon=ft.icons.NOTIFICATIONS, on_click=notifications_function)
    profile_action = ft.IconButton(icon=ft.icons.PERSON, on_click=profile_function)
    help_action = ft.IconButton(icon=ft.icons.HELP, on_click=help_function)

    page.appbar = ft.AppBar(
        bgcolor=ft.colors.GREEN_700,
        color=ft.colors.WHITE,
        leading=ft.Icon(ft.icons.LOCAL_HOSPITAL),
        title=ft.Text("Hospital de Lichinga"),
        actions=[search_action, settings_action, notifications_action, profile_action, help_action]
    )
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME, selected_icon=ft.icons.HOME, label="Casa"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PEOPLE),
                selected_icon_content=ft.Icon(ft.icons.PEOPLE),
                label="Funcionarios",
            ),
            
            ft.NavigationRailDestination(
                icon=ft.icons.CHAT,
                selected_icon_content=ft.Icon(ft.icons.HELP),
                label_content=ft.Text("Asistente IA"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Definicoes"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INFO,
                selected_icon_content=ft.Icon(ft.icons.INFO),
                label_content=ft.Text("Sobre o sistema"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.HELP,
                selected_icon_content=ft.Icon(ft.icons.HELP),
                label_content=ft.Text("Ajuda"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.EXIT_TO_APP, selected_icon=ft.icons.EXIT_TO_APP, label="Sair"
            ),
        ],
        on_change=change_page,
    )
    body=ft.Container(content=page_home,expand=True)
    page.controls.clear()

    page.update()
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                body
            ],
            expand=True,
        )
    )
    page.padding = 10
    page.floating_action_button=ft.FloatingActionButton(icon=ft.icons.ADD,on_click=open_cadastro_dialogo)
    page.update()
    
    atualizar_app(page)

# Funções de exemplo para cada ação
def search_function(e):
    print("Ação de pesquisa")

def settings_function(e):
    print("Ação de configurações")

def notifications_function(e):
    print("Ação de notificações")

def profile_function(e):
    print("Ação de perfil de usuário")

def help_function(e):
    print("Ação de ajuda")


# Executa o aplicativo
ft.app(target=main)
