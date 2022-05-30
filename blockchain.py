# Blockchain Class

import datetime as dt
import hashlib as hl
import json
import os

# Build blockchain
class Blockchain:
    
    def __init__(self, chain = []):
        self.chain = chain # list containing blocks. Is it important for the genesis block to start with prevHash=0?
        if len(chain) <= 0:
            # add genesis block if chain isnt given 
            self.createBlock(proof = 1, prevHash = '0')
    
    def createBlock(self, proof, prevHash):
        block = {
                    'index'         : len(self.chain)+1,
                    'timestamp'     : str(dt.datetime.now()),
                    'proof'         : proof, #same thing as current hash?
                    'previous_hash' : prevHash
                 } # make a block
        self.chain.append(block)
        return block
    
    def getPrevBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, prevProof):
        # Miners will call this when they want to put a block on the chain. 
        # They need to find the give miners a method they can run to find a blocks "proof" miners need to find. This is hard to find but easy to 
        # verify
            
        newProof = 1
        checkProof = False
        while checkProof is False:
            # demand four or more leading zeros for SHA256
            strToHash = str(newProof**2 - prevProof**2).encode()
            hashOperation = hl.sha256(strToHash).hexdigest()
            
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        return newProof # any guarentee that the while loop finishes? Prob not 
    
    def hash(self, block):
        # hash a block of blockchain
        encodedBlock = json.dumps(block, sort_keys=True).encode() # change format of block for SHA
        return hl.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        # each block is correct 
        
        prevBlock = chain[0]
        blockIndex =  1
        while blockIndex < len(chain):
            curBlock = chain[blockIndex]
            
            # check that sequence of hashs match i.e. previous hash of current
            # block equals the hash of the previous block
            if curBlock['previous_hash'] != self.hash(prevBlock):
                return False
            
            # check that hashes meet threshold 
            prevProof = prevBlock['proof']
            curProof = curBlock['proof']
            strToHash = str(curProof**2 - prevProof**2).encode()
            if hl.sha256(strToHash).hexdigest()[:4] != '0000':
                return False
            
            # update for next pass through the loop
            prevBlock = curBlock
            blockIndex += 1
        
        return True

    def toJson(self):
        # returns the object as a JSON
        bChainJson = {
            'timestamp': dt.datetime.now(),
            'chain': json.dumps(self.chain)
        }
        
        return bChainJson
    
    def saveChain(self):
        # saves chain to data folder 
        with open('./data/ledger.json', 'w') as f:
            json.dump(self.chain, f)


    def loadFromJson(self, pathToChain):
        # loads chain 

        try:
            
            with open(pathToChain, 'r') as jsonHandle:
                loadedChain = json.loads(jsonHandle.read())
                

            # check if fields are correct 
            chainLen = len(loadedChain)
            if chainLen > 0:
                print(f'Loaded chain with {chainLen} blocks')
                self.chain = loadedChain
            else:
                raise Exception('Loaded chain is empty!')
            
        except:
            print('Cannot find JSON.')
        








