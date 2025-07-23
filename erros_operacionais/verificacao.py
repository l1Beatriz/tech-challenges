from collections import defaultdict

def detectar_rubricas_incomuns(dataset):
    """
    Situação 1: Rubrica de RENDIMENTO que aparece no mês atual e 
    não apareceu nos últimos 6 meses.
    """
    historico = defaultdict(list)
    resultados = []

    # descobrir o mês mais atual
    mes_atual = max((item["ano_calculo"], item["mes_calculo"]) for item in dataset)

    # armazenar histórico de rubricas RENDIMENTO
    for item in dataset:
        if item["tipo_rubrica"] == "RENDIMENTO":
            chave = (item["cpf"], item["codigo_rubrica"])
            data = (item["ano_calculo"], item["mes_calculo"])
            historico[chave].append(data)

    # verificar quais rendimentos reapareceram após 6 meses
    for item in dataset:
        if item["tipo_rubrica"] != "RENDIMENTO":
            continue

        chave = (item["cpf"], item["codigo_rubrica"])
        data = (item["ano_calculo"], item["mes_calculo"])

        if data == mes_atual:
            ultimos_6_meses = [(mes_atual[0], mes_atual[1] - i) for i in range(1, 7)]
            if not any(mes in historico[chave] for mes in ultimos_6_meses):
                resultados.append({
                    "nome": item["nome"],
                    "cpf": item["cpf"],
                    "rubrica": item["codigo_rubrica"],
                    "mensagem": "Rubrica de rendimento reapareceu após 6 meses."
                })

    return resultados


def detectar_variacao_bruta(dataset):
    """
    Situação 2: Rubrica de DESCONTO com variação >= 5% em relação
    à média dos últimos 6 meses.
    """
    historico = defaultdict(list)
    alertas = []

    # descobrir o mês mais atual
    mes_atual = max((item["ano_calculo"], item["mes_calculo"]) for item in dataset)

    # agrupar histórico de descontos
    for item in dataset:
        if item["tipo_rubrica"] == "DESCONTO":
            chave = (item["cpf"], item["codigo_rubrica"])
            data = (item["ano_calculo"], item["mes_calculo"])
            historico[chave].append((data, item["valor"]))

    # verificar variação
    for chave, valores in historico.items():
        valores.sort()
        valores_anteriores = [v for d, v in valores if d < mes_atual]
        valores_atuais = [v for d, v in valores if d == mes_atual]

        if valores_atuais and valores_anteriores:
            media = sum(valores_anteriores[-6:]) / min(6, len(valores_anteriores))
            atual = valores_atuais[0]
            variacao = abs(atual - media) / media

            if variacao >= 0.05:
                alertas.append({
                    "cpf": chave[0],
                    "rubrica": chave[1],
                    "media_anterior": round(media, 2),
                    "valor_atual": atual,
                    "variacao_percentual": round(variacao * 100, 2),
                    "mensagem": "Desconto com variação brusca detectada."
                })

    return alertas
