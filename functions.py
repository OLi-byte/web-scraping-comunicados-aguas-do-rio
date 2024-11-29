def break_lines(texto, tamanho_maximo):
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


def veriry_keywords(keywords, title, text):
    for word in keywords:
        if word in title or word in text:
            return True
    return False
