class item:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def connected_block_generation_algorithm(record):
    struct_list = []
    visit = []
    block = []
    next = [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]]
    cnt = 0
    for i in range(len(record)):
        for j in range(len(record[i])):
            #print(record[i][j])
            if visit[i][j] == 0 and record[i][j]>0:
                cnt+=1
                visit[i][j] = 1
                head = 1
                tail = 1
                q = item(i,j)
                struct_list.append(q)
                tail += 1
                while head<tail:
                    p = struct_list[head]
                    block[cnt][struct_list[head].x][struct_list[head].y] = record[struct_list[head].x][struct_list[head].y]
                    for k in range(8):
                        nx = p.x + next[k][0]
                        ny = p.y + next[k][1]
                        if visit[nx][ny] == 0 and record[nx][ny]>0:
                            visit[nx][ny] = 1
                            struct_list[tail].x = nx
                            struct_list[tail].y = ny
                            tail += 1
                    head += 1
    print('cnt：',cnt)
if __name__ == '__main__':
    r =[[0, 1, 2,0,0,0,0,0,0,0,0],[0,0,6,4,5,2,1,0,0,0,0],[0,0,0,3,0,0,0,0,0,0,0],
         [0, 0, 0, 0, 0, 0, 0,0,0,0,0],[0,0,0,1,0,0,0,0,0,0,0],[0,0,2,3,4,0,0,0,0,0,0],
         [7, 0, 0, 3, 0, 0, 0,0,3,0,0],[0,0,0,0,0,3,2,0,0,0,0],[4,6,7,0,0,3,0,0,6,0,0],
         [0, 2, 0, 0, 0, 0, 0,0,5,0,0],[0,3,4,0,0,0,0,0,2,7,0],[0, 1, 2,0,0,0,0,0,7,0,0],
         [0,0,6,4,5,2,1,0,6,0,0],[0,0,0,3,0,0,0,0,4,0,0],
         [0, 0, 0, 0, 0, 0, 0,0,0,0,0],[0,0,0,1,0,0,0,0,5,0,0],[0,0,2,3,4,0,0,0,6,0,0],
         [0, 0, 0, 3, 0, 0, 0,6,7,0,0],[0,0,0,0,0,3,2,0,3,4,0],[4,6,7,0,0,3,0,0,7,0,0],
         [0, 2, 0, 0, 0, 0, 2,0,0,0,0],[0,3,4,0,0,0,3,0,0,6,0]]
    connected_block_generation_algorithm(r)