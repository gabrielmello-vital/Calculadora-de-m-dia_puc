from flask import Flask, request, jsonify
from model.student_model import studentModel
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/alunos', methods=['GET'])
def mostrar_alunos():
    """
    Retorna a lista de todos os alunos cadastrados.
    ---
    responses:
      200:
        description: Um dicionário com todos os alunos.
        schema:
          type: object
          example: {"123_MAT": {"nome": "Gabriel", "media": 8.5}}
    """
    model = studentModel() 
    alunos = model.get_all()
    return jsonify(alunos)

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    """
    Cadastra um novo aluno e calcula a média via Model.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Aluno
          required:
            - name
            - matricula
            - codigo
          properties:
            name:
              type: string
              example: "Gabriel Mello"
            matricula:
              type: string
              example: "1234567"
            codigo:
              type: string
              example: "INF1039"
            n1:
              type: number
              example: 8.0
            n2:
              type: number
              example: 7.5
            n3:
              type: number
              example: 0
            n4:
              type: number
              example: 0
    responses:
      201:
        description: Aluno cadastrado com sucesso e média retornada.
    """
    data = request.get_json()
    model = studentModel()
    media_calculada = model.saveAlunos(
        data['name'], 
        data['matricula'], 
        data['codigo'],
        data.get('n1', 0), 
        data.get('n2', 0), 
        data.get('n3', 0), 
        data.get('n4', 0)
    )
    
    return jsonify({
        "message": "Salvo com sucesso!",
        "media": media_calculada
    }), 201

@app.route('/alunos/<string:chave_composta>', methods=['DELETE'])
def deletar_aluno(chave_composta):
    """
    Remove um aluno do sistema usando a chave composta (matricula_disciplina).
    ---
    parameters:
      - name: chave_composta
        in: path
        type: string
        required: true
        description: "Exemplo: 2210456_INF1039"
    responses:
      200:
        description: Aluno removido com sucesso.
      404:
        description: Chave não encontrada.
    """
    model = studentModel()
    success = model.delete_aluno(chave_composta)
    
    if success:
        return jsonify({"message": f"Aluno {chave_composta} deletado!"}), 200
    else:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    
@app.route('/alunos/criterio/<string:codigo>', methods=['GET'])
def obter_criterio(codigo):
    """
    Retorna o nome da função de critério para uma disciplina.
    ---
    parameters:
      - name: codigo
        in: path
        type: string
        required: true
    responses:
      200:
        description: Nome da função de critério.
    """
    model = studentModel()
    criterio_func = model.disciplinasCriterios.get(codigo.upper())
    if criterio_func:
        return jsonify({"criterio": criterio_func.__name__}) 
    return jsonify({"error": "Não encontrado"}), 404
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)