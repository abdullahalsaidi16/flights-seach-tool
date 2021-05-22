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
    df = pd.read_csv(argsdict["input_file_path"])
    flights = [Flight(x) for _, x in df.iterrows()]
    # build graph
    all_places = set()
    [(all_places.add(x.source), all_places.add(x.dest)) for x in flights]
    graph = Graph(all_places)
    graph.add_flights(flights)
    for place in all_places:
        print(f"Starting Location {place}..")
        passenger = Passenger(argsdict["bags_count"], place)
        graph.find_combinations(passenger, argsdict["show_cost"])
