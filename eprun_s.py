# eprun_s.py    script for executing single-building EnergyPlus simulations through its Python API
# usage         python3 eprun_s.py <city> <year> <climate> <buildingID>
#               python3 eprun_s.py detroit 2040 rcp45 001

import argparse 
import sys 
import os
import multiprocessing as mp
from multiprocessing import Pool
import time

# Parse input arguments 
parser = argparse.ArgumentParser(description="Required eprun_s Arguments")

parser.add_argument('--city', '-c', help='city name (baltimore|boston|dallas|detroit|minneapolis|orlando|phoenix|seattle)', type=str, required=True)
parser.add_argument('--year', '-y', help='4-digit year', type=str, required=True)
parser.add_argument('--climate', '-w', help='climate scenario (historical|rcp45|rcp85)', type=str, required=True)
parser.add_argument('--id', '-i', help='3-digit building ID', type=str, required=True)

args = parser.parse_args()

city = args.city
year = args.year
climate = args.climate
id = args.id

cwd = os.getcwd()

# Query input idf


# Query input epw
