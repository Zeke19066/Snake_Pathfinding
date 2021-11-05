lst = [{'price': 99, 'barcode': '2342355'}, {'price': 88, 'barcode': '2345566'}]

maxPricedItem = max(lst, key=lambda x:x['price'])
minPricedItem = min(lst, key=lambda x:x['price'])