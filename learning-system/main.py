from requests.exceptions import ConnectionError
from socketIO_client_nexus import SocketIO
from manager import train,test_suite

def onTrainRequest(*args):
    print('Training Request: ', args[0])
    params = args[0]
    client = params['clientID']
    task = params['taskID']
    g = train(task)
    while True:
        try:
            data = next(g)
            if "Action" not in data:
                socket.emit('LSRES:trainRequest', {'event':'ACK', 'clientID':client, 'data':data, '_id': task})
            else:
                socket.emit('LSRES:trainRequest', {'event':'UPDATE_TASK', 'clientID':client, 'data':data, '_id':task})
        except StopIteration:
            socket.emit('LSRES:trainRequest', {'event':'ACK', 'clientID':client, 'data':'END', '_id': task})
            # socket.emit('LSRES:trainRequest', {'event':'UPDATE_TASK', 'clientID':client, 'data':data, '_id':task})
            break

def onTestQuery(*args):
    print("Entering test suite")
    params = args[0]
    client = params['clientID']
    task = params['taskID']
    query = params['query']
    response = test_suite(query,task)
    debug = response['data'][0]
    #for i in debug:
    #    print(i,type(i))
    print(response.keys())
    socket.emit('LSRES:testQuery', {'clientID': client, 'data': response})        

   
try:
    socket = SocketIO('localhost', 8081, wait_for_connection=False)
    socket.emit('pythonConnectionRequest')
    socket.on('LS:trainRequest', onTrainRequest)
    socket.on('LS:testQuery', onTestQuery)
    socket.wait()
except ConnectionError:
    print('The server is down. Try again later.')


# def main():
#     train()
#     js = report()

# main()