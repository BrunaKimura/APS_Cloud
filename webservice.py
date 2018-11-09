from flask import Flask, request
import tarefas
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world!"


@app.route('/Tarefas', methods=['GET', 'POST'])
def tarefa():
    if request.method == 'GET':
        return json.dumps(tarefas.dic_tarefas, default=lambda x : x.__dict__)
    print(request)
    dic = json.loads(request.data)
    tarefas.cont+=1
    tarefa = tarefas.Tarefas(dic["atri1"], dic["atri2"])
    tarefas.dic_tarefas[tarefas.cont] = tarefa
    return "200"


@app.route('/Tarefas/<int:id_tarefa>', methods=['GET', 'PUT', 'DELETE'])
def tarefaId(id_tarefa):
    try:
        if request.method == 'GET':
            return json.dumps(tarefas.dic_tarefas[id_tarefa], default=lambda x : x.__dict__)

        elif request.method == 'PUT':
            dic = json.loads(request.data)
            tarefa = tarefas.Tarefas(dic["atri1"], dic["atri2"])
            tarefas.dic_tarefas[id_tarefa] = tarefa
            return "200"

        else:
            del tarefas.dic_tarefas[id_tarefa]
            return "200"
    except:
        print("não existe id")
        return "Não exite id"


@app.route('/healthcheck')
def codigo200():
    return "200"

if __name__ == '__main__':
    app.run(debug=True)