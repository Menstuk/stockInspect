from django.shortcuts import render
import requests

def stock_table(request):
    url = 'http://localhost:9000/StocksPredictions'
    r = requests.get(url).json()
    params = {
        'data': r
    }
    return render(request, 'stock_table.html', params)
