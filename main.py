from flask import Flask, render_template, request, redirect, url_for
import uuid
import json

app = Flask(__name__)

def tasks_list():
    with open("db.json", "r") as arq:
        return json.loads(arq.read())

@app.route('/')
def home():
    lista = tasks_list()
    return render_template('home.html', tasks=lista)

@app.route('/tarefas/form', methods=['GET'])
def create_form():
    return render_template('form.html')

@app.route('/tarefas', methods=["POST"])
def create():
    body = request.form.to_dict()
    body["_id"] = str(uuid.uuid4())
    with open("db.json", "r+") as arq:
        lines = arq.read()
        lista = json.loads(lines)
        lista.append(body)

        arq.seek(0)
        arq.write(json.dumps(lista))
        arq.truncate()

    return redirect(url_for('home'))

@app.route('/tarefas/<string:task_id>/editar', methods=['GET'])
def edit_form(task_id):
    lista = tasks_list()
    task = next((t for t in lista if t['_id'] == task_id), None)
    if task:
        return render_template('edit.html', task=task)
    else:
        return "Tarefa não encontrada", 404

@app.route('/tarefas/<string:task_id>/atualizar', methods=['POST'])
def update(task_id):
    lista = tasks_list()
    task = next((t for t in lista if t['_id'] == task_id), None)
    if task:
        updated_task = request.form.to_dict()
        task.update(updated_task)
        with open("db.json", "w") as arq:
            arq.write(json.dumps(lista))
        return redirect(url_for('home'))
    else:
        return "Tarefa não encontrada", 404

@app.route('/tarefas/<string:task_id>/excluir', methods=['GET'])
def delete(task_id):
    lista = tasks_list()
    task = next((t for t in lista if t['_id'] == task_id), None)
    if task:
        lista.remove(task)
        with open("db.json", "w") as arq:
            arq.write(json.dumps(lista))
        return redirect(url_for('home'))
    else:
        return "Tarefa não encontrada", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


