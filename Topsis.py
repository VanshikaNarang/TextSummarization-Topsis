import sys
import pandas as pd
import numpy as np
import math as m

def topsis(input_file, weights, impacts, result_file):
    try:
        mydata = pd.read_csv(input_file)
        new_data = mydata.copy()
        for col in mydata.columns[1:]:
            try:
                mydata[col] = pd.to_numeric(mydata[col])
            except ValueError:
                print(f"Error: Non-numeric values found in column '{col}'.")
        if len(mydata.columns) < 3:
            print("Error: Input file must contain three or more columns.")
            return
        for col in mydata.columns[1:]:
            if not pd.to_numeric(mydata[col]).notna().all():
                print(f"Error: Non-numeric values found in column '{col}'.")
                return

        weights = [float(w) for w in weights.split(',')]
        impacts = [i.strip().lower() for i in impacts.split(',')]

        if len(weights) != len(impacts) or len(weights) != len(mydata.columns) - 1:
            print("Error: Number of weights, impacts, and columns must be the same.")
            return

        if not all(impact in ['+', '-'] for impact in impacts):
            print("Error: Impacts must be either +ve or -ve.")
            return
        
        for col in mydata.columns:
            try:
                mydata[col] = pd.to_numeric(mydata[col])
            except ValueError:
                print(f"Error: Non-numeric values found in column '{col}'.")
        data = mydata.iloc[:, 1:]
        
        normalized_data = data.copy()
        normalized_data = data.iloc[:, 1:].apply(lambda val: val / np.sqrt(np.sum(val**2)))

        weighted_normalized_data = normalized_data.copy()
        for i in range(1,len(weights)):
            weighted_normalized_data[data.columns[i]] *= weights[i-1]

        ideal_best=[]
        ideal_worst=[]
        for i in range(0, len(data.columns)):
            if(impacts[i]=='+'):
                ideal_best = pd.to_numeric(weighted_normalized_data.max())
                ideal_worst = pd.to_numeric(weighted_normalized_data.min())
            else:
                ideal_worst = pd.to_numeric(weighted_normalized_data.max())
                ideal_best = pd.to_numeric(weighted_normalized_data.min())

        separation_best = np.sqrt(np.sum((weighted_normalized_data - ideal_best.values) ** 2, axis=1))
        separation_worst = np.sqrt(np.sum((weighted_normalized_data - ideal_worst.values) ** 2, axis=1))

        topsis_score = separation_worst / (separation_worst + separation_best)
        
        rank = pd.Series(topsis_score).rank(ascending=False)

        result_data = new_data.copy()
        result_data['Topsis Score'] = topsis_score
        result_data['Rank'] = rank
        result_data.to_csv(result_file, index=False)
        print(f"Result saved to {result_file}")

    except FileNotFoundError:
        print("Error: File not found.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Incorrect Usage")
        print("Usage: python topsis.py <inputFileName> <Weights> <Impacts> <resultFileName>")
    else:
        topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
