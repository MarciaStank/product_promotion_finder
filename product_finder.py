import requests
import csv

# API de produtos utilizada para estudos
url = f"https://dummyjson.com/products"

# --------- Comentarios para estudos ------
# Poderia colocar a url direto na categoria Beauty tambem dai não precisaria do if e nem criar a variável categoria_desejada, mas quis deixar o código mais flexível para caso queira mudar a categoria depois sem precisar mexer na url.
# url = "https://dummyjson.com/products/category/beauty"
# --------- -------------------------------

# 1. Buscar produtos na API
# Fluxo:
# Requisição HTTP -> JSON -> Lista de produtos

def buscar_produtos():

    resposta = requests.get(url)
    dados = resposta.json()
    produtos = dados["products"]
    #categoria_desejada = "beauty"

    return produtos


# 2. Filtrar produtos
# Regras:
# - Categoria desejada
# - Preço máximo
# - Avaliação mínima
# - Desconto mínimo

def filtrar_produtos(produtos, categoria_desejada, preco_maximo, avaliacao_minima, desconto_minimo):
            
    produtos_filtrados = []

    for produto in produtos:
        preco = produto.get("price", 0)
        categoria = produto.get("category", "")
        avaliacao = produto.get("rating")
        desconto = produto.get("discountPercentage", 0)

        # Para verificar pq um produto entrou ou não no filtro
        # print(produto["title"], preco, avaliacao, categoria, desconto)

        if (
            categoria == categoria_desejada
            and preco <= preco_maximo
            and avaliacao >= avaliacao_minima
            and desconto >= desconto_minimo
                    ):
            produtos_filtrados.append(produto)

    return produtos_filtrados


# 3. Ordenar produtos
# Critério:
# Menor preço -> Maior preço

def ordenar_produtos(produtos):
    produtos_ordenados = sorted(produtos, key=lambda x: x["price"])
    return produtos_ordenados

# 4. Gerar promoções
# Fluxo:
# Produto -> Card formatado -> Terminal

def gerar_promocoes(produtos):

    for produto in produtos:
        nome = produto.get("title", "")
        preco = produto.get("price", 0)
        avaliacao = produto.get("rating", 0)
        desconto = produto.get("discountPercentage", 0)
        categoria = produto.get("category", "")

        print()
        print(f"🛒 Produto: {nome}")
        print(f"💰 Preço: ${preco}")
        print(f"⭐ Avaliação: {avaliacao}")
        print(f"🏷️  Categoria: {categoria}")
        print(f"🔥 Desconto: {desconto}%")
        print("-" * 40)
        print()


# 5. Escolher categoria
# Fluxo:
# Número do menu -> Categoria

def escolher_categoria():
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
    

# 6. Exportar produtos para CSV
# Saída:
# Lista filtrada e ordenada

def salvar_csv(produtos):
    with open("product_promotion_finder/output/product_promotions.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["Produto", "Preço", "Desconto", "Avaliação", "Estoque", "Marca", "Categoria", "Imagem"])
  
        
        for produto in produtos:
            nome = produto.get("title", "")
            preco = produto.get("price", 0)
            desconto = produto.get("discountPercentage", 0)
            avaliacao = produto.get("rating", 0)
            estoque = produto.get("stock", 0)
            marca = produto.get("brand", "Sem marca")
            imagem = produto.get("thumbnail", "")
            categoria = produto.get("category", "")

            escritor.writerow([nome, preco, desconto, avaliacao, estoque, marca, categoria, imagem])



# 7. Parâmetros do filtro

categoria_desejada = escolher_categoria()
preco_maximo = float(input("Digite o preço máximo: "))
avaliacao_minima = float(input("Digite a avaliação mínima: "))
desconto_minimo = float(input("Digite o desconto mínimo: "))


# 8. Programa principal
# Fluxo:
# Buscar -> Filtrar -> Ordenar -> Gerar promoções -> Salvar CSV

produtos = buscar_produtos()
produtos_filtrados = filtrar_produtos(produtos, categoria_desejada, preco_maximo, avaliacao_minima, desconto_minimo)
produtos_ordenados = ordenar_produtos(produtos_filtrados)
gerar_promocoes(produtos_ordenados)

salvar_csv(produtos_ordenados)
print(f"CSV criado com sucesso! {len(produtos_ordenados)} produtos encontrados.")

