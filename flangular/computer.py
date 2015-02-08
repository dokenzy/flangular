# -*- coding: utf-8 -*-

import json

from flask import Response, make_response
from flask.ext.restful import reqparse, abort, Api

from flangular import app, db, api
from . model import Resource

parser = reqparse.RequestParser()
parser.add_argument('processor', type=str)
parser.add_argument('ram', type=str)
parser.add_argument('power', type=str)

class Computer(db.Document):
    processor = db.StringField()
    ram = db.StringField()
    power = db.StringField()

    def __str__(self):
        return '<Computer> processor: {}, ram: {}, power: {}'.format(self.processor, self.ram, self.power)

class ComputerItem(Resource):
    def get(self, id):
        com = Computer.objects(id=id).first()
        data = json.loads(com.to_json())
        return Response(json.dumps(data),  mimetype='application/json')

    def put(self, id):
        args = parser.parse_args()
        com = Computer.objects(id=id).first()
        com.update(
            #upsert=True,
            set__processor=args['processor'],
            set__ram=args['ram'],
            set__power=args['power'],
        )
        com.reload()
        data = json.loads(com.to_json())
        return Response(json.dumps(data),  mimetype='application/json')

    def delete(self, id):
        com = Computer.objects(id=id).first()
        com.delete()
        resp = make_response(('', 204))
        return resp

class ComputerList(Resource):
    def get(self):
        data = dict(
            objects=[],
            count=0
        )
        computers = Computer.objects.all()
        for com in computers:
            data['objects'].append(json.loads(com.to_json()))
        data['count'] = len(data['objects'])
        return Response(json.dumps(data),  mimetype='application/json')

    def post(self):
        args = parser.parse_args()
        com = Computer(
            processor=args['processor'],
            ram=args['ram'],
            power=args['power'],
        ).save()
        data = Computer.objects.order_by('-id').first().to_json()
        return Response(json.dumps(data),  mimetype='application/json')


api.add_resource(ComputerItem, '/api/computer/<string:id>')
api.add_resource(ComputerList, '/api/computer')
