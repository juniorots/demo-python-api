from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

# Initialize app 
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullabe=False)
    email = db.Column(db.string(100), unique=True, nullabe=False)

    def json(sefl):
        return {'id': self.id, 'nome': self.nome, 'email': self.email}

db.create_all()


# simple test end-point
@app.route('/test', methods=['GET'])
def testGet():
    return make_response(jsonify({'message': 'routing...'}), 200)


#  POST
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()
        usuario = Usuario(nome=data['nome'], email=data['email'])
        db.session.add(usuario)
        db.session.commit()
        return make_response(jsonify({'message': 'usuario cadastrado'}), 201)
    except e:
        return make_response(jsonify({'message': 'falha na operacao com usuario'}), 500)


# GET
@app.route('/usuarios', methods=['GET'])
def listar_usuario():
    try:
        usuarios = Usuario.query.all()
        return make_response(jsonify([usuario.json() from usuario in usuarios]), 200)
    except e:
        return make_response(jsonfiy({'message': 'falha na listagem de usuarios'}), 500)


# GET DETAIL
@app.route('/usuarios/<int:id>', methods=['GET'])
def detalhar_usuario(id):
    try:
        usuario = Usuario.query.filter_by(id=id).first()
        if usuario:
            return make_response(jsonify({'usuario':usuario.json()}), 200)
        return make_response(jsonify({'message': 'usuario nao encontrado'}), 400)
    except e:
        return make_response(jsonfiy({'message': 'falha na leitura do usuario'}), 500)


# PUT
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    try:
        usuario = Usuario.query.filter_by(id=id).first()
        if usuario:
            data = request.get_json()
            usuario.nome = data['nome']
            usuario.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'usuario atualizado'}), 200)
        return make_response(jsonify({'message': 'usuario nao encontrado'}), 404)
    except e:
        return make_response(jsonify({'message': 'falha na atualizacao do usuario'}), 500)


# DELETE
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    try:
        usuario = Usuario.query.filter_by(id=id).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return make_response(jsonify({'message': 'usuario excluido com sucesso'}), 200)
        return make_response(jsonify({'message': 'usuario nao encontrado'}), 404)
    except e:
        return make_response(jsonify({'message': 'falha na exclusao do usuario'}), 500)

        

