import csv, math, random

def loadCsv(filename):
    data = list(csv.reader(open(filename)))
    try: float(data[0][0])
    except: data.pop(0) # Remove header if present
    return [[float(x) for x in row] for row in data]

def splitData(data, ratio):
    random.seed(1)
    shuffled = list(data)
    random.shuffle(shuffled)
    split_idx = int(len(data) * ratio)
    return shuffled[:split_idx], shuffled[split_idx:]

def separate(data):
    d = {}
    for row in data:
        d.setdefault(row[-1], []).append(row)
    return d

def mean(x): return sum(x)/len(x)

def stdev(x):
    avg = mean(x)
    variance = sum((i-avg)**2 for i in x) / (len(x)-1)
    return math.sqrt(variance)

def summarize(data):
    # zip(*data) transposes rows to columns. [:-1] ignores class label
    return [(mean(col), stdev(col)) for col in zip(*data)][:-1]

def summarizeByClass(data):
    return {c: summarize(rows) for c, rows in separate(data).items()}

def prob(x, m, s):
    if s == 0: return 0
    exponent = math.exp(-(x-m)**2 / (2*s**2))
    return (1 / (math.sqrt(2*math.pi) * s)) * exponent

def predict(summs, row):
    probs = {}
    for c, stats in summs.items():
        probs[c] = 1
        for i, (m, s) in enumerate(stats):
            probs[c] *= prob(row[i], m, s)
    return max(probs, key=probs.get)

def accuracy(test, preds):
    correct = sum(1 for i in range(len(test)) if test[i][-1] == preds[i])
    return correct / len(test) * 100

def main():
    filename = 'diabetes.csv'
    try:
        data = loadCsv(filename)
        train, test = splitData(data, 0.67)
        print(f"Split {len(data)} rows into train={len(train)} and test={len(test)}")
        
        summaries = summarizeByClass(train)
        preds = [predict(summaries, row) for row in test]
        
        print(f"Accuracy: {accuracy(test, preds):.2f}%")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")

if __name__ == "__main__":
    main()