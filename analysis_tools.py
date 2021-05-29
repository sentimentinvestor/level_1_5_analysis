
# takes in a list of dictionary objects (the ticker documents) and a metric
# returns the average value of that metric across all tickers
def calculate_average(documents, metric):
    datapoints = [t.get(metric) for t in documents if t.get(metric)]
    return sum(datapoints) / len(datapoints)
