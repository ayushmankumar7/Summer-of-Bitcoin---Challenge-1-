class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.trans = {}
        self.txid = txid      
        self.fee = int(fee)
        # TODO: add code to parse weight and parents fields
        self.weight = int(weight)                                                       
        self.parents = parents          

def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()[1:]])    # Index from 1 to avoid Including Index row

# Checks if all parents are present before TXID
def check_parent(parents, history):
    flag = True
    if ';' in parents:                                                                   # Check for Multiple Parents
        x = parents.split(";")                                                                      
    else:
        x = [parents]                                                                    # For Tx having only one Parent
    
    for parent in x:
        if parent in history:
            flag = True 
        else:
            return False  
    return flag

# Returns all valid transactions 
def get_valid_tx(mempool):
    history = []                                                                         # Stores all Valid TX Ids 
    fee_h = []                                                                           # Stores all corrosponding fees for Valid Tx
    weight_h = []                                                                        # Stores all corrosponfing weights for Valid Tx
    for transaction in mempool:
        if transaction.parents == "":                                                    # Check Confired Tx
            history.append(transaction.txid)
            fee_h.append(transaction.fee)
            weight_h.append(transaction.weight)
        elif check_parent(transaction.parents, history) == True:                         # Checks for Non Valid Tx
            history.append(transaction.txid)
            fee_h.append(transaction.fee)
            weight_h.append(transaction.weight)
        
    return history, fee_h, weight_h                                                      # Returns all Valid Tx and corrosponding weights and fees

# Calculate Final Block
def calc(valid_tx, fees, weights):  
    
    MAX = 4000000                                                                         # Maximum Cummulative Block Weight
    current_sum = 0                                                                       # Calculate Fees

    current_weight = 0                                                                    # Calculate Initial Weight
    initial_position = 0                                                                  # Starting Position of Contigious Sub Array
    final_position = 0                                                                    # Ending Position of Contigious Sub Array

    for i in range(len(fees)):
        current_weight += weights[i]
        if current_weight <=MAX:                                                          # MAX Block weight checking
            current_sum += fees[i]
            final_position += 1 
        else:
            current_weight -= weights[initial_position]                                   # Balance Cummulative Weight
            initial_position += 1                                                         
            final_position += 1
            if (initial_position is not final_position):
                current_sum -= fees[initial_position]
                current_sum += fees[final_position]
            else:
                current_sum = fees[final_position]

    return initial_position, final_position, current_sum, current_weight                    


if __name__ == '__main__':
    x = parse_mempool_csv()
    valid_transactions, fees, weights = get_valid_tx(x)                                                      # Get all Valid Transactions
    
    print("Number of Valid Transaction :", len(valid_transactions))
    print("Fee length :", len(fees))
    print("Weights length :", len(weights))

    initial_position, final_position, cum_sum, cum_weight = calc(valid_transactions, fees, weights)          # Calculate the Maximum Fee and corrosponding Subarray
    
    print("\n\n BLOCK \n\n")
    # print(valid_transactions[initial_position:final_position+1])
    print("Number of Valid Transaction :", len(valid_transactions))
    print("Number of TXID in BLOCK:", final_position - initial_position)
    print("Final Fees :",cum_sum)
    print("Final Weight :", cum_weight)

    print(f"Final Position: {final_position},  Initial Position: {initial_position}")

    final_file = open("block.txt", "w")
    final_file.writelines('\n'.join(valid_transactions[initial_position:final_position+1])+ '\n')               # Stores Tx Block into block.txt

    final_file.close()

    