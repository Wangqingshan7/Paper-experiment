

str1= "hello 11adasdsadsadas"

for i in range(5):
    path = 'hello'+str(i)+'.txt'
    print(path)
    with open(path,'w') as f:    #设置文件对象
        f.write(str1+"\n")