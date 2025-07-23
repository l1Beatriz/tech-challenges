# DOC: https://docs.python.org/3/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET

# 1. Abrir o arquivo XML original 
arquivo_original = 'localizationExemplo.xml'

tree = ET.parse(arquivo_original)  # Ler o XML e montar a "árvore"
root = tree.getroot()  # Acessa o elemento raiz - <localization>

# 2. Definir o namespace usado no XML 
# Isso é necessário porque o XML possui um "xmlns" especial na tag <localization>
ns = {'ns': 'http://nasajon.com/schemas/localizationExemplo.xsd'}
 

# 3. Alterar o idioma para português brasileiro 
root.set('culture', 'pt-BR')  # Troca culture="en" por culture="pt-BR"

# 4. Traduzir os textos 
# Encontra todos os elementos <string> dentro do XML
for string in root.findall('.//ns:string', ns):
    texto_original = string.text  # Pega o texto atual em inglês
    print(f'Texto original: {texto_original}')  # Mostra no terminal

    # Solicita ao usuário a tradução do texto
    traducao = input('Digite a tradução para o português: ')

    # Substitui o texto original pela tradução
    string.text = traducao

# 5. Salvar o novo arquivo traduzido
arquivo_traduzido = 'localization_ptBR.xml'
tree.write(arquivo_traduzido, encoding='utf-8', xml_declaration=True)

# 6. Finalização
print(f'\n✅ Tradução concluída com sucesso!')
print(f'Arquivo salvo como: {arquivo_traduzido}')