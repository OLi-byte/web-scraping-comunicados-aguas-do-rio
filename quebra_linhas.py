def adicionar_quebras_de_linha(texto, tamanho_maximo):
    palavras = texto.split()

    linhas = []

    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > tamanho_maximo:
            linhas.append(linha_atual)
            linha_atual = palavra
        else:
            if linha_atual:
                linha_atual += " " + palavra
            else:
                linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return "\n".join(linhas)
