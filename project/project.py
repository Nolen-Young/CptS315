import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

def main():
    baskets = []
    infile = open("StudentsPerformance.csv", "r")
    infile.readline()
    for line in infile:
        line = line.strip('\n')
        basket = line.split(",")
        n1 = int(basket.pop())
        n2 = int(basket.pop())
        n3 = int(basket.pop())
        avg = (n1+n2+n3)/3
        if avg >= 70:
            basket.append("Pass")
        else:
            basket.append("Fail")
        baskets.append(basket)
        
    te = TransactionEncoder()
    te_ary = te.fit(baskets).transform(baskets)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequentItemsets = apriori(df, min_support=0.15, use_colnames=True)
    frequentItemsets['length'] = frequentItemsets['itemsets'].apply(lambda x: len(x))
    frequentItemsets = frequentItemsets.sort_values(by='support', ascending=False)
    frequentItemsets.to_csv("results.csv", encoding='utf-8', index=False)
  
if __name__ == "__main__":
	main()  