from urllib import response 
from flask import Flask, jsonify
from blockchain import Blockchain
import datetime as dt
import sys
import atexit

def OnExitApp(user):
    print(user, 'terminated server')

    # save chain
    blockchain.saveChain()

atexit.register(OnExitApp, user='Nathan')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    # # mine block
    
    # get inputs from previous block/ current end block on chain
    prevBlock = blockchain.getPrevBlock()
    prevProof = prevBlock['proof']
    
    # 
    proof = blockchain.proofOfWork(prevProof)
    prevHash = blockchain.hash(prevBlock)
    block = blockchain.createBlock(proof, prevHash)
    
    response ={
            'message'       : 'Hey you just mined a block! That is awesome, you are awesome!',
            'index'         : block['index'],
            'timestamp'     : block['timestamp'],
            'proof'         : block['proof'],
            'previous_hash' : block['previous_hash']
        }
    return jsonify(response), 200


#  Request Blockchain
@app.route('/getChain', methods=['GET'])
def getChain():
    response = {
            'message'   : 'Blocks in the current chain',
            'chain'     : blockchain.chain,
            'length'    : len(blockchain.chain),
            'timestamp' : str(dt.datetime.now()) 
        }
    return jsonify(response), 200


# Request server to check if chain is valid
@app.route('/checkValid', methods=['GET'])
def checkValid():
    response = {
        'isValid' : blockchain.isChainValid(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':

    pathToChain = './data/ledger.json'

    # load the blockchain with most recent saved chain
    # TODO: add some check that timestamp makes sense with last server shutdown
    blockchain  = Blockchain()
    blockchain.loadFromJson(pathToChain)

    # check if valid 
    if blockchain.isChainValid(blockchain.chain) is True:
        # Run the app
        app.run(host='0.0.0.0', port = 5000)
    else:
        print('ERROR: Chain is not valid.')
