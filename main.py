import argparse
from sys import argv
from datetime import date, datetime, timedelta, time
from socrata import *
from utils import *

parser = argparse.ArgumentParser(description="Extract the dataset named Police Department Incident Reports: 2018 to Present \
                                 from The City and Condado of San Francisco. Socrata Open Data API have been used to programmatically \
                                 return the dataset.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
type_modes = ["LAST_DATE", "REFRESH"]
parser.add_argument("-m", "--mode", type=str, choices=type_modes, default=type_modes[0], required=True, help="the reference is the last date")
parser.add_argument("-s", "--start_date", type=datetime.fromisoformat, default="2018-01-01", required=("--mode="+type_modes[1] in argv), help="used with refresh mode: from the desired date since 2018-01-01")
parser.add_argument("-e", "--end_date", type=datetime.fromisoformat, default=date.today(), required=("--mode="+type_modes[1] in argv), help="used with refresh mode: from the desired date since 2018-01-01")
args = vars(parser.parse_args())

args_converted = Utils(args).modify_entry_params()

start_date = args_converted["start_date"]
end_date = args_converted["end_date"]

with open('config.json', 'r') as f:
    config = json.load(f)

get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
get_headers = config.get('api').get('headers')
params = config.get('api').get('params')

# new_params = Params(params,start_date).specify_params()
connection = Socrata(get_url, get_headers, params, start_date).api_connection()

# arguments = Params(params,start_date).specify_params()

print(connection, start_date, type(start_date))


