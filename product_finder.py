import requests
import csv
from datetime import datetime
import sqlite3


# Arquivo de estudo:
# output/promotion_history.db
#
# Objetivo:
# Organizar o Promotion Finder utilizando classes,
# aproximando o projeto de uma estrutura profissional.
#
# Conceitos praticados:
# - Orientação a Objetos
# - Classes
# - Métodos
# - Atributos
# - self
# - __init__
# - Separação de responsabilidades

# 1. Buscar produtos na API
# Fluxo:
# Requisição HTTP -> JSON -> Lista de produtos

# Classe principal do Promotion Finder
class PromotionFinder:

    def __init__(self):
        self.url = "https://dummyjson.com/products"
        self.nome_banco = "output/promotion_history.db"
        self.categoria_desejada = ""
        self.preco_maximo = 0
        self.avaliacao_minima = 0
        self.desconto_minimo = 0
        self.deseja_comparar = False

# Busca produtos na API   
    def buscar_produtos(self):

        resposta = requests.get(self.url)
        dados = resposta.json()
        produtos = dados["products"]

        return produtos
    
# Filtra produtos com base nos critérios escolhidos    
    def filtrar_produtos(self, produtos):
            
        produtos_filtrados = []

        for produto in produtos:
        
            preco = produto.get("price", 0)
            categoria = produto.get("category", "")
            avaliacao = produto.get("rating")
            desconto = produto.get("discountPercentage", 0)

       
            if (
                categoria == self.categoria_desejada
                and preco <= self.preco_maximo
                and avaliacao >= self.avaliacao_minima
                and desconto >= self.desconto_minimo
                     ):
                
                produtos_filtrados.append(produto)

        return produtos_filtrados
    
# Ordena produtos pelo menor preço    
    def ordenar_produtos(self, produtos):
        produtos_ordenados = sorted(produtos, key=lambda x: x["price"])
        
        return produtos_ordenados
    
    def gerar_promocoes(self, produtos):

        for produto in produtos:
            data_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nome = produto.get("title", "")
            preco = produto.get("price", 0)
            avaliacao = produto.get("rating", 0)
            desconto = produto.get("discountPercentage", 0)
            categoria = produto.get("category", "")

            print()
            print(f"📅 Data da Consulta: {data_consulta}")
            print(f"🛒 Produto: {nome}")
            print(f"💰 Preço: ${preco}")
            print(f"⭐ Avaliação: {avaliacao}")
            print(f"🏷️  Categoria: {categoria}")
            print(f"🔥 Desconto: {desconto}%")
            print("-" * 40)
            print()

        return produtos
    
# Exibe o menu e retorna a categoria escolhida    
    def escolher_categoria(self):
        while True: 
            print("Categorias disponíveis:")
            print("1 - beauty")
            print("2 - fragrances")
            print("3 - furniture")
            print("4 - groceries")

            opcao = input("Escolha uma categoria pelo número: ")

            if opcao == "1":
                return "beauty"
            elif opcao == "2":
                return "fragrances"
            elif opcao == "3":
                return "furniture"
            elif opcao == "4":
                return "groceries"
            else:
                print("Opção inválida. Tente novamente.\n")
        
# Exporta os produtos da execução atual para CSV
    def salvar_csv(self, produtos):
        with open("output/product_list_current.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Data da Consulta", "Produto", "Preço", "Desconto", "Avaliação", "Estoque", "Marca", "Categoria", "Imagem"])

            data_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for produto in produtos:
                nome = produto.get("title", "")
                preco = produto.get("price", 0)
                desconto = produto.get("discountPercentage", 0)
                avaliacao = produto.get("rating", 0)
                estoque = produto.get("stock", 0)
                marca = produto.get("brand", "Sem marca")
                imagem = produto.get("thumbnail", "")
                categoria = produto.get("category", "")

                escritor.writerow([data_consulta, nome, preco, desconto, avaliacao, estoque, marca, categoria, imagem])

        print(f"CSV atual salvo com {len(produtos)} produtos.")

# Cria o banco e a tabela de histórico
    def criar_banco(self):
       conexao = sqlite3.connect(self.nome_banco)
       cursor = conexao.cursor()

       cursor.execute("""
       CREATE TABLE IF NOT EXISTS produtos (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           data_consulta TEXT,
           produto TEXT,
           preco REAL,
           desconto REAL,
           avaliacao REAL,
           estoque INTEGER,
           marca TEXT,
           categoria TEXT,
           imagem TEXT
       )
       """)

       conexao.commit()
       conexao.close()

# Salva registros históricos do SQLite
    def salvar_historico_sqlite(self, produtos):
        conexao = sqlite3.connect(self.nome_banco)
        cursor = conexao.cursor()

        data_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for produto in produtos:
            nome = produto.get("title", "")
            preco = produto.get("price", 0)
            desconto = produto.get("discountPercentage", 0)
            avaliacao = produto.get("rating", 0)
            estoque = produto.get("stock", 0)
            marca = produto.get("brand", "Sem marca")
            categoria = produto.get("category", "")
            imagem = produto.get("thumbnail", "")

            cursor.execute("""
            INSERT INTO produtos (
                data_consulta,
                produto,
                preco,
                desconto,
                avaliacao,
                estoque,
                marca,
                categoria,
                imagem
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data_consulta,
                nome,
                preco,
                desconto,
                avaliacao,
                estoque,
                marca,
                categoria,
                imagem
            ))

        conexao.commit()
        conexao.close()

        print(f"Histórico SQLite salvo com {len(produtos)} produtos.")

# Carrega registros históricos do SQLite
    def carregar_historico_sqlite(self):
        conexao = sqlite3.connect(self.nome_banco)
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT produto, preco
        FROM produtos
        """)

        registros = cursor.fetchall()

        historico = []

        for registro in registros:
            historico.append({
                "Produto": registro[0],
                "Preço": registro[1]
            })

        conexao.close()

        return historico


# Compara preços atuais com o menor preço histórico
    def comparar_precos(self, produtos_atuais):
        conexao = sqlite3.connect(self.nome_banco)
        cursor = conexao.cursor()

        print("\n📊 Comparação com histórico:")

        for produto in produtos_atuais:
            nome = produto.get("title", "")
            preco_atual = produto.get("price", 0)

            # Simulação temporária para testar novo menor preço
            # if nome == "Red Nail Polish":
                #preco_atual = 7.99

            cursor.execute("""
            SELECT MIN(preco)
            FROM produtos
            WHERE produto = ?
            """, (nome,))

            resultado = cursor.fetchone()
            menor_preco_historico = resultado[0]

            print(f"\n🛒 Produto: {nome}")
            print(f"💰 Preço atual: ${preco_atual}")

            if menor_preco_historico is None:
                print("📌 Produto sem histórico anterior.")
            else:
                print(f"📉 Menor preço histórico: ${menor_preco_historico}")

                if preco_atual < menor_preco_historico:
                    economia = menor_preco_historico - preco_atual
                    percentual = (economia / menor_preco_historico) * 100

                    print("🔥 NOVO MENOR PREÇO!")
                    print(f"💵 Economia: ${economia:.2f}")
                    print(f"📊 Desconto real vs histórico: {percentual:.2f}%")
                else:
                    print("Sem novo menor preço.")

            print("-" * 40)

        conexao.close()

# Gera alertas quando encontra novo menor preço
    def gerar_alertas(self, produtos_atuais):
        conexao = sqlite3.connect(self.nome_banco)
        cursor = conexao.cursor()

        alertas = []

        for produto in produtos_atuais:
            nome = produto.get("title", "")
            preco_atual = produto.get("price", 0)

            # Simulação temporária para testar novo menor preço
            # Simulação temporária para testar envio de alerta no Telegram
            # Remover na versão final

            if nome == "Red Nail Polish":
                preco_atual = 7.99

            cursor.execute("""
            SELECT MIN(preco)
            FROM produtos
            WHERE produto = ?
            """, (nome,))

            resultado = cursor.fetchone()
            menor_preco_historico = resultado[0]

            if menor_preco_historico is not None and preco_atual < menor_preco_historico:
                economia = menor_preco_historico - preco_atual
                percentual = (economia / menor_preco_historico) * 100

                alerta = {
                    "produto": nome,
                    "preco_atual": preco_atual,
                    "menor_preco_historico": menor_preco_historico,
                    "economia": economia,
                    "percentual": percentual
                }

                alertas.append(alerta)

        conexao.close()

        return alertas

# Exibe alertas no terminal
    def exibir_alertas(self, alertas):
        if not alertas:
            print("\nNenhum alerta de promoção encontrado.")
            return

        print("\n🔥 ALERTAS DE PROMOÇÃO:")

        for alerta in alertas:
            print()
            print(f"🛒 Produto: {alerta['produto']}")
            print(f"💰 Preço atual: ${alerta['preco_atual']}")
            print(f"📉 Menor preço histórico: ${alerta['menor_preco_historico']}")
            print(f"💵 Economia: ${alerta['economia']:.2f}")
            print(f"📊 Desconto real: {alerta['percentual']:.2f}%")
            print("-" * 40)


# Integração com o Telegram

def enviar_mensagem_telegram(mensagem):
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_TELEGRAM_CHAT_ID"

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    dados = {
        "chat_id": chat_id,
        "text": mensagem
    }

    resposta = requests.post(url, data=dados)

    if resposta.status_code == 200:
        print("✅ Mensagem enviada para o Telegram.")
    else:
        print("❌ Erro ao enviar mensagem.")
        print(resposta.text)

# Monta a mensagem que será enviada ao Telegram

def montar_mensagem_telegram(alertas):
    if not alertas:
        return "✅ Nenhuma nova promoção encontrada."

    mensagem = "🔥 ALERTAS DE PROMOÇÃO:\n\n"

    for alerta in alertas:
        mensagem += f"🛒 Produto: {alerta['produto']}\n"
        mensagem += f"💰 Preço atual: ${alerta['preco_atual']}\n"
        mensagem += f"📉 Menor preço histórico: ${alerta['menor_preco_historico']}\n"
        mensagem += f"💵 Economia: ${alerta['economia']:.2f}\n"
        mensagem += f"📊 Desconto real: {alerta['percentual']:.2f}%\n"
        mensagem += "-" * 40 + "\n"

    return mensagem


# Criação do objeto principal
finder = PromotionFinder()

# Entrada de filtros do usuário

finder.categoria_desejada = finder.escolher_categoria()
finder.preco_maximo = float(input("Digite o preço máximo: "))
finder.avaliacao_minima = float(input("Digite a avaliação mínima: "))
finder.desconto_minimo = float(input("Digite o desconto mínimo: "))
finder.deseja_comparar = input("Deseja comparar os preços atuais com o histórico? (s/n): ").lower() == "s"


# Programa principal
# Fluxo:
# Criar banco SQLite
# -> Buscar produtos
# -> Filtrar produtos
# -> Ordenar produtos
# -> Gerar promoções
# -> Gerar alertas
# -> Exibir alertas
# -> Salvar histórico SQLite
# -> Salvar CSV atual
# -> Montar mensagem para o Telegram
# -> Enviar mensagem para o Telegram

finder.criar_banco()

produtos = finder.buscar_produtos()

produtos_filtrados = finder.filtrar_produtos(produtos)
produtos_ordenados = finder.ordenar_produtos(produtos_filtrados)

finder.gerar_promocoes(produtos_ordenados)

alertas = finder.gerar_alertas(produtos_ordenados)
finder.exibir_alertas(alertas)

finder.salvar_historico_sqlite(produtos_ordenados)
finder.salvar_csv(produtos_ordenados)


print(f"CSV criado com sucesso! {len(produtos_ordenados)} produtos encontrados.")
print("Processo finalizado com sucesso.")

mensagem = montar_mensagem_telegram(alertas)

print("\n📨 Mensagem que será enviada:")
print(mensagem)

enviar_mensagem_telegram(mensagem)
