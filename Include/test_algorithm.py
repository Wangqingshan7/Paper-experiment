import random
def find_connection_block(grid):
    if not grid:
        return 0
    row = len(grid)
    col = len(grid[0])
    vis = set()
    location = []
    directx = [-1, 1, 0, 0,-1,1,-1,1]
    directy = [0, 0, -1, 1,-1,-1,1,1]
    ans = 0
    for i in range(row):
        for j in range(col):
            if grid[i][j] >= 1 and (i, j) not in vis:
                vis.add((i, j))
                stack = [(i, j)]
                ans += 1
                s=[]
                while len(stack) != 0:
                    x, y = stack.pop(0)
                    s.append((x,y))
                    for t in range(8):
                        newx, newy = x + directx[t], y + directy[t]
                        if -1 < newx < row and -1 < newy < col and (newx, newy) not in vis and grid[newx][newy] >= 1:
                            vis.add((newx, newy))
                            stack.append((newx, newy))
                location.append(s)
    # for i in location:
    #     print(i)
    sum_of_blocks = 0
    max = 0
    for i in location:
        sum_of_blocks+=len(i)
        if len(i)>max:
            max = len(i)
            maxi = i
    #print(max,maxi)
    max_flag = 0
    for i in maxi:
        if grid[i[0]][i[1]]>max_flag:
            max_flag = grid[i[0]][i[1]]
            max_block_flag_coordinate = i
    #print(max_block_flag_coordinate)
    return ans,location,max_block_flag_coordinate,sum_of_blocks

def select_fog_server(grid,location,t):
    size_of_blocks = []
    selected_fs =[]
    for i in range(len(location)):
        sum = 0
        for j in range(len(location[i])):
            #print(location[i][j][0], location[i][j][1])
            Flag = grid[location[i][j][0]][location[i][j][1]]
            #print(Flag)
            sum += Flag
        #rint(sum/len(location[i]))
        size_of_blocks.append([i,len(location[i]),sum/len(location[i])])
    #print(size_of_blocks)
    # print(size_of_blocks)
    size_of_blocks = sorted(size_of_blocks,key=(lambda x:[x[1],x[2]]),reverse=True)
    #print(size_of_blocks)
    b = []
    tool_t = t
    for a in size_of_blocks:
        if tool_t < 0:
            break
        else:
            tool_t = tool_t - a[1]
            b.append(a[0])
    #print(b)
    for i in range(len(b)-1):
        #print("第",b[i],"连通块,该联通块雾服务器的数量为：",len(location[b[i]]))
        for j in range(len(location[b[i]])):
            selected_fs.append(location[b[i]][j])
            #print(location[b[i]][j])
    #print(location[b[-2]])
    #print("被选中服务器的坐标：",selected_fs)
    #print(len(selected_fs))
    gap = t-len(selected_fs)
    #print("在最后一个block中挑选的雾服务器数量：",gap)
    fianl_blocks=[]
    for i in location[b[-1]]:
        flag = grid[i[0]][i[1]]
        fianl_blocks.append((i,flag))
    #print(fianl_blocks)
    sort_final_block = sorted(fianl_blocks,key=(lambda x:[x[1]]),reverse=True)
    #print(sort_final_block)
    for i in range(gap):
        #print(sort_final_block[i][0])
        selected_fs.append(sort_final_block[i][0])
    #print(selected_fs,len(selected_fs))
    return selected_fs,len(selected_fs)

    # for i in range(len()-b[-1]):
    #     print(location[b[-2]][i])
def generate_cfs(selected_fs,n,p):
    comporised_fs = set()
    #print(1 in compromised_fs)
    number = 0
    while number < int(n*p):
        random_int = random.randint(0, n-1)
        if selected_fs[random_int] not in comporised_fs:
            comporised_fs.add(selected_fs[random_int])
            number += 1
    #print(comporised_fs)
    #print(coordinate_cfs)
    return  comporised_fs


def behappy(r,threshold_p,c_p):
    num, blocks, voting_fog_server, sum_fog_servers = find_connection_block(r)
    print(num, blocks, voting_fog_server, sum_fog_servers)

    interacted_fs = []
    for block in blocks:
        for f_s in block:
            interacted_fs.append(f_s)
    # print(interacted_fs,len(interacted_fs))
    selected_fs, number_of_selected_fs = select_fog_server(r, blocks, int(sum_fog_servers*threshold_p))  # 5 is the shairm's threshold
    print(selected_fs, number_of_selected_fs)

    # random scheme
    random_scheme_selected = generate_cfs(interacted_fs, sum_fog_servers, threshold_p)
    print("random_scheme_selected:", random_scheme_selected)

    path = 'false data='+str(int(sum_fog_servers*c_p))+' and threshold='+ str(int(sum_fog_servers*t_p))+'.txt'

    with open(path, 'w') as f:
        f.write("r:" + str(r) + '\n' + "interacted_fs:" + str(interacted_fs) + '\n' + "proposed scheme:" + str(
            selected_fs) + '\n' + "random scheme:" + str(random_scheme_selected) + '\n')
    p = 0
    p_c = 0
    for i in range(100):
        # randomly attacked fog server
        compromised_fs = generate_cfs(interacted_fs, sum_fog_servers, c_p)
        print(compromised_fs)
        a = [x for x in selected_fs if x in compromised_fs]
        b = [x for x in random_scheme_selected if x in compromised_fs]
        with open(path, 'a') as f:
            f.write(str(compromised_fs) + '\t' + str(a) + '\t' + str(b) + "\n")
        #print("a:", a)
        #print("b:", b)
        if len(a) == 0:
            p += 1
        if len(b) == 0:
            p_c += 1
    print(p)
    print(p_c)
    with open(path, 'a') as f:
        f.write("proposed scheme accuracy:" + str(p / 100) + "\n" + "proposed scheme accuracy:" + str(p_c / 100))
    print("proposed scheme:", p / 100)
    print("random scheme:", p_c / 100)


if __name__ == '__main__':
    # r = [[0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 0, 0, 2, 0], [0, 0, 0, 3, 0, 0, 0, 9, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0],
    #      [7, 0, 0, 3, 0, 0, 0, 0, 3, 2, 0, 0], [0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0], [4, 6, 7, 0, 0, 3, 0, 0, 1, 6, 0, 0],
    #      [0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 2, 0], [0, 3, 4, 0, 0, 0, 0, 0, 2, 7, 1, 0], [0, 1, 2, 0, 0, 0, 0, 2, 0, 7, 0, 0],
    #      [0, 0, 6, 4, 5, 2, 1, 0, 2, 6, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 3, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 4, 0, 5, 0, 0], [0, 0, 2, 3, 4, 0, 0, 3, 0, 6, 0, 0],
    #      [0, 0, 0, 3, 0, 0, 0, 6, 7, 0, 0, 0], [0, 0, 0, 0, 0, 3, 2, 0, 1, 3, 4, 0], [4, 6, 7, 0, 0, 3, 0, 1, 0, 7, 0, 0],
    #      [0, 2, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0], [0, 3, 4, 0, 0, 0, 3, 0, 2, 0, 6, 0]]
    # r =[[0, 1, 2,0,0,0,0,0,0,0,2,0],[0,0,6,4,5,2,1,0,0,0,2,0],[0,0,0,3,0,0,1,0,0,0,0,0],
    #      [0, 0, 0, 0, 0, 0, 0,0,5,0,0,0],[0,0,0,1,0,0,5,0,0,0,0,0],[0,0,1,2,3,4,0,0,0,0,0,0],
    #      [7, 0, 0, 3, 0, 0,4, 0,0,3,0,0],[0,0,0,5,0,0,3,2,0,0,0,0],[4,6,7,0,3,0,3,0,0,6,0,0],
    #      [0, 2, 0, 0, 0,3,0, 0,0,5,0,0],[0,3,4,0,0,0,1,0,2,7,0],[0, 1, 2,0,0,2,0,0,0,7,0,0],
    #      [0,0,6,4,5,2,2,1,0,6,0,0],[0,0,0,3,0,0,2,0,0,4,0,0],
    #      [0, 0, 0,0, 0, 0, 0, 0,0,0,0,0],[0,0,0,0,1,0,0,0,0,5,0,0],[0,0,2,3,4,0,0,0,0,6,0,0],
    #      [0, 0, 0, 3, 0,1, 0, 0,6,7,0,0],[0,0,0,0,0,3,2,0,0,3,4,0],[4,6,7,0,0,3,0,0,7,0,0,0],
    #      [0, 2, 0, 0, 0, 0,2, 2,0,0,0,0],[0,3,4,0,0,0,0,3,0,0,6,0]]
    #11*22
    #50
    # r=[[0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
    #    [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
    #    [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
    #    [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0]]

    #100
    # r = [[0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
    #      [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
    #      [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
    #      [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0],
    #      [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0],
    #      [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0],
    #      [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],[0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0]]

    #150
    # r= [[0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
    #     [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
    #     [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
    #     [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0],
    #     [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0],
    #     [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0],
    #     [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1],
    #     [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0],
    #     [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1],
    #     [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0]]

    #200
    # r = [[0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
    #      [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
    #      [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
    #      [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0],
    #      [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0],
    #      [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0],
    #      [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1],
    #      [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0],
    #      [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1],
    #      [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0],
    #      [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
    #      [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
    #      [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
    #      [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0]]

    #250
    r = [[0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
         [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
         [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
         [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0],
         [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0],
         [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0],
         [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1],
         [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0],
         [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1],
         [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0],
         [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0],
         [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0], [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4],
         [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0], [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],
         [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0], [0, 1, 2, 0, 0, 7, 0, 7, 0, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 5, 0, 0, 0],
         [1, 0, 0, 3, 0, 0, 0, 9, 0, 0, 3, 0], [0, 0, 0, 9, 0, 0, 0, 2, 0, 0, 2, 0], [0, 0, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0],
         [1, 0, 2, 3, 4, 0, 0, 3, 0, 0, 0, 4], [0, 1, 2, 0, 1, 0, 4, 0, 1, 0, 0, 1], [0, 0, 6, 4, 5, 2, 1, 0, 1, 0, 2, 0],
         [0, 1, 0, 3, 0, 1, 0, 9, 0, 0, 2, 0],[0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0]]
    p_list = [0.1,0.2,0.3,0.4,0.5]
    for c_p in p_list:
        for t_p in p_list:
            behappy(r,t_p,c_p)

