# import time
# start_time = time.time()
# i=0
# for i in range(100):
#     i+=1
# end_time = time.time()
# print(end_time-start_time)
# import time
# start = time.clock()
# i=0
# for i in range(100):
#    i+=1
# end = time.clock()
# print(end-start)
# from time import *
# begin_time = time()
# i=0
# while i<100:
#     print(i)
#     i+=1
#
# end_time = time()
# run_time = end_time-begin_time
# print ('该循环程序运行时间：',run_time)

import time
start =time.clock()
sum = 0
for i in range(1,101):
    sum=sum+i
print(sum)
end = time.clock()
print('Running time: %s Seconds'%(end-start))




#print(time.gmtime(0))
# import datetime
# starttime = datetime.datetime.now()
# #long running
# sum = 0
# for i in range(1,101):
#     sum+=i
# print(sum)
# endtime = datetime.datetime.now()
# print(endtime - starttime)

# import timeit
# print(timeit.timeit('1+1',number=10**5))
# print(timeit.timeit('1+1',number=10**6))
# print(timeit.timeit('1+1',number=10**8))
