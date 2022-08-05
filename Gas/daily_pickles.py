import Gas.gas as gas
import pickle
#import matplotlib.pyplot as plt

    
def daily_pickle_gas():
    with open("pickles/gas_georgia.p", "rb" ) as f:
    	gas_georgia = pickle.load(f)

    reg, mid, prem, die = gas.get_gas('GA')
    temp = []
    temp.append(reg)
    temp.append(mid)
    temp.append(prem)
    temp.append(die)
    gas_georgia.append(temp)
    with open("pickles/gas_georgia.p", "wb" ) as f:
    	pickle.dump(gas_georgia, f)
        
if __name__ == '__main__':
    daily_pickle_gas()