from data_set import dataset
from verificacao import detectar_rubricas_incomuns, detectar_variacao_bruta

# Executar verificações
rubricas_incomuns = detectar_rubricas_incomuns(dataset)
variacoes_brutas = detectar_variacao_bruta(dataset)

# Mostrar resultados
print("Rubricas reaparecendo após 6 meses:")
for alerta in rubricas_incomuns:
    print(alerta)

print("\nDescontos com variação brusca:")
for alerta in variacoes_brutas:
    print(alerta)
