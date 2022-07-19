import yaml
import logging
import re

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            logging.error(exc)

def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string)
    return string

def col_header_val(df, table_cfg):
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x, '_'), list(df.columns)))
    expected_col = list(map(lambda x: x.lower(), table_cfg["columns"]))
    expected_col.sort()
    #df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis=1)
    if list(expected_col) == list(df.columns):
        print("column name validation passed")
        return 1
    else:
        print("column name validation failed")
        mismatch = list(set(df.columns).difference(expected_col))
        print("Columns not in YAML file: ", mismatch)
        missing =  list(set(expected_col).difference(df.columns))
        print("Columns not in data file: ", missing)
        return 0
