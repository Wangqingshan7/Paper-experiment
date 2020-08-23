from scipy.special import comb,perm
import xlwt
# print(perm(3,2))  #A(3,2)
# print(comb(3,2)) #C(3,2)
# print(comb(100,10))
# print(comb(10,5))
# print(comb(100,20))
def probability():
    book = xlwt.Workbook()
    for k in range(1,6):
        n = k*50
        str1 = str(n)
        print(str1)
        table = book.add_sheet(str1, cell_overwrite_ok=True)
        for i in range(1,6):    #虚假数据的比例 10%~50%
            for j in range(1,6):    #Shamir(n,t)中t的取值 n*10%~n*50%
                denominator = comb(n,n*j*0.1)
                numerator = comb(n-n*i*0.1,n*j*0.1)
                print(i, j, "分母:", denominator, "分子:", numerator)
                p = numerator/denominator
                print(p)
                table.write(i,j,p)
    book.save(filename_or_stream="experiment-p.xls")
if __name__ =="__main__":
    probability()