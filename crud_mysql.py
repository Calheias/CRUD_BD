import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crudbd"
)

cursor = conn.cursor()

def criar_tabelas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS autor (
        matricula INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        nacionalidade VARCHAR(100),
        cpf INT,
        niver DATE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS editora (
        codEdit INT AUTO_INCREMENT PRIMARY KEY,
        cnpj INT(14),
        nome VARCHAR(100),
        cidade VARCHAR(100),
        estado VARCHAR(100)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livro (
        idlivro INT AUTO_INCREMENT PRIMARY KEY,
        isbn INT(13),
        nome VARCHAR(100),
        paginas INT,
        preco DECIMAL(10, 2),
        lancamento DATE,
        autor_matricula INT,
        editora_cod INT,
        FOREIGN KEY (autor_matricula) REFERENCES autor(matricula),
        FOREIGN KEY (editora_cod) REFERENCES editora(codEdit)
    )""")

    conn.commit()

def inserir_registro(tabela, campos, valores):
    colunas = ", ".join(campos)
    placeholders = ", ".join(["%s"] * len(campos))
    sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
    cursor.execute(sql, valores)
    conn.commit()
    print(f"Registro inserido em '{tabela}'.")

def listar_registros(tabela):
    if tabela == "livro":
        cursor.execute("""
        SELECT livro.idlivro, livro.nome, livro.paginas, livro.preco, livro.lancamento,
               autor.nome AS autor_nome, editora.nome AS editora_nome
        FROM livro
        JOIN autor ON livro.autor_matricula = autor.matricula
        JOIN editora ON livro.editora_cod = editora.codEdit
        """)
    else:
        cursor.execute(f"SELECT * FROM {tabela}")

    resultados = cursor.fetchall()
    for row in resultados:
        print(row)

def atualizar_registro(tabela, campos, valores, id_registro):
    id_campo = "idlivro" if tabela == "livro" else ("matricula" if tabela == "autor" else "codEdit")
    set_clause = ", ".join([f"{campo} = %s" for campo in campos])
    sql = f"UPDATE {tabela} SET {set_clause} WHERE {id_campo} = %s"
    cursor.execute(sql, valores + (id_registro,))
    conn.commit()
    print(f"Registro com ID {id_registro} atualizado na tabela '{tabela}'.")

def deletar_registro(tabela, id_registro):
    id_campo = "idlivro" if tabela == "livro" else ("matricula" if tabela == "autor" else "codEdit")
    sql = f"DELETE FROM {tabela} WHERE {id_campo} = %s"
    cursor.execute(sql, (id_registro,))
    conn.commit()
    print(f"Registro com ID {id_registro} deletado de '{tabela}'.")

def menu_entidade(nome_tabela, campos):
    while True:
        print(f"\n {nome_tabela}")
        print("1. Inserir")
        print("2. Listar")
        print("3. Atualizar")
        print("4. Deletar")
        print("5. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valores = tuple(input(f"{campo.capitalize()}: ") for campo in campos)
            inserir_registro(nome_tabela, campos, valores)
        elif opcao == "2":
            listar_registros(nome_tabela)
        elif opcao == "3":
            id_registro = int(input("ID do registro a atualizar: "))
            novos_valores = tuple(input(f"Novo {campo}: ") for campo in campos)
            atualizar_registro(nome_tabela, campos, novos_valores, id_registro)
        elif opcao == "4":
            id_registro = int(input("ID do registro a deletar: "))
            deletar_registro(nome_tabela, id_registro)
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Livro")
        print("2. Autor")
        print("3. Editora")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            menu_entidade("livro", ["isbn", "nome", "paginas", "preco", "lancamento", "autor_matricula", "editora_cod"])
        elif escolha == "2":
            menu_entidade("autor", ["nome", "nacionalidade", "cpf", "niver"])
        elif escolha == "3":
            menu_entidade("editora", ["cnpj", "nome", "cidade", "estado"])
        elif escolha == "4":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    criar_tabelas()
    menu_principal()

cursor.close()
conn.close()


# # Funções de CRUD para "usuarios"
# def criar_usuario(nome, email):
#     sql = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
#     valores = (nome, email)
#     cursor.execute(sql, valores)
#     conn.commit()
#     print(f"Usuário '{nome}' criado com sucesso.")

# def listar_usuarios():
#     cursor.execute("SELECT * FROM usuarios")
#     resultados = cursor.fetchall()
#     for usuario in resultados:
#         print(usuario)

# def atualizar_usuario(id_usuario, novo_nome, novo_email):
#     sql = "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s"
#     valores = (novo_nome, novo_email, id_usuario)
#     cursor.execute(sql, valores)
#     conn.commit()
#     print(f"Usuário com ID {id_usuario} atualizado.")

# def deletar_usuario(id_usuario):
#     sql = "DELETE FROM usuarios WHERE id = %s"
#     valores = (id_usuario,)
#     cursor.execute(sql, valores)
#     conn.commit()
#     print(f"Usuário com ID {id_usuario} deletado.")

# # Menu
# def menu():
#     while True:
#         print("\n1. Criar usuário\n2. Listar usuários\n3. Atualizar usuário\n4. Deletar usuário\n5. Sair")
#         opcao = input("Escolha uma opção: ")

#         if opcao == "1":
#             nome = input("Nome: ")
#             email = input("Email: ")
#             criar_usuario(nome, email)
#         elif opcao == "2":
#             listar_usuarios()
#         elif opcao == "3":
#             id_usuario = int(input("ID do usuário: "))
#             novo_nome = input("Novo nome: ")
#             novo_email = input("Novo email: ")
#             atualizar_usuario(id_usuario, novo_nome, novo_email)
#         elif opcao == "4":
#             id_usuario = int(input("ID do usuário: "))
#             deletar_usuario(id_usuario)
#         elif opcao == "5":
#             break
#         else:
#             print("Opção inválida.")

# # Execução principal
# if __name__ == "__main__":
#     criar_tabelas()
#     menu()

# cursor.close()
# conn.close()
