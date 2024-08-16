import flet as ft
from controls import*
from datetime import datetime
import time
from components import*
import sys
import os
from pdf_printer import create_pdf
import asyncio




employers=[]
deletedEmployers=[]
deathEmployers=[]
licenseEmployers=[]
suspensoEmployers=[]
trasferidos=[]
curent_page="home"
card_changed=False

progess_page= ft.AlertDialog(open=True,content=ft.Row(height=30,width=100,controls=[ft.ProgressRing(),ft.Text("Caregando...",weight="bold")]))
        
def salvar_pdf(e):
    dados=getFuncionarios()
    create_pdf(dados)
    
def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def main(page: ft.Page):
    page.title = "Hospital de Lichinga"
    page.theme_mode = 'light'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    token=''
    global employers,setores,suspensoEmployers,licenseEmployers,curent_page

    token=page.client_storage.get('token')
    set_headers(token)
    def check_isLoged():
        t= page.client_storage.get('token')
        print(t)
        if t != None:
            return True
        else:
            False
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
    employers=getFuncionarios()
    setores=getSectores()
    # Criação dos campos de entrada e botões
    username_input = ft.TextField(label="Usuário ou telefone", autofocus=True)
    password_input = ft.TextField(label="Senha", password=True)
    result_text = ft.Text("")

    async def update_card():
        global psiquiatria_card,medicina1_card,laboratorio_card,maternidade_card,setores
        setores=await asyncio.to_thread(getSectores)

    def atualizar_app(page,card_changed=False):
        login_dialog.open=False
        global psiquiatria_card,medicina1_card,laboratorio_card,maternidade_card,setores
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
            if card_changed:
                asyncio.run(update_card())
            else:
                psiquiatria_card=psiquiatria(setores['Psiquiatria'])
                medicina1_card=medicina(setores['Medicina 1'])
                laboratorio_card=laboratorio(setores['Laboratório'])
                maternidade_card=maternidade(setores['Maternidade'])
            funcionarios=getFuncionarios()
            update_home(funcionarios)
            update_employer(funcionarios)
            
            if curent_page=="home":
                body.content=page_home
            elif curent_page=='employers':
                body.content=page_employers
            else:
                pass
            
            
           
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
        progressbar.visible=True
        page.update()
        res=login(username_input.value,password_input.value)
        if res.status_code == 200:
            token = res.json()['access_token']
            headers['Authorization'] = f"Bearer {token}"
            page.client_storage.set("token",token)
        progressbar.visible=False
        atualizar_app(getFuncionarios())
    progressbar=ft.ProgressBar(color="amber", bgcolor="#eeeeee",visible=False)
    login_dialog = ft.AlertDialog(
        title=ft.Text("Entrar no sistema"),
        content=ft.Column(height=200,controls=[
            username_input,
            password_input,
            result_text,
            progressbar,
            ft.CupertinoButton(text="Entar no Sistema",bgcolor=ft.colors.GREEN_700,width=300,color="white",on_click=_login)
        ]),
        on_dismiss=_check,
    )
    def find_filtered(e):
        if filtrar.value =="Provincia":
            update_employer(getEmployerByProvince(provincia_s.value))
            page.update()
        elif filtrar.value =="Naturalidade":
            pass
        elif filtrar.value =="Sector":
            update_employer(getEmployerBySector(sector_s.value))
            page.update()
        elif filtrar.value =="Genero":
            update_employer(getEmployerByGenre(sexo_filter.value))
            page.update()
        elif filtrar.value =="Reparticao":
            update_employer(getEmployerByReparticao(reparticao_s.value))
            page.update()
        elif filtrar.value =="Estado":
            if estado.value=="DELETADO":
                update_employer(getDeletedEmployers())
            elif estado.value=="ACTIVO":
                update_employer(getFuncionarios())
            elif estado.value=="APOSENTADO":
                update_employer(getReformados())
            elif estado.value=="FALECIDO":
                update_employer(getDeathEmployers())
            elif estado.value=="SUSPENSO":
                update_employer(getSuspensedEmployers())
            elif estado.value=="TRANSFERIDO":
                update_employer(getTrasferidoEmployers())
            elif estado.value=="LICENCA/FERIAS":
                update_employer(getEmployerLicenca())

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
            filtrar,provincia_s,sector_s,reparticao_s,estado,sexo_filter,ft.FloatingActionButton(icon=ft.icons.FIND_IN_PAGE,on_click=find_filtered),
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


    #criar uma funcao assicrona que veriica mudanca no banco de daos para atualizar a tela de uma forma dinamina sem travar a tela
    
    async def atualizar_home():
        global employers,setores,deletedEmployers,deathEmployers,suspensoEmployers,licenseEmployers,trasferidos
    
        if employers:
            #default
            body.content=page_home
            page.update()

            novosdados = await asyncio.to_thread(getFuncionarios)
            setores=await asyncio.to_thread(getSectores)
            deletedEmployers= await asyncio.to_thread(getDeletedEmployers)
            suspensoEmployers=await asyncio.to_thread(getSuspensedEmployers)
            licenseEmployers=await asyncio.to_thread(getEmployerLicenca)
            deathEmployers=await asyncio.to_thread(getDeathEmployers)
            trasferidos=await asyncio.to_thread(getTrasferidoEmployers)

            if novosdados != employers:
                update_home(novosdados)
                body.content=page_home
                page.update()
                page.update()
                employers = novosdados  # Atualiza a variável global com os novos dados
            else:
                pass
                
        else:
            body.content = page_employers
            page.update()
    


        
    def update_home(data=employers):
        psiquiatria_card=psiquiatria(setores['Psiquiatria'])
        medicina1_card=medicina(setores['Medicina 1'])
        laboratorio_card=laboratorio(setores['Laboratório'])
        maternidade_card=maternidade(setores['Maternidade'])
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
                                ft.Card(content=tabela(data,page,atualizar_app),height=page.window_height-medicina1_card.height-10),
 
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
        funcoes_demo.content=ft.Text(value[0])
        page.update()

    def done(e):
        value=re.split(" ",str(nascimento.value))
        nascimento_demo.content=ft.Text(value[0])
        page.update()
    nascimento_demo=ft.Container()
    nascimento=ft.DatePicker(
                    first_date=datetime(year=2000, month=1, day=1),
                    last_date=datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day),
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
    label="Sector",
    width=160,
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
    width=160,
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
    label="Sector",
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
        ft.dropdown.Option("Nenhuma Reparticao"),
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
    estado = ft.Dropdown(
    label="Estado",
    width=160,
    options=[
        ft.dropdown.Option("ACTIVO"),
        ft.dropdown.Option("LICENCA/FERIAS"),
        ft.dropdown.Option("APOSENTADO"),
        ft.dropdown.Option("SUSPENSO"),
        ft.dropdown.Option("DELETADO"),
        ft.dropdown.Option("TRANSFERIDO"),
        ft.dropdown.Option("FALECIDO"),
        ]
    )

    def find_searching(e):
        datas=update_employer(getFuncionariosByQuery(e.control.value))
        page.update()

    #telas
    page_home=home(page)
    page_employers=employer(page)
    page_assistente=assistente(page)
    page_licenca=ft.Container(content=ft.Row(height=100,width=100,controls=[ft.ProgressRing(bgcolor=ft.colors.ORANGE_500,height=50,width=50)],alignment=ft.MainAxisAlignment.CENTER))

    search_input=ft.TextField(label="Pesquisar",on_submit=find_searching,width=170)
    filtrar=ft.Dropdown(
        label="filtrar por",
        width=160,
        options=[
            
            ft.dropdown.Option("Provincia"),
            ft.dropdown.Option("Sector"),
            ft.dropdown.Option("Genero"),
            ft.dropdown.Option("Estado"),
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

    async def atualizar_employers():
        global employers
    
        if employers:
            body.content = page_employers
            page.update()
            novosdados = await asyncio.to_thread(getFuncionarios)
            
            if novosdados != employers:
                update_employer(novosdados)
                page.update()
                employers = novosdados  # Atualiza a variável global com os novos dados
            else:
                pass
                
        else:
            body.content = page_employers
            page.update()

    async def employersLicenca():
        tabela=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Funcionario")),
                ft.DataColumn(ft.Text("Dias a Descancar")),
                ft.DataColumn(ft.Text("Dias Restantes")),
                ft.DataColumn(ft.Text("Data do inicio das ferias")),
                ft.DataColumn(ft.Text("Termina no dia")),
                ft.DataColumn(ft.Text("Estado"))
            ],
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300),)
        ferias = []
        if ferias:
            body.content = page_licenca
            page.update()
        else:
            body.content = page_licenca
            page.update()
            novos_dados = await asyncio.to_thread(getCustomFerias)
            for feria in novos_dados:
                
                if int(feria['dias_restantes']>0): 
                    sinal=ft.Container(width=100,height=25,bgcolor=ft.colors.GREEN_500,border_radius=5,content=ft.Row(
                        controls=[ft.Text("ativo",color="white",weight='bold')],alignment=ft.MainAxisAlignment.CENTER))
                else:
                    sinal=ft.Container(width=100,height=25,bgcolor=ft.colors.ORANGE_500,border_radius=5,
                                       content=ft.Row(controls=[ft.Text("passado",color="white",weight='bold')]
                                                      ,alignment=ft.MainAxisAlignment.CENTER))
                tabela.rows.append(
                    ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(feria['funcionario'],weight='bold')),
                        ft.DataCell(ft.Text(feria['dias'])),
                        ft.DataCell(ft.Text(feria['dias_restantes'],weight='bold')),
                        ft.DataCell(ft.Text(formatar_data(feria['inicio']))),
                        ft.DataCell(ft.Text(formatar_data(feria['fim']))),
                        ft.DataCell(sinal),
                        
                    ],
                ),
                )
            def search_emp_licenca(e):
                asyncio.run(employersLicenca)

            find=ft.TextField(label="procurar")
            page_licenca.content=ft.Column(controls=[
                ft.Row(height=160,controls=[
                    ft.Card(content=ft.Container(padding=10,content=ft.Column(controls=[
                        ft.Text("Filtrar Os Funcionarios em Licenca/Ferias",weight='bold',size=25,color=ft.colors.GREY_700),
                        ft.Row(controls=[
                            find,ft.CupertinoButton("buscar",bgcolor=ft.colors.GREEN_600,on_click=search_emp_licenca)
                        ],alignment=ft.MainAxisAlignment.CENTER)
                    ],alignment=ft.MainAxisAlignment.CENTER)))
                ]),
                tabela
            ])
            page.update()
            

    def  change_page(e):
        global curent_page
        index=e.control.selected_index
        if index==0:
            curent_page='home'
            asyncio.run(atualizar_home())
        elif index==1:
            curent_page="employers"
            asyncio.run(atualizar_employers())
        elif index==2:
            curent_page='licenca'
            asyncio.run(employersLicenca())
        elif index==3:
            curent_page='assistent'
            body.content=page_assistente
            page.update()
        elif index==4:
            atualizar_app(page)
            pass
        elif index==5:
            atualizar_app(page)
            pass
        elif index==7:
            page.client_storage.remove('token')
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
            "reparticao":reparticao.value,
            "especialidade": especialidade.value,
            "categoria": categoria.value,
            "nuit": nuit.value,
            "careira":careira.value,
            "faixa_etaria":faixa_etaria.value
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
    nascimento_btn=ft.ElevatedButton(
        icon=ft.icons.CALENDAR_MONTH,
        text="nascimento",
        on_click=open_nascimento,
        )
    funcoes_btn=ft.ElevatedButton(icon=ft.icons.CALENDAR_MONTH,text="Inicio das funcoes",on_click=open_funcoes)
    especialidade=ft.Dropdown(
        label="Especialidade",
        options=[
        ft.dropdown.Option('Cirurgia Geral'),
        ft.dropdown.Option('Oftalmologia'),
        ft.dropdown.Option('Cardiologia'),
        ft.dropdown.Option('Pediatria'),
        ft.dropdown.Option('Ginecologia e Obstetrícia'),
        ft.dropdown.Option('Ortopedia e Traumatologia'),
        ft.dropdown.Option('Anestesiologia'),
        ft.dropdown.Option('Radiologia'),
        ft.dropdown.Option('Legista'),
        ft.dropdown.Option('Otorrinolaringologia'),
        ft.dropdown.Option('Medicina Interna'),
        ft.dropdown.Option('Urologia')
    ],
    )
    faixa_etaria=ft.Dropdown(
        label="Faixa Etaria",
        options=[
            ft.dropdown.Option('11-18 anos: Adolescentes'),
            ft.dropdown.Option('19-29 anos: Jovens adultos'),
            ft.dropdown.Option('30-39 anos: Adultos'),
            ft.dropdown.Option('40-49 anos: Meia-idade'),
            ft.dropdown.Option('50-64 anos: Pré-idosos'),
            ft.dropdown.Option('65+ anos: Idosos')
        ]
    )
    categoria = ft.Dropdown(
    label="Categoria",
    options=[
        ft.dropdown.Option("Agente de farmácia"),
        ft.dropdown.Option("Agente de Medicina preventiva"),
        ft.dropdown.Option("Agente de serviço"),
        ft.dropdown.Option("Assistente Administrativo D"),
        ft.dropdown.Option("Assistente técnico"),
        ft.dropdown.Option("Auxiliar administrativo"),
        ft.dropdown.Option("Auxiliar de Farmácia"),
        ft.dropdown.Option("Carpinteiro"),
        ft.dropdown.Option("Condutor de veículos de serviço"),
        ft.dropdown.Option("Cozinheiro"),
        ft.dropdown.Option("Documentalista A"),
        ft.dropdown.Option("Enfermeira Pediatra"),
        ft.dropdown.Option("Enfermeira Saúde Materno-Infantil"),
        ft.dropdown.Option("Enfermeiro"),
        ft.dropdown.Option("Enfermeiro A"),
        ft.dropdown.Option("Enfermeiro de SMI A"),
        ft.dropdown.Option("Enfermeiro Geral"),
        ft.dropdown.Option("Enfermeiro Geral Especializado"),
        ft.dropdown.Option("Especialista de Saúde"),
        ft.dropdown.Option("Farmacêutico A"),
        ft.dropdown.Option("Fisioterapeuta A"),
        ft.dropdown.Option("Inspeção Superior"),
        ft.dropdown.Option("Jurista A"),
        ft.dropdown.Option("Médica Hospitalar Assistente"),
        ft.dropdown.Option("Médico de Clínica Geral"),
        ft.dropdown.Option("Médico de Clínica Geral de 1A"),
        ft.dropdown.Option("Médico de Clínica Geral de 2A"),
        ft.dropdown.Option("Médico Dentista"),
        ft.dropdown.Option("Médico Hospitalar Assistente"),
        ft.dropdown.Option("Nutricionista A"),
        ft.dropdown.Option("Outra"),
        ft.dropdown.Option("Psicólogo A"),
        ft.dropdown.Option("Servente de unidades sanitárias"),
        ft.dropdown.Option("Técnico"),
        ft.dropdown.Option("Técnico administrativo C"),
        ft.dropdown.Option("Técnico de Ação Social B"),
        ft.dropdown.Option("Técnico de Odontoestomatologia"),
        ft.dropdown.Option("Técnico de Oftalmologia"),
        ft.dropdown.Option("Técnico de Optometria A"),
        ft.dropdown.Option("Técnico de Psiquiatria e Saúde Mental"),
        ft.dropdown.Option("Técnico de Radiologia"),
        ft.dropdown.Option("Técnico de Radiologia A"),
        ft.dropdown.Option("Técnico Especializado de Saúde"),
        ft.dropdown.Option("Técnico Profissional"),
        ft.dropdown.Option("Técnico de Laboratório"),
        ft.dropdown.Option("Técnico de Laboratório A"),
        ft.dropdown.Option("Técnico de Manutenção D"),
        ft.dropdown.Option("Técnico de Medicina"),
        ft.dropdown.Option("Técnico de Medicina Física e Reabilitação"),
        ft.dropdown.Option("Técnico de Nutrição"),
        ft.dropdown.Option("Técnico de Administração Hospitalar"),
        ft.dropdown.Option("Técnico de Anestesiologia"),
        ft.dropdown.Option("Técnico de Cirurgia A"),
        ft.dropdown.Option("Técnico de Electromedicina"),
        ft.dropdown.Option("Técnico de Electrónica C"),
        ft.dropdown.Option("Técnico de Estatística Sanitária"),
        ft.dropdown.Option("Técnico de Farmácia"),
        ft.dropdown.Option("Técnico de Instrumentação")
    ]
)

    nuit=ft.TextField(label="Nuit" )

   
    
    bi=ft.TextField(label="Numero de BI" )
    def change_province(e):
        if provincia.value == "Niassa":
            naturalidade.options = [
                ft.dropdown.Option("Cuamba"),
                ft.dropdown.Option("Lago"),
                ft.dropdown.Option("Lichinga"),
                ft.dropdown.Option("Majune"),
                ft.dropdown.Option("Mandimba"),
                ft.dropdown.Option("Marrupa"),
                ft.dropdown.Option("Maúa"),
                ft.dropdown.Option("Mavago"),
                ft.dropdown.Option("Mecanhelas"),
                ft.dropdown.Option("Mecula"),
                ft.dropdown.Option("Metarica"),
                ft.dropdown.Option("Muembe"),
                ft.dropdown.Option("Ngauma"),
                ft.dropdown.Option("N'gauma"),
                ft.dropdown.Option("Nipepe"),
                ft.dropdown.Option("Sanga"),
            ]
        elif provincia.value == "Nampula":
            naturalidade.options = [
                ft.dropdown.Option("Angoche"),
                ft.dropdown.Option("Eráti"),
                ft.dropdown.Option("Ilha de Moçambique"),
                ft.dropdown.Option("Lalaua"),
                ft.dropdown.Option("Malema"),
                ft.dropdown.Option("Meconta"),
                ft.dropdown.Option("Mecubúri"),
                ft.dropdown.Option("Memba"),
                ft.dropdown.Option("Mogincual"),
                ft.dropdown.Option("Mogovolas"),
                ft.dropdown.Option("Moma"),
                ft.dropdown.Option("Monapo"),
                ft.dropdown.Option("Mossuril"),
                ft.dropdown.Option("Muecate"),
                ft.dropdown.Option("Murrupula"),
                ft.dropdown.Option("Nacala-a-Velha"),
                ft.dropdown.Option("Nacala Porto"),
                ft.dropdown.Option("Nampula"),
                ft.dropdown.Option("Rapale"),
                ft.dropdown.Option("Ribaué"),
            ]
        elif provincia.value == "Cabo Delgado":
            naturalidade.options = [
                ft.dropdown.Option("Ancuabe"),
                ft.dropdown.Option("Balama"),
                ft.dropdown.Option("Chiúre"),
                ft.dropdown.Option("Ibo"),
                ft.dropdown.Option("Macomia"),
                ft.dropdown.Option("Mecúfi"),
                ft.dropdown.Option("Meluco"),
                ft.dropdown.Option("Metuge"),
                ft.dropdown.Option("Mocímboa da Praia"),
                ft.dropdown.Option("Montepuez"),
                ft.dropdown.Option("Mueda"),
                ft.dropdown.Option("Muidumbe"),
                ft.dropdown.Option("Namuno"),
                ft.dropdown.Option("Nangade"),
                ft.dropdown.Option("Palma"),
                ft.dropdown.Option("Pemba"),
                ft.dropdown.Option("Quissanga"),
            ]
        elif provincia.value == "Zambézia":
            naturalidade.options = [
                ft.dropdown.Option("Alto Molócue"),
                ft.dropdown.Option("Chinde"),
                ft.dropdown.Option("Derre"),
                ft.dropdown.Option("Gilé"),
                ft.dropdown.Option("Gurué"),
                ft.dropdown.Option("Ile"),
                ft.dropdown.Option("Inhassunge"),
                ft.dropdown.Option("Luabo"),
                ft.dropdown.Option("Lugela"),
                ft.dropdown.Option("Maganja da Costa"),
                ft.dropdown.Option("Milange"),
                ft.dropdown.Option("Mocuba"),
                ft.dropdown.Option("Mopeia"),
                ft.dropdown.Option("Morrumbala"),
                ft.dropdown.Option("Mulevala"),
                ft.dropdown.Option("Namacurra"),
                ft.dropdown.Option("Namarroi"),
                ft.dropdown.Option("Nicoadala"),
                ft.dropdown.Option("Pebane"),
                ft.dropdown.Option("Quelimane"),
            ]
        elif provincia.value == "Tete":
            naturalidade.options = [
                ft.dropdown.Option("Angónia"),
                ft.dropdown.Option("Cahora-Bassa"),
                ft.dropdown.Option("Changara"),
                ft.dropdown.Option("Chifunde"),
                ft.dropdown.Option("Chiuta"),
                ft.dropdown.Option("Doa"),
                ft.dropdown.Option("Macanga"),
                ft.dropdown.Option("Magoé"),
                ft.dropdown.Option("Marávia"),
                ft.dropdown.Option("Marávia"),
                ft.dropdown.Option("Moatize"),
                ft.dropdown.Option("Mutarara"),
                ft.dropdown.Option("Tsangano"),
                ft.dropdown.Option("Zumbo"),
            ]
        elif provincia.value == "Sofala":
            naturalidade.options = [
                ft.dropdown.Option("Beira"),
                ft.dropdown.Option("Búzi"),
                ft.dropdown.Option("Caia"),
                ft.dropdown.Option("Chemba"),
                ft.dropdown.Option("Cheringoma"),
                ft.dropdown.Option("Chibabava"),
                ft.dropdown.Option("Dondo"),
                ft.dropdown.Option("Gorongosa"),
                ft.dropdown.Option("Machanga"),
                ft.dropdown.Option("Maringué"),
                ft.dropdown.Option("Marromeu"),
                ft.dropdown.Option("Nhamatanda"),
            ]
        elif provincia.value == "Manica":
            naturalidade.options = [
                ft.dropdown.Option("Bárue"),
                ft.dropdown.Option("Chimoio"),
                ft.dropdown.Option("Gondola"),
                ft.dropdown.Option("Guro"),
                ft.dropdown.Option("Macate"),
                ft.dropdown.Option("Machaze"),
                ft.dropdown.Option("Macossa"),
                ft.dropdown.Option("Manica"),
                ft.dropdown.Option("Mavonde"),
                ft.dropdown.Option("Mossurize"),
                ft.dropdown.Option("Sussundenga"),
                ft.dropdown.Option("Tambara"),
            ]
        elif provincia.value == "Inhambane":
            naturalidade.options = [
                ft.dropdown.Option("Funhalouro"),
                ft.dropdown.Option("Govuro"),
                ft.dropdown.Option("Homoíne"),
                ft.dropdown.Option("Inhambane"),
                ft.dropdown.Option("Inharrime"),
                ft.dropdown.Option("Inhassoro"),
                ft.dropdown.Option("Jangamo"),
                ft.dropdown.Option("Massinga"),
                ft.dropdown.Option("Maxixe"),
                ft.dropdown.Option("Morrumbene"),
                ft.dropdown.Option("Panda"),
                ft.dropdown.Option("Vilanculos"),
                ft.dropdown.Option("Zavala"),
            ]
        elif provincia.value == "Gaza":
            naturalidade.options = [
                ft.dropdown.Option("Bilene"),
                ft.dropdown.Option("Chibuto"),
                ft.dropdown.Option("Chicualacuala"),
                ft.dropdown.Option("Chigubo"),
                ft.dropdown.Option("Chókwè"),
                ft.dropdown.Option("Guijá"),
                ft.dropdown.Option("Mabalane"),
                ft.dropdown.Option("Manjacaze"),
                ft.dropdown.Option("Mapai"),
                ft.dropdown.Option("Massangena"),
                ft.dropdown.Option("Massingir"),
                ft.dropdown.Option("Xai-Xai"),
            ]
        elif provincia.value == "Maputo":
            naturalidade.options = [
                ft.dropdown.Option("Boane"),
                ft.dropdown.Option("Magude"),
                ft.dropdown.Option("Manhiça"),
                ft.dropdown.Option("Marracuene"),
                ft.dropdown.Option("Matola"),
                ft.dropdown.Option("Matutuíne"),
                ft.dropdown.Option("Moamba"),
                ft.dropdown.Option("Namaacha"),
            ]
        elif provincia.value == "Cidade de Maputo":
            naturalidade.options = [
                ft.dropdown.Option("Distrito Urbano 1"),
                ft.dropdown.Option("Distrito Urbano 2"),
                ft.dropdown.Option("Distrito Urbano 3"),
                ft.dropdown.Option("Distrito Urbano 4"),
                ft.dropdown.Option("Distrito Urbano 5"),
            ]
            
        page.update()

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
            ],
            on_change=change_province
        )
    provincia_s = ft.Dropdown(
            label="Província",
            width=140,
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
    
    naturalidade=ft.Dropdown(label="Natualidade")
    residencia = ft.Dropdown(
    label="Residencia",
    options=[
        ft.dropdown.Option("Estação"),
        ft.dropdown.Option("Cimento"),
        ft.dropdown.Option("Cerâmica"),
        ft.dropdown.Option("Barragem"),
        ft.dropdown.Option("Liberdade"),
        ft.dropdown.Option("Missão"),
        ft.dropdown.Option("Chiuaula"),
        ft.dropdown.Option("Sanjala"),
        ft.dropdown.Option("Lurio"),
        ft.dropdown.Option("Chuilucuto"),
        ft.dropdown.Option("Namacula"),
        ft.dropdown.Option("Mutapassa"),
        ]
    )


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
                nome,apelido,ft.Row(controls=[nascimento_btn,nascimento_demo]),bi,nuit,faixa_etaria,provincia,naturalidade,
            ]),
            ft.Column(controls=[
                residencia,sexo,ft.Row(controls=[funcoes_btn,funcoes_demo]),especialidade,categoria,careira,sector,reparticao
            ]),
            ]), progressBar,demo_erro
           ,
           
        ]),
        actions=[
            ft.CupertinoButton("Cadastrar o Funcionario",bgcolor=ft.colors.GREEN_700,width=600,on_click=add)
        ],
    
    )
    def cl(e):
        perfil.open=False
        page.update()

    def open_cadastro_dialogo(e):
        page.dialog=cadastro_dialogo
        cadastro_dialogo.open=True
        page.update()

    perfil=ft.AlertDialog(title=ft.Text("Perfil"),)
    def seeprofile(e):
        usuario=getUser(token)

        perfil.content=ft.Column(height=140,controls=[
                ft.Row(
                    controls=[
                        ft.Text("Nome: ",weight="bold"),ft.Text(usuario['username'])
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text("Contact: ",weight="bold"),ft.Text(usuario['contact'])
                    ]
                ),
                ft.ElevatedButton("minimizar",bgcolor=ft.colors.GREEN_600,on_click=cl,color="white")
        ])
        page.dialog=perfil
        perfil.open=True
        page.update()


    def log_out(e):
        page.client_storage.remove("token")
        atualizar_app(page)

    
    new_user_dlg=ft.AlertDialog(title=ft.Text("Novo Usuario"))
    new_username=ft.TextField(label="Nome do Usuario")
    new_contact=ft.TextField(label="Contacto")
    new_pass=ft.TextField(label="senha")


    alert_erro=ft.AlertDialog(title=ft.Text("Erro Ao Cadastrar"),content=ft.Row(controls=[
        ft.Icon(ft.icons.ERROR,color="red"),ft.Text("Ocorreu um erro ao cadastrar!")
    ]))
    alert_sucesso=ft.AlertDialog(title=ft.Text("Feito com exito"),content=ft.Row(controls=[
        ft.Icon(ft.icons.INFO,color="green"),ft.Text("Cadastrado com sucesso")
    ]))

    def alert_s():
        page.dialog=alert_sucesso
        alert_sucesso.open=True
        page.update()

    def alert_e():
        page.dialog=alert_erro
        alert_erro.open=True
        page.update()
    def add_new_user(e):
        data={
        "name":new_username.value,
        "contact":new_contact.value,
        "password":new_pass.value}
        status_code=NovoUsuario(data)
        if status_code ==200:
            #print("cadastrado")
            alert_s()
        else:
            #print("ocoreu um erro")
            alert_e()

    def new_user(e):
        page.dialog=new_user_dlg
        new_user_dlg.open=True
        new_user_dlg.content=ft.Column(height=240,controls=[
            new_username,new_contact,new_pass,
            ft.CupertinoButton("Cadastrar",bgcolor=ft.colors.GREEN_600,width=300,on_click=add_new_user)
        ])
        page.update()

    # Ações do AppBar
    pm=ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem("Ver Perfil",on_click=seeprofile),
            ft.PopupMenuItem("Terminar sessao",on_click=log_out),
            ft.PopupMenuItem("Novo usuario",on_click=new_user)
        ]
    )
    def change_mode(e):
        if page.theme_mode=='light':
            page.theme_mode='dark'
            page.appbar.bgcolor=ft.colors.PURPLE_900
        else:
            page.theme_mode='light'
            page.appbar.bgcolor=ft.colors.GREEN_700
        page.update()
    page.appbar = ft.AppBar(
        bgcolor=ft.colors.GREEN_700,
        color=ft.colors.WHITE,
        leading=ft.Icon(ft.icons.LOCAL_HOSPITAL),
        title=ft.Text("Hospital de Lichinga"),
        actions=[ft.IconButton(ft.icons.LIGHT_MODE,on_click=change_mode),pm]
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
                icon_content=ft.Icon(ft.icons.PEOPLE),
                selected_icon_content=ft.Icon(ft.icons.PEOPLE),
                label="Licenca/Reriado",
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


    


# Executa o aplicativo
ft.app(target=main)
