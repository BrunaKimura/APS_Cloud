from flask import Flask, request
import requests
import os
# import boto3

# client = boto3.client('ec2')

app = Flask(__name__)

# instance_iterator = client.describe_instances(
#     Filters=[
#         {
#             'Name': 'tag:Owner',
#             'Values': [
#                 'Banco',
#             ],
#         },
#         {
#             'Name': 'instance-state-name',
#                 'Values':[
#                     'running',
#                     'pending'
#                 ]
#         },
#     ]
# )


# instacias = instance_iterator['Reservations']
# if len(instacias) !=0:
#     for i in instacias:
#         for e in i['Instances']:
#             ip_publico = str(e['PublicIpAddress'])

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):

    ip_db = os.environ['DB_HOST']

    caminho = "http://" + ip_db + ":5000/"

    print(caminho)

    if request.method == 'GET':
        r = requests.get(caminho + path)
        return r.text

    elif request.method == 'POST':
        print(request.json)
        r = requests.post(caminho + path, json=request.json)
        return r.text

    elif request.method == 'PUT':
        r = requests.put(caminho + path, json=request.json)
        return r.text

    elif request.method == 'DELETE':
        r = requests.delete(caminho + path)
        return r.text

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')