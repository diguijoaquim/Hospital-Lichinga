from reportlab.lib.pagesizes import landscape, A4, portrait
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime
from random import randint
import os
from controls import getDays, getRestante, formatar_data
from pathlib import Path
save_path = Path.home() / "Documents" / "RP"
save_path.mkdir(parents=True, exist_ok=True)

filename = ''
green_light = colors.HexColor('#E6F2E6')  # Define a cor verde clara globalmente

def create_pdf(dados):
    global filename
    filename = f"hospital_lichinga_{randint(1, 100)}.pdf"
    
    # Configurações básicas do documento PDF em formato paisagem
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Calcula as margens (padding) de 10% da largura da página
    padding = width * 0.1

    # Calcula a largura útil para a tabela
    table_width = width - 2 * padding

    # Cor de fundo verde leve
    # green_light = colors.HexColor('#E6F2E6')  # Cor verde clara definida globalmente

    # Cor de borda cinza mais claro
    border_color = colors.grey

    # Título e subtítulo
    titulo = "Hospital de Lichinga"
    subtitulo = "Sistema de Gestão de Recursos Humanos"
    data = formatar_data("2024-07-12")  # Formata a data aqui

    # Define o estilo para o texto do título e subtítulo
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - padding / 2, titulo)

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - padding, subtitulo)
    c.drawCentredString(width / 2, height - padding * 1.5, data)

    # Dados fictícios dos funcionários

    # Estilo de tabela com cores personalizadas, linhas e cantos arredondados
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), green_light),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Cor de fundo das células
        ('GRID', (0, 0), (-1, -1), 1, border_color),  # Borda da tabela com cor cinza claro
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('RADIUS', (0, 0), (-1, -1), 4)  # Raio dos cantos arredondados
    ])

    # Criação da tabela
    data_with_headers = [["Nome", "Naturalidade", "Setor", "Repartição", "Começou a Trabalhar em", "Morada"]]
    for func in dados:
        data_formatada = formatar_data(func['inicio_funcoes'])  # Formata a data aqui
        data_with_headers.append([func['nome'], f"{func['naturalidade']}/{func['provincia']}", func['sector'], func['reparticao'], data_formatada, func['residencia']])

    t = Table(data_with_headers, colWidths=[table_width/6]*6)  # Divide a largura igualmente entre as 6 colunas
    t.setStyle(style)

    # Calcula a altura da tabela
    w, h = t.wrapOn(c, table_width, height)

    # Posiciona a tabela um pouco abaixo do subtítulo, com 50 pixels de distância
    y = height - h - padding - 50
    x = padding
    t.drawOn(c, x, y)

    # Fecha o PDF
    c.save()
    os.startfile(filename)

def print_employer(employer):
    filename = f"{employer['nome']}_{randint(1, 100)}.pdf"
    
    # Configurações básicas do documento PDF em formato retrato (portrait)
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Título e subtítulo
    titulo = "Hospital de Lichinga"
    subtitulo = "Sistema de Gestão de Recursos Humanos"
    data_hoje = formatar_data(datetime.now().strftime("%Y-%m-%d"))  # Formata a data atual aqui

    # Define o estilo para o texto do título e subtítulo
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, titulo)

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 70, subtitulo)
    c.drawCentredString(width / 2, height - 90, data_hoje)

    # Dados do funcionário
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"Nome: {employer['nome']}")
    c.drawString(100, height - 170, f"Naturalidade: {employer['naturalidade']} / {employer['provincia']}")
    c.drawString(100, height - 190, f"Setor: {employer['sector']}")
    c.drawString(100, height - 210, f"Repartição: {employer['reparticao']}")
    c.drawString(100, height - 230, f"Começou a Trabalhar em: {formatar_data(employer['inicio_funcoes'])}")  # Formata a data aqui
    c.drawString(100, height - 250, f"Morada: {employer['residencia']}")
    c.drawString(100, height - 270, f"Data de Nascimento: {formatar_data(employer['nascimento'])}")  # Formata a data aqui
    c.drawString(100, height - 290, f"Especialidade: {employer['especialidade']}")
    c.drawString(100, height - 310, f"Categoria: {employer['categoria']}")
    c.drawString(100, height - 330, f"BI: {employer['bi']}")
    c.drawString(100, height - 350, f"NUIT: {employer['nuit']}")
    c.drawString(100, height - 370, f"Estado: {employer['status']}")

    # Verifica se o funcionário tem registro de férias
    if 'ferias' in employer and employer['ferias']:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 400, "Registros de Férias:")

        # Dados para a tabela de férias
        table_data = [["Início das Férias", "Fim das Férias", "Total de Dias", "Dias Restantes"]]
        for ferias in employer['ferias']:
            table_data.append([
                formatar_data(ferias['data_inicio_ferias']),  # Formata a data aqui
                formatar_data(ferias['data_fim_ferias']),  # Formata a data aqui
                getDays(data_inicio=ferias['data_inicio_ferias'], data_fim=ferias['data_fim_ferias']),
                getRestante(data_inicio=ferias['data_inicio_ferias'], data_fim=ferias['data_fim_ferias'])
            ])

        # Criação da tabela de férias
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), green_light),  # Cor de fundo do cabeçalho igual à principal
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Cor de fundo das células
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)  # Borda da tabela com cor cinza
        ])
        
        ferias_table = Table(table_data, colWidths=[100, 100, 100, 100])
        ferias_table.setStyle(table_style)

        # Desenhar a tabela no PDF
        w, h = ferias_table.wrapOn(c, width, height)
        ferias_table.drawOn(c, 100, height - 450 - h)

    # Fecha o PDF
    c.save()

    # Abre o PDF automaticamente (somente para Windows)
    os.startfile(filename)
