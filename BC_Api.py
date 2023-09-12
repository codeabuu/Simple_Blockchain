import hashlib
import json
from textwrap import dedent
from uuid import uuid4
from flask import flask

class Blockchain(object):
    app = Flask(__name__)
    node_id = str(uuid4()).replace('-', '')
    blockchain = Blockchain()

    def mine
