from flask import Flask, jsonify, request
from uuid import uuid4

# Create a Flask web application
app = Flask(__name__)

# Create a unique node ID
node_id = str(uuid4()).replace('-', '')
from blockchain import Blockchain
# Import the Blockchain class from the blockchain module

# Create a Blockchain instance
blockchain = Blockchain()

# Define a route for mining a new block
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

# Create a new transaction for rewarding the miner (sender='0' represents the system)
    blockchain.new_transaction(
        sender='0',
        receiver=node_id,
        amount=1,
    )

    # Calculate the previous hash for the new block
    previous_hash = blockchain.hash(last_block)
    # Create a new block and add it to the blockchain
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block formed",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    # Return the response as JSON with an HTTP status code 200 (OK)
    return jsonify(response), 200

# Define a route for creating a new transaction
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # Get the transaction data from the request
    values = request.get_json()

   # Check if the required fields (sender, receiver, amount) are present
    required = ['sender', 'receiver', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['receiver'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    # Get the current state of the blockchain and its length
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# Start the Flask app on host '0.0.0.0' (accessible from any IP) and port 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

