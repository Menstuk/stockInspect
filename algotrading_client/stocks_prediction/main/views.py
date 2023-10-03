from django.shortcuts import render
import requests

def stock_table(request):
    url = 'http://localhost:9000/getStocksByDate?date=1%2F11%2F2012'
    r = requests.get(url).json()
    params = {
        'data': r
    }
    return render(request, 'stock_table.html', params)
