import hashlib
import json
from textwrap import dedent
from uuid import uuid4
from flask import flask
from flas import Flask, jsonify, request
from blockchain import Blockchain

class Blockchain(object):
    app = Flask(__name__)
    node_id = str(uuid4()).replace('-', '')
    blockchain = Blockchain()

    @app.route('/mine', methods=['GET'])
    def mine():
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        blockchain.new_transaction(
                sender='0'
                receiver=node_id,
                amount=1,
                )
        prev_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, prev_hash)
        response = {
                'message': "New Block foromed",
                'index': block['index'].
                'transactions': block['transactions'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash'],
        return jsonify(response), 200

    @app.route('/transaction/new', methods=['POST'])
    def new_transaction():
        values = request.get_json()

        required = ['sender', 'receiver', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400
        index = blockchain.new_transaction(values['sender'], values['receiver'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
                'chain': blockchain.chain,
                'length': len(blockchain.chain),
                }
                return jsonify(response), 200

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
