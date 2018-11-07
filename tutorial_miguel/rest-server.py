from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)

tarefas = [
    {
        'id': 1,
        'title': u'Buy groceries',
    },
    {
        'id': 2,
        'title': u'Learn Python',
    }
]

campos_tarefas = {
    'title': fields.String,
}

class Tarefas(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('dic', type = str, required = True,
                                    help = 'Dicionario', 
                                    location = 'json')

        self.reqparse.add_argument('description', type = str, default = "", location = 'json')

        super(Tarefas, self).__init__()

    def get(self):
        return {'tarefas': [marshal(tarefa, campos_tarefas) for tarefa in tarefas]}

    def post(self):
        args = self.reqparse.parse_args()
        tarefa = {
            'id': tarefa[-1]['id'] + 1,
            'title': args['title']
        }
        tarefas.append(tarefa)
        return {'tarefas    ': marshal(tarefa, campos_tarefas)}, 201

class TarefasId(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')

        super(TarefasId, self).__init__()
    
    def get(self, id_tarefa):
        tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == id_tarefa]
        if len(tarefa) == 0:
            abort(404)
        return {'tarefa': marshal(tarefa[0], campos_tarefas)}

    def put(self, id_tarefa):
        tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == id_tarefa]
        if len(tarefa) == 0:
            abort(404)
        tarefa = tarefa[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                tarefa[k] = v
        return {'tarefa': marshal(tarefas, campos_tarefas)}

    def delete(self, id_tarefa):
        tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == id_tarefa]
        if len(tarefa) == 0:
            abort(404)
        tarefas.remove(tarefa[0])
        return {'result': True}

# class Healthcheck():
    # def healthcheck(self):
        # return 200

api.add_resource(Tarefas, '/Tarefa', endpoint = 'Tarefa')
api.add_resource(TarefasId, '/Tarefa/<int:id>', endpoint = 'TarefaId')
# api.add_resource(Healthcheck, '/healthcheck', endpoint = 'healthcheck')

if __name__ == '__main__':
    app.run(debug=True)
