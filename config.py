import configparser
import os
import pandas as pd


script_dir = os.path.dirname(__file__)
relative_path = "config.ini"
file_path = os.path.join(script_dir, relative_path)
 
#Read config.ini file
config_obj = configparser.ConfigParser()
config_obj.read(file_path)
data_info = config_obj["data"]
 
# Set your parameters:
 
# Data
#TEST_DATA = data_info["test_file_path"]
TEST_DATA = "data/Book2.csv"
Input_Data = pd.read_csv(TEST_DATA)

# Filters
MAP_FILTERS_KEYS = ["Organization", "AOR", "CurrentLocation", "Deploy", "Branch", "ServiceSkill", "Group", "Country", "PersonnelType", "Waiver", "SOF", "FTN"]
MAP_FILTERS_VALUES = ["Organization", "AOR", "CurrentLocation", "Deploy", "Branch", "ServiceSkill", "Group", "Country", "PersonnelType", "Waiver", "SOF", "FTN"]


MAP_FILTERS = dict(zip(MAP_FILTERS_KEYS,MAP_FILTERS_VALUES))

ROSTER_FILTERS = {"Org Group":"Organization", 
               "Group": "OrgAbbreviation",
               "Duty Status": "Agency",
               "Deployability": "Location",
               "Nondeploy": "State",
               "FTN": "FTN"}

ALL_FILTERS = {**MAP_FILTERS, **ROSTER_FILTERS}