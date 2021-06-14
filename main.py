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


def get_valid_tx(mempool):
    history = []
    corr_fees = []
    t_fee = 0 
    t_weight = 0 
    MAX = 4000000
    for transaction in mempool:
        if transaction.parents == "":
            history.append(transaction)
        elif check_parent(transaction.parents, history):  
            history.append(transaction)
        else:
            continue
    return history 


def calc(x):
    history = []
    t_fee = 0
    t_weight = 0
    MAX = 4000000
    for i in x:
        if t_weight < MAX:       
            if i.parents == "":
                
                if (t_weight + i.weight) < MAX:
                    t_weight += i.weight
                    t_fee += i.fee
                else:
                    break   
                history.append(i.txid)
            elif i.parents in history:
                 
                if (t_weight + i.weight) < MAX: 
                    t_weight += i.weight
                    t_fee += i.fee
                else:
                    break  
                history.append(i.txid)
            else:
                continue            
        else:
            break 
        print(f"TXID: {i.txid}, total_fee: {t_fee}, total_weight: {t_weight}")
    print(len(history))


    





if __name__ == '__main__':
    x = parse_mempool_csv()
    # calc(x)
    valid_transactions = get_valid_tx(x)
    print("Number of Valid Transaction :", len(valid_transactions))
    # with open("mempool.csv") as f:
        # print([f.readlines()[0]])