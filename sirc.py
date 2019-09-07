from tkinter import filedialog
from tkinter import *
import os, docx, csv

####################################################################
######################  Evento 01  #################################
##### Indicar o arquivo de dados para os calculos necessários ######
############ Button - Indique o arquivo de dados ###################
####################################################################

dadosData = []
def mfileopen():
    # Primeiro ela armazena o nome dado à planilha de dados indicada via interface
    # e renomea esta planilha como "arquivo"
    arquivo = filedialog.askopenfilename()

    # Abrimos o arquivo, deixamos ele pronto para leitura e convertemos a planilha para uma lista de dados
    dadosFile = open(arquivo)
    dadosReader = csv.reader(dadosFile)
    global dadosData
    dadosData = list(dadosReader)


####################################################################
######################  Evento 02  #################################
#######Indica o diretório onde as recomendações serão salvas #######
######## Button - Diretório onde os arquivos serão salvos ##########
####################################################################

def mDirectotyopen():
    # Primeiro ela armazena o nome dado à planilha que foi digitado na caixa da interface
    # e renomear como "arquivo"
    global diretorio
    diretorio = str(filedialog.askdirectory())
    os.chdir(diretorio)

####################################################################
######################  EVENTO 03  #################################
######### Cálculos necessários e produção das recomendações ########
########## Button - Gerar recomendações para as amostras ###########
####################################################################

# Criamos uma função "gerarRecomendacao" que fará todos os procedimentos para a recomendação de calagem

def gerarRecomendacao():

    # Dentro da função criamos um arquivo .docx vazio que receberá os dados de recomendação das amostras
    # Sendo que, para cada amostra será gerado um arquivo diferente.docx, ao final de cada looping

    doc = docx.Document()

    # O looping for irá verificar linha por linha da nossa planilha de dados

    for row in dadosData:

        # Uma instrução if que faz com que o laço ignore
        # a primeira linha da planilha de dados (o cabeçalho)
        # mas que a partir da segunda linha passe a fazer a leitura de dados de cada amostra

        if str(row[0]) != str('Amostra'):

            # Buscamos os dados de acordo com seu indice em cada linha da planilha
            # Convertemos os dados para o tipo de dados que cada um represente
            # Armazenamos os dados em variáveis com nomes mais familiares
            # Os três passos acima são feitos para cada linha da planilha
            # Onde cada linha representa uma amostra de solo diferente

            # amx refere-se ao nome em que o que arquivo de recomendação será salvo utilizando a função
            # doc.save() dentro do loop
            amx = str(row[1]) + '.docx'
            am = str(row[1])
            pro = str(row[2])
            k = float(row[5])
            na = float(row[6])
            ca = float(row[7])
            mg = float(row[8])
            alh = float(row[10])
            v1 = float(row[11])
            x = float(row[12])
            ta = str(row[13])
            pf = float(row[14])
            li = float(row[15])
            el = float(row[16])
            fc = float(row[17])
            lbc = float(row[18])
            cbc = float(row[19])
            base_menor = float(row[20])
            base_maior = float(row[21])

            # à seguir são realizados alguns calculos para conversão e ajuste dos dados obtidos da planilha

            # Tranformação do K e o Na de mg/dm³ para cmolc/dm³
            k = k/390
            na = na/230

            # CTC potencial
            ctctotal = ca + mg + k + na + alh

            # Soma de Bases
            sb = ca + mg + k + na

            # Saturação por bases
            v2 = sb/ctctotal * 100

            # Número de plantas por hectare
            numplant = 10000/(el * li)

            # Calculos para aplicação de calcário em sulco
            vol_de_sulco = ((((base_maior + base_menor)*(pf/100)/2)*(100/el*100))*1000)
            perc_vol_de_sulco = vol_de_sulco/(1000*1000*pf/10)

            # Calculamos também a Necessidade de calagem por 3 diferentes métodos
            # Metódo 1 - Soma de bases
            ncm1 = ((ctctotal * (v1 - v2)) / 100) * (20/pf)

            # Metódo 2 - Soma de cálcio e mágnesio ideal para a cultura
            ncm2 = (x - (ca + mg))

            # Metódo 3 - Teor de H + Al
            ncm3 = alh

            # A condicional If faz a decisão de qual metódo apresenta valor adequado como necessidade de calagem
            # com base nas recomendações de ..... et al ()
            if ncm1 >= ncm2:
                nc = ncm1
            elif ncm2 <= ncm3:
                nc = ncm2
            else:
                nc = ncm3

            # qc representa a quantidade de calcário segundo a profundidade a ser aplicado em caso de área total
            qc = nc * pf/20

        # A Condicional if elseif else fará a converção de necessidade de calagem (agora chamada de qc) para
        # a quantidade de calcário necessário para diferentes métodos de aplicação (faixa, sulco, em cova e área total)
        # E geramos uma recomendação para cada amostra
            # Instruções para a recomendação para aplicação em faixa
            if ta == 'fx':

                # Conversão de qc para valores a serem aplicado no sulco em g de calcário/planta
                qc = (qc * 1000000) / numplant * fc/100

                # Texto da recomendação
                doc.add_paragraph('Prognóstico Para Calagem', 'Title')
                doc.add_paragraph('Amostra ' + am)
                doc.add_paragraph('Produtor: ' + pro)
                doc.add_heading('Quantidade de calcário', 1)
                p = doc.add_paragraph('Para a corrigir o pH do solo e elevar os teores de Ca e Mg indica-se preparar e '
                                  'aplicar %.2f g de calcário/planta' %qc)
                p.alignment = 3

                doc.save(amx)
                # Após o relatório ser salvo (linha acima),
                # a linha abaixo é introduzida para que um novo arquivo .docx vazio seja criado
                # e utilizado para criação da próxima recomendação
                doc = docx.Document()


            # Instruções para a recomendação para aplicação em sulco
            elif ta == 'sc':

                # Conversão de qc para valores a serem aplicado no sulco em g de calcário/metro de sulco
                qc = (qc * perc_vol_de_sulco)/(100/el*100)*1000000

                # Texto da recomendação
                doc.add_paragraph('Prognóstico Para Calagem', 'Title')
                doc.add_paragraph('Amostra ' + am)
                doc.add_paragraph('Produtor - ' + pro)
                doc.add_heading('Quantidade de calcário', 1)
                p = doc.add_paragraph('Para a corrigir o pH do solo e elevar os teores de Ca e Mg indica-se preparar e '
                                  'aplicar %.2f g de calcário/metro de suco' %qc)
                p.alignment = 3
                doc.save(amx)
                # Após o relatório ser salvo (linha acima),
                # a linha abaixo é introduzida para que um novo arquivo .docx vazio seja criado
                # e utilizado para criação da próxima recomendação
                doc = docx.Document()

            # Instruções para a recomendação para aplicação em cova/berço
            elif ta == 'cv':

                # Conversão de qc para valores a serem aplicado no sulco em g de calcário/metro de sulco
                qc = qc * 100 * lbc * cbc

                # Texto da recomendação
                doc.add_paragraph('Prognóstico Para Calagem', 'Title')
                doc.add_paragraph('Amostra ' + am)
                doc.add_paragraph('Produtor - ' + pro)
                doc.add_heading('Quantidade de calcário', 1)
                p = doc.add_paragraph('Para a corrigir o pH do solo e elevar os teores de Ca e Mg indica-se '
                                  'aplicar %.2f g de calcário/cova' %qc)
                p.alignment = 3

                doc.save(amx)
                # Após o relatório ser salvo (linha acima),
                # a linha abaixo é introduzida para que um novo arquivo .docx vazio seja criado
                # e utilizado para criação da próxima recomendação
                doc = docx.Document()

            # Instruções para a recomendação para aplicação em área total
            else:
                qc = nc
                doc.add_paragraph('Prognóstico Para Calagem', 'Title')
                doc.add_paragraph('Amostra ' + am)
                doc.add_paragraph('Produtor - ' + pro)
                doc.add_heading('Quantidade de calcário', 1)
                p = doc.add_paragraph('Para a corrigir o pH do solo e elevar os teores de Ca e Mg indica-se '
                                  'aplicar %.2f t de calcário/ha' %qc)
                p.alignment = 3

                doc.save(amx)
                # Após o relatório ser salvo (linha acima),
                # a linha abaixo é introduzida para que um novo arquivo .docx vazio seja criado
                # e utilizado para criação da próxima recomendação
                doc = docx.Document()

############################################################################################
######################  EVENTO 04  #########################################################
#Interpretador dos dados e relatório de amostras que possivelmente não precisam de calagem##
######## Button - Diagnóstico Prévio da necessidade de calagem #############################
############################################################################################

# Criamos uma função "reverAmostra" que fará todos os procedimentos de interpretação
# bucando encontrar dados que indiquem que a amostra não precisa de calagem

def reverAmostras():

    # Começamos Criamos um arquivo docx vazio que será utilizado dentro do loop
    doc = docx.Document()
    p = doc.add_paragraph('Amostras que precisão de uma revisão dos dados', 'Title')
    p.alignment = 1


    for row in dadosData:
        if str(row[0]) != str('Amostra'):
            # Primeiro armazenamos os dados em variáveis com nomes mais familiares
            am = str(row[1])
            ph = float(row[3])
            k = float(row[5])
            na = float(row[6])
            ca = float(row[7])
            mg = float(row[8])
            alh = float(row[10])

            # Tranformação do K e o Na de mg/dm³ para cmolc/dm³
            k = k/390
            na = na/230

            # Realizamos alguns calculos básicos
            ctctotal = float(ca + mg + k + na + alh)
            ratecamg = float(ca/mg)
            cactc = float(ca/ctctotal * 100)
            mgctc = float(mg/ctctotal * 100)

            # Utilizamos primeiramente o pH para verificarmos a necessidade de calagem
            if ph > 5.4:
                #Adicionar o numéro da amostra à lista vazia
                doc.add_heading('Identificação da amostra: %s' %am, 2)
                doc.add_paragraph('pH: %.2f' %ph)
                doc.add_paragraph('CTC da amostra: %.2f' %ctctotal)
                doc.add_paragraph('Percentagem de Ca na CTC: %.2f' %cactc)
                doc.add_paragraph('Percentagem de Mg na CTC: %.2f' %mgctc)
                doc.add_paragraph('Teor de H+Al: %.2f' %alh)
                doc.add_paragraph('Relação Ca/Mg: %.2f' %ratecamg)
                doc.save('Amostras_para_revisão_de_dados.docx')

####################################################################
######################  INTERFACE  #################################
####################################################################

janela = Tk()
janela.iconbitmap('arts/paper-pencil-and-calculator.ico')
janela.title("Interpretação e Recomendação de Calagem")
janela.geometry("600x300+200+200")
janela["bg"] = "snow2"

# EVENTO 01
# Botão para indicar o arquivo de dados
bt = Button(janela, width = 30, text = "Indique o arquivo de dados",
            command = mfileopen, bg = "black", fg="white").place(x = 200, y = 20)

# EVENTO 02
# Botão para indicar o diretório onde as recomendações e relatórios serão salvos
bt = Button(janela, width = 50, text = "Indique o diretório onde as recomendações serão salvas",
            command = mDirectotyopen, bg = "black", fg="white").place(x = 120, y = 50)

# EVENTO 03
# Botão para gerar um diagnóstico prévio da necessidade de calagem
bt = Button(janela, width=35, height = 2, text = "Diagnóstico prévio da necessidade de calagem",
            command = reverAmostras, bg = "black", fg="white").place(x = 20, y = 130)

# EVENTO 04
# Botão para gerar as recomendações e salvar no diretório indicado
bt = Button(janela, width = 35, height = 2, text = "Gerar recomendações para as amostras",
            command = gerarRecomendacao, bg = "black", fg="white").place(x = 330, y = 130)

logotipo = PhotoImage(file="arts/logotipo_ca.png")
label = Label(janela, image = logotipo).pack(side=BOTTOM)

janela.mainloop()