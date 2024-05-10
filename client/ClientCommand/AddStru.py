from ClientSocket.SocketClient import SocketClient

class AddStru():
    def __init__(self, client:SocketClient):
        self.parameters = {}
        self.client = client
    
    def show_result(self, res):
        if res['status'] == 'OK':
            print(f"Add {self.parameters} success")
        else:
            print(f"Add {self.parameters} fail")

    def query_name(self, name):
        self.client.name_query(name)
        result = self.client.wait_response()

        return result
    
    def add_name(self, name):
        self.parameters['name'] = name
        self.parameters['scores'] = {}

    def add_subject_and_score(self, subject, score):
        if 'scores' not in self.parameters.keys():
            self.parameters['scores'] = {}
        self.parameters['scores'][subject] = score

    def send_parameters_to_server(self):
        self.client.send_command("add", self.parameters)
        result = self.client.wait_response()

        return result
    
    def reset_parameters(self):
        self.parameters.clear()