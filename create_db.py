import sqlite3

def create_db():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        print("Criando tabelas...")
        
        # Tabelas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Livros (
            LivroID INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Autor TEXT,
            AnoPublicacao INTEGER,
            Genero TEXT,
            Quantidade INTEGER NOT NULL CHECK (Quantidade >= 0)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            ClienteID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Email TEXT UNIQUE,
            Telefone TEXT,
            DataCadastro DATE NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Emprestimos (
            EmprestimoID INTEGER PRIMARY KEY AUTOINCREMENT,
            LivroID INTEGER,
            ClienteID INTEGER,
            DataEmprestimo DATE NOT NULL,
            DataDevolucao DATE,
            FuncionarioID INTEGER,
            FOREIGN KEY (LivroID) REFERENCES Livros(LivroID),
            FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),
            FOREIGN KEY (FuncionarioID) REFERENCES Funcionarios(FuncionarioID)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Funcionarios (
            FuncionarioID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Cargo TEXT,
            Email TEXT UNIQUE
        )
        ''')
        
        conn.commit()
        print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_db()
