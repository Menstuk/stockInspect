from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import pandas as pd


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            data_df = pd.read_csv('end_of_day_prices.csv', names=['id', 'date', 'close_price'], header=None)
            # data_df['date'] = pd.to_datetime(data_df['date'])
            parsed_url = urlparse(self.path)
            if parsed_url.path == '/getStocksByDate':
                date = parse_qs(parsed_url.query)['date'][0]
                stocks_json = self.get_stocks_by_date(data_df, date).to_json(orient='records')
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(stocks_json.encode(encoding='utf_8'))
            else:
                self.send_response(404)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                self.wfile.write('route not found'.encode())
        except Exception as err:
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'an error occurred: {err=}'.encode())

    def get_stocks_by_date(self, df, date):
        return df[pd.to_datetime(df['date']) == date]

def main():
    PORT = 9000
    server_address =('localhost', PORT)
    server = HTTPServer(server_address, RequestHandler)
    print('Server is running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
