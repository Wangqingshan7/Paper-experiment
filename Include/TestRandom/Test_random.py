import random
def happy(n,p):
    r = set()
    f = set()
    i=0
    while i<int(n-n*p):
        x = random.randint(1,n)
        if x in r:
            pass
        else:
            r.add(x)
            i+=1
    print(r,len(r))
    print(f,len(f))
if __name__ == "__main__":
    happy(50,0.1)

# #接口返回值
# list1 = ['张三', '李四', '王五', '老二']
# #数据库返回值
# list2 = ['张三', '李四', '老二', '王七']
#
# a = [x for x in list1 if x in list2] #两个列表表都存在
# b = [y for y in (list1 + list2) if y not in a] #两个列表中的不同元素
#
# print('a的值为:',a)
# print('b的值为:',b)
#
# c = [x for x in list1 if x not in list2]  #在list1列表中而不在list2列表中
# d = [y for y in list2 if y not in list1]  #在list2列表中而不在list1列表中
# print('c的值为:',c)
# print('d的值为:',d)

