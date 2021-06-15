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
        current_weight += weights[i]
        if current_weight <=MAX:
            current_sum += fees[i]
            final_position += 1 
        else:
            current_weight -= weights[initial_position]
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

    print(f"Final Position: {final_position},  Initial Position: {initial_position}")

    final_file = open("block.txt", "w")
    final_file.writelines('\n'.join(valid_transactions[initial_position:final_position+1])+ '\n')

    final_file.close()

    