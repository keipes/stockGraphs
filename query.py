import requests
import urllib
import json
import pprint
import string

base_url = 'http://query.yahooapis.com/v1/public/yql?q={query}&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='


def query(query):
    query_url = base_url.format(query=urllib.parse.quote(query))
    return json.loads(requests.get(query_url).text)

def print_as_table(results_list):
    has_header = False
    padding = 4
    header = []
    col_widths = []
    output_rows = []
    for entry in results_list:
        row_data = []
        for idx, field in enumerate(sorted(entry.keys()), 0):
            value = str(entry[field]) if entry[field] is not None else ''
            if idx == len(col_widths):
                col_widths.append(0)
            col_widths[idx] = max(col_widths[idx], len(field), len(value))
            if not has_header:
                header.append(field)
            row_data.append(value)
        output_rows.append(row_data)
        has_header = True
    header_print = '| '
    for idx, col_title in enumerate(header, 0):
        header_print += col_title.ljust(col_widths[idx]) + " | "
    print(header_print)
    for row in output_rows:
        row_print = '| '
        for idx, val in enumerate(row, 0):
            row_print += str(val).ljust(col_widths[idx]) + " | "
        print(row_print)

def chart_js_data(results_list):
    labels = []
    values = []
    key_list = list(results_list[0].keys())
    label_key = 'Date' # key_list[0]
    value_key = 'Adj_Close' # key_list[1]
    for entry in results_list:
        for field, value in entry.items():
            if field == label_key:
                labels.append(value)
            elif field == value_key:
                values.append(value)
    return {
        'labels': labels,
        'values': values
        }

def get_results_list(yql):
    res = query(yql)
    if 'query' in res:
        results = res['query']['results']
        for table in results:
            if isinstance(results[table], dict):
                results_list = [results[table]]
            else:
                results_list = results[table]
            return results_list
    if 'error' in res:
        pprint.pprint(res)

def stock_last_month(symbol):
    yql = 'select Date, Adj_Close from yahoo.finance.historicaldata where symbol=\"{symbol}\" and startDate = "2014-01-01" and endDate = "2014-03-04"'.format(symbol=symbol)
    res = get_results_list(yql)
    return chart_js_data(list(reversed(res)))

def main():
    print(vffvx_last_month())

    # yql = 'select * from yahoo.finance.stocks where symbol=\"vffvx\"'
    # yql = 'select * from yahoo.finance.quote where symbol=\"vffvx\"'
    # yql = 'select Date, Adj_Close from yahoo.finance.historicaldata where symbol=\"vffvx\" and startDate = "2014-01-01" and endDate = "2014-03-04"'
    # res = query(yql)
    # if 'query' in res:
    #     results = res['query']['results']
    #     for table in results:
    #         if isinstance(results[table], dict):
    #             results_list = [results[table]]
    #         else:
    #             results_list = results[table]
    #         print_as_table(results_list)
    #         print(chart_js_data(results_list))
        


    # if 'error' in res:
    #     pprint.pprint(res)
    

if __name__ == '__main__':
    main()
