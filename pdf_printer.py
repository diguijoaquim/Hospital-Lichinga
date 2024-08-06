from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime
from random import randint
import os
from controls import getFuncionarios, DeleteEmployerByID, UpdateEmployer, GetEmployerByID,getSectores

filename=''
def create_pdf(dados):
    global filename
    filename=f"hospital_lichinga_{randint(1,100)}.pdf"
    
    # Configurações básicas do documento PDF em formato paisagem
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Calcula as margens (padding) de 10% da largura da página
    padding = width * 0.1

    # Calcula a largura útil para a tabela
    table_width = width - 2 * padding

    # Cor de fundo verde leve
    green_light = colors.HexColor('#E6F2E6')  # Escolha um tom de verde claro que você goste

    # Cor de borda cinza mais claro
    border_color = colors.grey

    # Título e subtítulo
    titulo = "Hospital de Lichinga"
    subtitulo = "Sistema de Gestão de Recursos Humanos"
    data = "12 de julho de 2024"

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
    data_with_headers = [["Nome", "Naturalidade", "Setor", "Repartição", "Comecou a Trabalhar em", "Morada"]]
    for func in dados:
        data=datetime.fromisoformat(func['inicio_funcoes'])
        data_with_headers.append([func['nome'],f"{func['naturalidade']}/{func['provincia']}",func['sector'],func['reparticao'],func['inicio_funcoes'],func['residencia']],)

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