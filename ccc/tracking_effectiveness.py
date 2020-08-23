import time
from fog_server import Fog
from test_algorithm import *
from sss import Shamir
def e_d_v_excution(n):
    key = '1234561234561234'
    M = []
    fog1 = Fog(11, M, key, '127.0.0.3', 8712, 0.0)
    ciphertext = b'u+VsWRiT5x7GCXzjxwjvXh5BM/qYuCS7LHJQgQKEjyKMc8cId+sFldXzIjKztDjdGy+G9FE9zBZ6gJ0cfPkIXQ==S\x9ch,\x95\x81g\xb8\x81\xd8\x9f~u\xe4\x97\xd4'
    for i in  range(n):
        fog1.validation_decrypt_message(ciphertext)
def time_of_all(r,percentage,all_shares):

    size_of_r = len(r) * len(r[0])
    #print(size_of_r)
    need_share = []
    num_of_selected_fog_server = int(size_of_r * percentage)
    print(num_of_selected_fog_server)
    for i in range(num_of_selected_fog_server):
        need_share.append(all_shares[i])
    print(need_share)

    start_edv_time = time.clock()
    #Algorithm1
    ans, blocks, vote_fs_coordinate, sum_of_blocks = find_connection_block(r)
    print(ans, blocks, vote_fs_coordinate, sum_of_blocks)
    #Algorithm2
    s,s_l=select_fog_server(r, blocks,int(size_of_r*percentage))
    print(s,s_l)
    #edv-about twice of size_of_R
    e_d_v_excution(size_of_r*2)
    #cover secret
    print(Shamir.combine(need_share))
    return time.clock()-start_edv_time


if __name__ == "__main__":
    r=[[1, 1, 2, 0, 1, 1, 2, 0, 1, 7],[1, 0, 6, 4, 5, 2, 1, 3, 1, 1],[0, 4, 0, 3, 0, 0, 8, 4, 9, 0],
       [0, 0, 1, 0, 4, 0, 0, 6, 0, 8],[3, 0, 0, 1, 8, 0, 6, 0, 5, 0],[1, 1, 2, 6, 1, 0, 2, 0, 7, 7],
       [1, 0, 6, 4, 5, 2, 1, 0, 0, 1],[0, 4, 0, 3, 0, 0, 8, 0, 9, 0],[0, 0, 1, 0, 4, 0, 0, 6, 1, 8],
       [3, 0, 0, 1, 0, 0, 6, 0, 5, 0],[1, 1, 2, 0, 1, 0, 2, 0, 0, 7],[1, 0, 6, 4, 5, 2, 1, 6, 0, 1],
       [0, 4, 0, 3, 0, 0, 8, 0, 9, 0],[0, 0, 1, 0, 4, 0, 1, 6, 0, 8],[3, 0, 0, 1, 0, 4, 6, 0, 5, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 5, 0],[0, 0, 0, 0, 4, 0, 0, 6, 0, 8],[0, 0, 0, 3, 0, 0, 1, 2, 0, 0],
        [0, 0, 6, 4, 5, 2, 1, 0, 0, 0],[0, 1, 2, 0, 1, 0, 0, 1, 0, 7],[0, 1, 2, 0, 0, 0, 0, 0, 0, 7],
       [0, 0, 6, 4, 5, 2, 1, 0, 3, 0],[0, 0, 0, 3, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 4, 0, 1, 6, 0, 8],
       [0, 0, 0, 1, 0, 1, 0, 2, 5, 0]]
    print(r[14][0])
    t = 0
    for i in range(len(r)):
        for j in range(len(r[i])):
            print(r[i][j],end="")
            if r[i][j]>=1:
                t+=1
        print()
    print(t)
    p = Shamir.pol(50, b'helloworldfight!') #一个多项式，至少需要t份才能恢复出秘密
    main_share = []
    for i in range(1,t+1):
        main_share.append((i, Shamir.make_share(i, p)))
    print(main_share)

    print(time_of_all(r,0.2,main_share)) ######