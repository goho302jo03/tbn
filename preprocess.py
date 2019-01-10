
def check_empty_element(file):

    data = read_csv(file)
    n_col = len(data[0])
    cnt = [0] * n_col

    for row in data:
        for i in range(n_col):
            if row[i] == '':
                cnt[i] += 1

    print('file: ' + file)
    print('missing value: ' + str(cnt))

def check_new_key(data, key):

    if key not in data:
        data[key] = {
            'info': {
                'age': None,
                'children': None,
                'edu': None,
                'gender': None,
                'income': None,
                'work': None
            },
            'behavior': [],
            'cc': [],
            'fx': [],
            'ln': [],
            'wm': []
        }

def read_csv(file):

    with open(file, 'r') as f:
        data = f.readlines()[1:]

    for idx, row in enumerate(data):
        row = row.strip('\n')
        data[idx] = row.split(',')
        data[idx] = [ele.strip('"') for ele in data[idx]]

    return data

def check_cif_zero():

    cif = read_csv('./src/TBN_CIF.csv')
    zero = read_csv('./src/TBN_Y_ZERO.csv')

    for z in zero:
        flag = 0
        for c in cif:
            if z[0] == c[0]:
                flag = 1
                break
        if flag == 0:
            print(z)

def merge_per_file(data, name, file, col_name):

    for row in file:
        key = row[0]
        check_new_key(data, key)
        tmp = {}
        for idx, ele in enumerate(col_name):
            tmp[ele] = row[idx + 1]
        data[key][name].append(tmp)

def merge():

    data = {}
    cif = read_csv('./src/TBN_CIF.csv')
    fx = read_csv('./src/TBN_FX_TXN.csv')
    ln = read_csv('./src/TBN_LN_APPLY.csv')
    cc = read_csv('./src/TBN_CC_APPLY.csv')
    wm = read_csv('./src/TBN_WM_TXN.csv')
    behavior = read_csv('./src/TBN_CUST_BEHAVIOR.csv')

    for row in cif:
        key = row[0]
        check_new_key(data, key)
        for idx, ele in enumerate(['age', 'children', 'edu', 'gender', 'income', 'work']):
            data[key]['info'][ele] = row[idx + 1]

    merge_per_file(data, 'ln', ln, ['dt', 'amt', 'use'])
    merge_per_file(data, 'cc', cc, ['dt'])
    merge_per_file(data, 'wm', wm, ['dt', 'risk', 'type', 'amt'])
    merge_per_file(data, 'fx', fx, ['dt', 'amt'])
    merge_per_file(data, 'behavior', behavior, ['dt', 'page'])

    print(data['P9KAV4D7P-H7PSCE'])

if '__main__' == __name__:

    merge()
