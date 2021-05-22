# Flight Search tool

## Description
this command line script searches for all possible trips a passenger could make. from a preset flights data
with the following conditions:

-  having 1 to 4 hours for each
transfer between flights
- passengers cannot travel through the same cities on the same trip
- satisfies the number of bags allowed in each flight

## Input Data:
there is a default data provide but you can add new data as described in the **Usage** section

the schema of the data should be as the following:

- source, destination are the code of airport the flight is departing from and arriving to
- departure, arrival are times of departure and arrival
- price is the price of flight per person (without baggage)
- bags_allowed the number of bags passenger is allowed to take with them
- bag_price additional price per each bag passenger would like to take with them
- flight_number is the unique identifier of each flight


### Example Output:
the passenger with 0 bags can make the following trips:
```bash
Starting Location USM..
USM -> HKT | with total cost: 35
Starting Location DPS..
DPS -> HKT | with total cost: 160
DPS -> BWN | with total cost: 93
DPS -> BWN -> DPS | with total cost: 211
Starting Location HKT..
HKT -> USM | with total cost: 31
Starting Location BWN..
BWN -> DPS | with total cost: 85
```


## Setup
in the command line enter the repo directory
### install requirements with Pipenv
```
pipenv install
pipenv shell
```
### install requirements with requirements file
`Note:` you must be having python 3 installed and configured

```bash
pip install -r requirements.txt
```

## Usage
### command line args

| Name | Type |  Description | Default | Validation |
| --- | --- |  --- | --- |  --- |
| input-file-path | String | the path of the flights data file | ./input.csv | should be a csv file path |
| bag-count | Int | Number of bags the passenger have | 0 | gte than zero and lte than 2 |
| show-cost | Bool | Flag when is true show the mininal cost for each flight | False | |
|

### Search with new data
you can provide a csv file containing the flights data like the following example:
```csv
source,destination,departure,arrival,flight_number,price,bags_allowed,bag_price
USM,HKT,2017-02-11T06:25:00,2017-02-11T07:25:00,PV404,24,1,9
```
and provide the new CSV file path as described in the command line args

### Command line usage example 

```bash
python find_companiation.py --bags-count=2 --show-cost=True
```
