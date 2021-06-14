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
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()[1:]])

# Checks if all parents are present before TXID
def check_parent(parents, history):
    flag = True
    if ';' in parents:
        x = parents.split(";") 
    else:
        x = [parents]
    
    for parent in x:
        if parent in history:
            flag = True 
        else:
            return False  
    return flag

# Returns all valid transactions 
def get_valid_tx(mempool):
    history = []
    fee_h = []
    weight_h = []
    for transaction in mempool:
        if transaction.parents == "":
            history.append(transaction.txid)
            fee_h.append(transaction.fee)
            weight_h.append(transaction.weight)
        elif check_parent(transaction.parents, history) == True:  
            history.append(transaction.txid)
            fee_h.append(transaction.fee)
            weight_h.append(transaction.weight)
        else:
            continue
    return history, fee_h, weight_h 

# Calculate Final Block
def calc(valid_tx, fees, weights):  
    
    MAX = 4000000
    current_sum = 0
    max_sum = 0

    current_weight = 0
    initial_position = 0 
    final_position = 0

    for i in range(len(fees)):
        current_sum += fees[i]
        
        if current_sum > max_sum and current_weight < MAX:
            if current_weight + weights[i] < MAX:
                current_weight += weights[i]
            
                max_sum = current_sum
                initial_position = i 
        final_position = i 

    return initial_position, final_position, max_sum, current_weight


if __name__ == '__main__':
    x = parse_mempool_csv()
    # calc(x)
    valid_transactions, fees, weights = get_valid_tx(x)
    print("Number of Valid Transaction :", len(valid_transactions))
    print("Fee length :", len(fees))
    print("Weights length :", len(weights))


    initial_position, final_position, cum_sum, cum_weight = calc(valid_transactions, fees, weights)
    
    print("\n\n BLOCK \n\n")
    print(valid_transactions[initial_position:final_position+1])
    print("Number of Valid Transaction :", len(valid_transactions))
    print("Number of TXID in BLOCK:", final_position - initial_position)
    print("Final Fees :",cum_sum)
    print("Final Weight :", cum_weight)

    final_file = open("block.txt", "w")
    final_file.writelines(valid_transactions[initial_position:final_position+1])

    final_file.close()