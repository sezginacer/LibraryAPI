import multiprocessing
import threading
import requests

url = 'http://0.0.0.0:8000/'


def get_token():
    return requests.post(url + 'token/', data={'username': 'admin',
                                               'password': 'admin'}).json()['token']

def req(token):
    requests.get(url + 'book/', headers={'Authorization': 'Token {}'
                                         .format(token)})
    print('<-->')

if __name__ == '__main__':
    cpus = multiprocessing.cpu_count()
    print('CPU Cores: {}'.format(cpus))
    tp = input('thread (t) or process (p): ')
    num = input('how many requests: ')
    token = get_token()
    array = []
    counter = 0

    if tp == 't':
        for i in range(int(num)):
            t = threading.Thread(target=req,
                                 args=(token,))
            t.start()
            array.append(t)
            counter += 1
            if counter % cpus == 0:
                for tt in array:
                    tt.join()
                array = []

    elif tp == 'p':
        for i in range(int(num)):
            p = multiprocessing.Process(target=req,
                                        args=(token,))
            p.start()
            array.append(p)
            counter += 1
            if counter % cpus == 0:
                for pp in array:
                    pp.join()
                array = []
    else:
        print('invalid option!')
