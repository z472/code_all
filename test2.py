import random
import os
class Ari_exp:
    '''
    属性：数字大小范围，运算符数量，负数检测量
    方法：生成数字，生成算术表达式，计算算术表达式，
    '''
    nmax = -1
    noperator = 3 #规定运算符个数不超过3
    def Produce_num(self):
        #随机数，真分数或是整数
        i=random.randint(0,100)
        if i%2 :
            a = random.randint(1,self.nmax)
            b = random.randint(1,self.nmax)
            c,d = a,b
            n = self.max_two(c,d)   #之前是个循环，这个调用没测试，不过出错概率很小
            a,b = c//n,d//n
            if a>b:
                if b==1:
                    return str(a//b) 
                else :
                    return str(a//b)+"'"+str(a%b)+"/"+str(b)
            elif a<b:
                return str(a)+"/"+str(b)
            else :
                return "1"  
        else :return str(random.randint(0,self.nmax) )#跟踪后面的0的算法
    
    def Produce_ari_exp(self):
        #生成算术表达式，但是不一定符合条件
        operator = [ '+','-','*','/' ]
        ari_exp = [] 
        i = 1
        ope_num = random.randint(1,self.noperator)#运算符数量
        #输出无括号的表达式列表，每个数和运算符之间有空格，为了分清分数
        #和除法，看着舒服一点，也方便插入括号
        ari_exp.extend( [self.Produce_num(),' '] )
        while i<=ope_num:
            ope = operator[random.randint(0,3)]
            ari_exp.extend( [ope,' '] )
            ari_exp.extend([ self.Produce_num() ,' ' ])
            i += 1
        #随机添加括号，目前是只能加一对
        if random.randint(0,9)%2 == 1:
            lindex = 4 * random.randint(0, (ari_exp.__len__()-6)//4 )
            rindex = lindex + 6 + 4*random.randint(0, (ari_exp.__len__()-lindex-6)//4 )
            ari_exp.insert(lindex,'('),ari_exp.insert(rindex,')')
        #上面这段后来改写了一次，因为后面的format_str不能将连续两个是空格的情况解决    
        ari_exp.extend( [ '=' ] )
        return ''.join(ari_exp)
    
    def Lower_num(self,str_num):
        #之前觉得要把负号后的数生成时就弄小它，但是后来发现可以被除法把后面的数减小，这函数无效才对
        #利用部分计算的方法，循环生成一个数直到比传入的数更小
        while True:
            n1 = self.Produce_num()
            ret = self.Compute_non( str_num + ' '+ '-' + ' ' + n1 )
            if ret[0] != '运算中出现负数':
                break
        return n1
    def Compute_non(self,test):
        a_e = test.split(' ')  #不考虑括号影响,test是字符串，a_e是列表
        while a_e.count('*') != 0 or a_e.count('/') != 0:
            t = 0
            for i in a_e:
                if i == '*' or i == '/':
                    break
                t += 1      # t 运算符索引
            left , right = self.Change( a_e[t-1] ),self.Change( a_e[t+1] )
            if a_e[t] == '*':
                result = [ str( int(left[0])*int(right[0]) ),str( int(left[1])*int(right[1]) ) ]
            else:
                if right[0] == '0': return '除数为0导致的错误'
                else: result = [ str( int(left[0])*int(right[1]) ),str( int(left[1])*int(right[0]) ) ]
            a_e.pop(t),a_e.pop(t)
            a_e[t-1] = result[0]+'/'+result[1]
        while a_e.count('+') != 0 or a_e.count('-') != 0:
            t = 0
            for i in a_e:
                if i == '+' or i == '-':
                    break
                t += 1
            left , right = self.Change( a_e[t-1] ),self.Change( a_e[t+1] ) 
            x = self.min_two( int(left[1]),int(right[1]) )  
            if left[0] != '0' and right[0] != '0':
                c,d = x//int(left[1]),x//int(right[1])
                if a_e[t] == '+':
                    result = [ str( int(left[0])*c + int(right[0])*d ) , str(x) ]
                elif int(left[0])*c - int(right[0])*d < 0:
                    return "运算中出现负数"
                else:
                    result = [ str( int(left[0])*c - int(right[0])*d ),str(x) ]
            elif left[0] == '0':    
                if a_e[t] == '+':
                    result = right
                else : return "运算中出现负数"
            else : result = left
            a_e.pop(t),a_e.pop(t)
            a_e[t-1] = result[0]+'/'+result[1]
            if result[0] == '0':
                a_e[t-1] = '0'     
        return ''.join(a_e) #该字符串的形式是'x='或'x'  x是字符串的最终结果
    
    def Compute_all(self,test):
        a_e = test.split(' ')
        #print(a_e)
        a_e = self.format_str(a_e)
        #print(a_e)
        t ,tt = -1 ,-1
        for i in a_e:
            if '(' in i:
                t = a_e.index(i)
            if ')' in i:
                tt = a_e.index(i)
        if t >= 0:
            child_ari_exp = a_e[ t:tt+1 ]
            #去括号，计算括号内容，合并到总算术表达式中
            child_ari_exp[0],child_ari_exp[tt-t] = child_ari_exp[0][1:],child_ari_exp[tt-t][:child_ari_exp[tt-t].__len__()-1]
            if self.Compute_non(''.join(child_ari_exp) ) == '除数为0导致的错误': a_e = list('除数为0导致的错误')
            elif self.Compute_non(''.join(child_ari_exp) ) == "运算中出现负数" :a_e = list("运算中出现负数")
            else :
                a_e[t] = self.Compute_non(''.join(child_ari_exp) )
                a_e[t+1:] = a_e[tt+1:]
        return self.Compute_non(''.join(a_e) )

    def answer_format(self,str_ans):#把Compute_all的答案修饰一下
        if str_ans[ str_ans.__len__()-1 ] == '=':
            str_ans = str_ans[ :str_ans.__len__()-1 ]
        n3 = str_ans.split('/')
        if n3[0] == '0':
            return '0'
        x = self.max_two( int(n3[0]), int(n3[1]) )
        n3[0] ,n3[1]= str( int(n3[0])//x ) ,str( int(n3[1])//x )
        if n3[1] == '1':
            return n3[0]
        elif int(n3[0]) > int(n3[1]):
            return str( int(n3[0])//int(n3[1]) )+"'"+str( int(n3[0]) % int(n3[1]) )+'/'+n3[1]
        else:
            return n3[0]+'/'+n3[1]
        

    def format_str(self,test):#目的是规格化字符串，但传入的是个元素都为字符串的列表
        i = 1
        why = test.__len__()
        while i <= why:
            test.insert( 2*i-1,' ' )
            i += 1
        test.pop( test.__len__()-1 )
        #print(test)
        return test
            
        
    def Change(self,c):#传入生成数方法返回的字符串，返回列表
        if "'" in c:
            fenshu = c.split("'")
            rfenshu = fenshu[1].split('/')
            rfenshu[0] = str( int(fenshu[0])*int(rfenshu[1])+int(rfenshu[0]) )
        elif '/' in c:
            rfenshu = c.split('/')
        else:rfenshu = [ str(c),'1' ]
        return rfenshu

    def max_two(self,a,b):
        if a<b:
            a,b = b,a
        n = 1
        while n:
            n,a,b = a%b,b,a%b
        return a

    def min_two(self,a,b):
        return a*b//self.max_two(a,b)
    
    def End_ari_exp(self,n):#最后的输出，先不包括排除重复表达式的功能
        special = set() # 表达式运算过程字符串的集合，来剔除重复
        i = 1
        fp = open("Exercise.txt",'w')
        fpx = open("Answer.txt","w")
        while i <= n:
            a_e = self.Produce_ari_exp()
            if self.Compute_all(a_e) != '除数为0导致的错误' and self.Compute_all(a_e) != "运算中出现负数":#从之前的结果看，这里至少有一半不合格的被剔除掉
                if ( special & { self.order_exp(a_e) } ) == set():#等于空集
                    special.add(self.order_exp(a_e) )
                    #print(i,':', a_e, self.answer_format(self.Compute_all(a_e))   )
                    if i == 1:
                        fp.write(str(i)+':'+a_e),fpx.write(str(i)+':'+self.answer_format(self.Compute_all(a_e) ) )
                    else:
                        fp.write('\n'+str(i)+':'+a_e),fpx.write('\n'+str(i)+':'+self.answer_format(self.Compute_all(a_e) ) )
                    i += 1
        fp.close(),fpx.close()

                    
    def order_exp(self,str_right):#将正确的准备输出的表达式的运算过程写成字符串，为了判断重复
        ord_exp = []
        a_e = str_right.split(' ')
        #print(a_e)
        a_e = self.format_str(a_e)
        #print(a_e)
        t ,tt = -1 ,-1
        for i in a_e:
            if '(' in i:
                t = a_e.index(i)
            if ')' in i:
                tt = a_e.index(i)
        if t >= 0:
            child_ari_exp = a_e[ t:tt+1 ]
            #去括号，在括号中寻找最先做的操作
            child_ari_exp[0],child_ari_exp[tt-t] = child_ari_exp[0][1:],child_ari_exp[tt-t][:child_ari_exp[tt-t].__len__()-1]
            ord_exp = self.odr_help(''.join(child_ari_exp) ,ord_exp ) #传进去的列表会在方法内被修改，相当于传给过去一个地址
            a_e[t] = self.Compute_non(''.join(child_ari_exp) )
            a_e[t+1:] = a_e[tt+1:]
        ord_exp = self.odr_help( ''.join(a_e), ord_exp )  
        return  ''.join(ord_exp)

    def odr_help(self,str_right,ord_exp):   #ord_exp是列表，该函数返回值也是列表，它就是上一个函数的复用段
        a_e2 = ''.join(str_right).split(' ')
        while a_e2.count('*') != 0 or a_e2.count('/') != 0:
            t2 = 0
            for ii in a_e2:
                if ii == '*' or ii == '/':
                    break
                t2 += 1
            left,right = self.Change(a_e2[t2-1])[0]+'/'+self.Change(a_e2[t2-1])[1] ,self.Change(a_e2[t2+1])[0]+'/'+self.Change(a_e2[t2+1])[1]#让数的形式一致
            if a_e2[t2] == '*':
                if self.Compute_non(left+' '+'-'+' '+right) == "运算中出现负数":#让左右可交换运算输出的字符串变的一致
                    ord_exp.extend([  left+' '+'*'+' '+right,' ' ])
                else:   ord_exp.extend([  right+' '+'*'+' '+left,' ' ])
                a_e2[t2-1] = self.Compute_non(left+' '+'*'+' '+right)
                a_e2.pop(t2) , a_e2.pop(t2)
            else :
                ord_exp.extend([ left+' '+'/'+' '+right , ' '])
                a_e2[t2-1] = self.Compute_non(left+' '+'/'+' '+right)
                a_e2.pop(t2) , a_e2.pop(t2)
        while a_e2.count('+') != 0 or a_e2.count('-') != 0:
            t2 = 0
            for ii in a_e2:
                if ii == '+' or ii == '-':
                    break
                t2 += 1
            left,right = self.Change(a_e2[t2-1])[0]+'/'+self.Change(a_e2[t2-1])[1] ,self.Change(a_e2[t2+1])[0]+'/'+self.Change(a_e2[t2+1])[1]
            if a_e2[t2] == '+':
                if self.Compute_non(left+' '+'-'+' '+right) == "运算中出现负数":#让左右可交换运算输出的字符串变的一致
                    ord_exp.extend([  left+' '+'+'+' '+right,' ' ])
                else:   ord_exp.extend([  right+' '+'+'+' '+left,' ' ])
                a_e2[t2-1] = self.Compute_non(left+' '+'+'+' '+right)
                a_e2.pop(t2) , a_e2.pop(t2)
            else :
                ord_exp.extend([ left+' '+'-'+' '+right , ' '])
                a_e2[t2-1] = self.Compute_non(left+' '+'-'+' '+right)
                a_e2.pop(t2) , a_e2.pop(t2)
        return ord_exp

    def test_txt(self,exerfile,answfile):#完成检测文本文件中算术表达式答案的计算，比较，最后输出信息
        correct,wrong = 0 , 0
        c1 = list()
        w1 = list()
        fp = open(exerfile,"r")
        fpx = open(answfile,"r")
        while True:
            str1 = fp.readline()
            if str1.__len__() == 0:
                break
            else:                
                str1 = str1.split(':')
            #默认是每道题都有答案的，但答案文件如果中间有一道题没有答案也有可能
            str2 = fpx.readline()
            str2 = str2.split(':')
            '''
            if str2.__len__() != 0:
                str2 = str2.split(":")
            else:
                wrong += 1
                w1.append( str1[0])
            '''
            str1[1] = str1[1][ : str1[1].__len__()-1]
            keep1,keep2 = list( self.answer_format(self.Compute_all(str1[1]) ) ),list(str2[1])    #最后一行的处理和前几行不一样，写的是反刍式的判断
            str2[1] = str2[1][ : str2[1].__len__()-1]
            if self.answer_format(self.Compute_all(str1[1]) ) != str2[1] :
                wrong += 1
                w1.append( str1[0] )
            else:
                correct += 1
                c1.append( str1[0] )
        if ''.join(keep1) == ''.join(keep2):
            wrong -= 1
            GG = w1.pop( w1.__len__()-1 )
            correct += 1
            c1.append(GG)
        if c1 != list():
            print("Correct:",correct,'(',''.join(self.format_str(c1) ),')' )
        else: print("Correct:",correct,'(',''.join(c1),')' )
        if w1 != list():
            print("Wrong:",wrong,'(',''.join(self.format_str(w1) ) ,')')
        else :print("Wrong:",wrong,'(',''.join(w1),')' )
        

# 与用户交互：-r：生成数最大值，-n:生成题目的个数，
#-e <exercisefile>.txt -a <answerfile>.txt:检测答案正确性，并输出统计结果,功能写出来了
#也能通过改变已建立的两个文件内容来验证，但是没写用户交互的接口

while True:
    c = input("-r")
    nmax =  int(c)
    if nmax <= 0:
        print("-r:重新输入")
    else :
        break
print("nmax = ",nmax)

while True:
    c = input("-n")
    n = int(c)
    if n <= 0:
        print("-n:重新输入")
    else :
        break

a = Ari_exp()
a.nmax = nmax
a.End_ari_exp(n)
a.test_txt('Exercise.txt','Answer.txt')

    


    

