from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM Livros').fetchall()
    conn.close()
    return render_template('index.html', livros=livros)

@app.route('/livros', methods=['GET'])
def livros():
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM Livros').fetchall()
    conn.close()
    return render_template('livros.html', livros=livros)



@app.route('/cadastro_livro', methods=['GET', 'POST'])
def cadastro_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        quantidade = request.form['quantidade']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO Livros (Titulo, Autor, AnoPublicacao, Genero, Quantidade) VALUES (?, ?, ?, ?, ?)',
                     (titulo, autor, ano, genero, quantidade))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('cadastro_livro.html')

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_cadastro = request.form['data_cadastro']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO Clientes (Nome, Email, Telefone, DataCadastro) VALUES (?, ?, ?, ?)',
                     (nome, email, telefone, data_cadastro))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('cadastro_cliente.html')

@app.route('/cadastro_funcionario', methods=['GET', 'POST'])
def cadastro_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        email = request.form['email']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO Funcionarios (Nome, Cargo, Email) VALUES (?, ?, ?)',
                     (nome, cargo, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('cadastro_funcionario.html')

@app.route('/emprestimo', methods=['GET', 'POST'])
def emprestimo():
    if request.method == 'POST':
        livro_id = request.form['livro_id']
        cliente_id = request.form['cliente_id']
        funcionario_id = request.form['funcionario_id']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO Emprestimos (LivroID, ClienteID, DataEmprestimo, FuncionarioID) VALUES (?, ?, DATE("now"), ?)',
                     (livro_id, cliente_id, funcionario_id))
        conn.execute('UPDATE Livros SET Quantidade = Quantidade - 1 WHERE LivroID = ?', (livro_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('emprestimo.html')

@app.route('/livros_emprestados')
def livros_emprestados():
    conn = get_db_connection()
    # Ajuste a consulta para incluir informações dos clientes e funcionários
    query = '''
    SELECT E.EmprestimoID, L.Titulo AS Titulo, C.Nome AS Cliente, F.Nome AS Funcionario, E.DataEmprestimo
    FROM Emprestimos E
    JOIN Livros L ON E.LivroID = L.LivroID
    JOIN Clientes C ON E.ClienteID = C.ClienteID
    JOIN Funcionarios F ON E.FuncionarioID = F.FuncionarioID
    '''
    
    emprestimos = conn.execute(query).fetchall()
    emprestimos_atualizados = []
    
    for emprestimo in emprestimos:
        data_emp = datetime.strptime(emprestimo['DataEmprestimo'], '%Y-%m-%d')
        # Calcular a data de devolução
        data_devolucao = data_emp + timedelta(days=10)
        # Adicionar ao resultado
        emprestimo_dict = dict(emprestimo)
        emprestimo_dict['DataDevolucao'] = data_devolucao.strftime('%Y-%m-%d')
        emprestimos_atualizados.append(emprestimo_dict)
    
    conn.close()
    return render_template('livros_emprestados.html', emprestimos=emprestimos_atualizados)

@app.route('/excluir_livro/<int:livro_id>', methods=['POST'])
def excluir_livro(livro_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Livros WHERE LivroID = ?', (livro_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('livros'))

@app.route('/excluir_cliente/<int:cliente_id>', methods=['POST'])
def excluir_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Clientes WHERE ClienteID = ?', (cliente_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

@app.route('/excluir_funcionario/<int:funcionario_id>', methods=['POST'])
def excluir_funcionario(funcionario_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Funcionarios WHERE FuncionarioID = ?', (funcionario_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('funcionarios'))


@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM Clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/funcionarios')
def funcionarios():
    conn = get_db_connection()
    funcionarios = conn.execute('SELECT * FROM Funcionarios').fetchall()
    conn.close()
    return render_template('funcionarios.html', funcionarios=funcionarios)


if __name__ == "__main__":
    app.run(debug=True)
