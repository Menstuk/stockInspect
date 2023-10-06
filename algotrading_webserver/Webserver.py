from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from DataManager import DataManager

data_manager = DataManager()


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            if parsed_url.path == '/StocksPredictions':
                stocks_preds_df = data_manager.predictor.new_day_preds_df.loc[:, data_manager.predictor.new_day_preds_df.columns != 'id']
                stocks_preds_json = stocks_preds_df.to_json(orient='records')
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(stocks_preds_json.encode(encoding='utf_8'))
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


def main():
    data_manager.initialize()
    PORT = 9000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, RequestHandler)
    print('Server is running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
