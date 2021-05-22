"""
 command lint tool for searhching for flights
 author: abdullah alsaidi
"""
import argparse
import pandas as pd
#
from utils import Flight, Passenger, Graph


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file-path", default="./input.csv")
    parser.add_argument("-nb", "--bags-count", type=int, default=0)
    parser.add_argument("-sc", "--show-cost", type=bool, default=False)

    args = parser.parse_args()
    argsdict = vars(args)
    # Validate input
    assert  0 <= argsdict["bags_count"] <= 2, "The value of bags count should be between 0 and 2" 
    assert argsdict["input_file_path"].endswith('.csv'), "the path provided isn't for CSV file"
    try:
        df = pd.read_csv(argsdict["input_file_path"])
        
    except OSError as e:
        print(e)
        print("Using the input.csv")
        argsdict["input_file_path"] = "./input.csv"
        df = pd.read_csv(argsdict["input_file_path"])

    # Creating flights instances    
    flights = [Flight(x) for _, x in df.iterrows()]
    # building graph
    all_places = set()
    [(all_places.add(x.source), all_places.add(x.dest)) for x in flights]
    graph = Graph(all_places)
    graph.add_flights(flights)
    for place in all_places:
        print(f"Starting Location {place}..")
        passenger = Passenger(argsdict["bags_count"], place)
        graph.find_combinations(passenger, argsdict["show_cost"])
