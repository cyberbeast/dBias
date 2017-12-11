from requests.exceptions import ConnectionError
from socketIO_client_nexus import SocketIO
from manager import train,report

def onTrainRequest(*args):
    print('Training Request: ', args[0])
    params = args[0]
    client = params['clientID']
    task = params['taskID']
    g = train(task)
    while True:
        try:
            data = next(g)
            socket.emit('LSRES:trainRequest', {'event':'ACK', 'clientID':client, 'data':data})
        except StopIteration:
            socket.emit('LSRES:trainRequest', {'event':'ACK', 'clientID':client, 'data':'END'})
            break           


try:
    socket = SocketIO('localhost', 8081, wait_for_connection=False)
    socket.emit('pythonConnectionRequest')
    socket.on('LS:trainRequest', onTrainRequest)
    socket.wait()
except ConnectionError:
    print('The server is down. Try again later.')


# def main():
#     train()
#     js = report()

# main()