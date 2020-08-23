import threading
import time
from sss import Shamir
from vehicle_client import Vehicle

# def test_threading():
#     i=0
#     while i < 1000:
#         i+=1
def produce_vehicle(x,message):
    key = '1234561234561234'
    v = Vehicle(Shamir.pol(10,123456),'231','pse'+str(x),key)
    broadcast_message = b'ay7eM3N9hyngbWdDBvxGe6HfHTL7MWzrOUW0u1XBjug=S\xed\xc9K\x862\x8ac\xe7\r\xfe\xb2\xb0i\xdb\x12'
    v.establish_connection_and_send_message(broadcast_message,message)
if __name__ == "__main__":
    threading_list=[]
    f = open(r"C:\Users\WangQingShan\Desktop\test.txt", 'r', encoding='utf-8')
    message =f.read()
    print(message)
    f.close()

    # start_time = time.clock()
    # produce_vehicle(1,message)
    # print("execution time:",time.clock()-start_time)

    for j in range(1,5):
        print(j)
        t = threading.Thread(target=produce_vehicle(j,message))
        threading_list.append(t)
    for t in threading_list:
        start_time = time.clock()
        print(t.name)
        t.start()
        print("threading",t.name,"execution time:",time.clock()-start_time)

# key = '1234561234561234'
# v1 = Vehicle(Shamir.pol(10, 123456), '123', 'jack', key)
# broadcast_message = b'ay7eM3N9hyngbWdDBvxGe6HfHTL7MWzrOUW0u1XBjug=S\xed\xc9K\x862\x8ac\xe7\r\xfe\xb2\xb0i\xdb\x12'
# v1.establish_connection_and_send_message(broadcast_message,'hello world')
#print(v1.generate_message(11,"hello world"))