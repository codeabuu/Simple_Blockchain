import hashlib
import time
import json
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nowtransaction = []
        self.new_block(prev_hash=1, proof=100)
    def new_block(self):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.nowtransaction,
            'proof': proof,
            'prev_hash': prev_hash or self.hash(self.chain[-1])
        }
        self.nowtransaction = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, receiver, amount):
        self.nowtransaction.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def hash(self, block):
        block_str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    def valid_proof(self, last_proof, proof):
        guess = '{}{}'.format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

