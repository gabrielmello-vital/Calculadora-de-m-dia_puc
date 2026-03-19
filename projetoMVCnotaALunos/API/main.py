from flask import Flask, request, jsonify
from model.student_model import studentModel


app = Flask(__name__)

@app.route('/alunos', methods=['GET'])
def mostrar_alunos():
    model = studentModel() 
    alunos = model.get_all()
    return jsonify(alunos)

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    model = studentModel()
    media_calculada = model.saveAlunos(
        data['name'], data['matricula'], data['codigo'],
        data['n1'], data['n2'], data['n3'], data['n4']
    )
    
    return jsonify({
        "message": "Salvo com sucesso!",
        "media": media_calculada
    }), 201

@app.route('/alunos/<string:chave_composta>', methods=['DELETE'])
def deletar_aluno(chave_composta):
    model = studentModel()
    success = model.delete_aluno(chave_composta)
    
    if success:
        return jsonify({"message": f"Aluno {chave_composta} deletado!"}), 200
    else:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    
@app.route('/alunos/criterio/<string:codigo>', methods=['GET'])
def obter_criterio(codigo):
    model = studentModel()
    criterio_func = model.disciplinasCriterios.get(codigo.upper())
    if criterio_func:
        return jsonify({"criterio": criterio_func.__name__}) 
    return jsonify({"error": "Não encontrado"}), 404
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)