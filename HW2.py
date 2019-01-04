
# coding: utf-8

# In[198]:


# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 19:34:18 2018

@author: NTHU
"""

import numpy as np
import pdb

#Plaintext="a3 c5 08 08 78 a4 ff d3 00 ff 36 36 28 5f 01 02"
#Key="36 8a c0 f4 ed cf 76 a6 08 a3 b6 78 31 31 27 6e"
#aa=input("a:")
Plaintext=input('Plaintext:')
Key=input('Key:')
mx='100011011'

#mx='1011'
def hex2bin(a):
    ans= bin(int(a,16))
    ans=ans[2:]
    ans='0'*(len(mx)-1-len(ans))+ans
    return ans
def bin2hex(a):
    ans=hex(int(a,2))
    ans=ans[2:]
    if len(ans)!=2:
        ans='0'+ans
    return ans


def gf256_add(a,b,mx):
    mx_len=len(mx)
    add_ans=bin(int(a,2)^int(b,2))
    if len(add_ans) < mx_len:
        
        add_ans=add_ans[2:]
        add_ans='0'*(len(mx)-1-len(add_ans))+add_ans
        
    else:
        add_ans=add_ans[2:]
   # print('add_ans',add_ans)
    return(add_ans)
    
    
def gf256_multi_x(a,mx):
    
    if a[0]=='0':
        multi_x_ans=a[1:]+'0'
    else:
        tem=a+'0'

        multi_x_ans=gf256_add(tem,mx,mx)
    if len(multi_x_ans)<8:
        multi_x_ans='0'+multi_x_ans
    return(multi_x_ans)

    
def gf256_multi(a,b,mx):
    if len(b)!=8:
        b='0'*(8-len(b))+b
    if len(a)!=8:
        a='0'*(8-len(a))+a
    a0=a
    a1=gf256_multi_x(a,mx)
    a2=gf256_multi_x(a1,mx)
    a3=gf256_multi_x(a2,mx)
    a4=gf256_multi_x(a3,mx)
    a5=gf256_multi_x(a4,mx)
    a6=gf256_multi_x(a5,mx)
    a7=gf256_multi_x(a6,mx)
    a=[a7,a6,a5,a4,a3,a2,a1,a0]
    tem='00000000'
    for i in range(len(tem)):
        
        if b[i]=='1':
            tem=bin(int(tem,2)^int(a[i],2))
            tem=tem[2:]
            if len(tem)<8:
                tem='0'*(8-len(tem))+tem
    return tem    

 


def c1(a):           #count 1
    for i in range(len(a)):
        if a[i]=='1':
            digi= len(a)-i
            break
    return digi
  
      
def gf256_div(a,b,mx):
    quotient='00000000'
    dividend=a    #被除數
    divisor=b    #除數
    
  
   
    t=1
    if divisor=='00000001':
        quotient=a
        rem='00000000'
    else:
        a_d=c1(a)   #  a's digits
        b_d=c1(b)
        while t==1 :
            d_d=a_d-b_d   #digits difference
            k='0'*(7-d_d)+'1'+'0'*(d_d)
            if len(dividend)==9:
                quotient=gf256_add(quotient,k,mx)
                rem=gf256_multi(divisor,quotient,mx)
                a_d=c1(rem)
                if a_d >= b_d:
                    dividend=rem
                else:
                    break

            else:
                quotient=gf256_add(quotient,k,mx)
                #print('quotient',quotient)
                tem=gf256_multi(divisor,k,mx)
                #print('tem',tem)
                rem=gf256_add(dividend,tem,mx)
                #print('rem',rem)
                a_d=c1(rem)
                if a_d >= b_d:
                    dividend=rem
                else:
                    break
    if len(quotient)!=8:
        quotient='0'*(8-len(quotient))+quotient
    if len(rem)!=8:
        rem='0'*(8-len(rem))+rem
        
    return quotient, rem

 


def gf256_inv(aa,mx):
    a=mx
    b=aa
    v_oldd='00000001'
    w_oldd='00000000'
    v_old='00000000'
    w_old='00000001'
    r='00000000'
    if b=="00000000":
        w_now="00000000"
    elif b=="00000001":
        w_now="00000001"
    else:
        while r!='00000001':
            q=gf256_div(a,b,mx)[0]
            #print('q',q)
            r=gf256_div(a,b,mx)[1]
            #print('r',r)
            if len(r)!=8:
                r='0'*(8-len(r))+r
            if len(q)!=8:
                q='0'*(8-len(q))+q
            #print('r',r)
            v_now=gf256_add(v_oldd,gf256_multi(q,v_old,mx),mx)
            w_now=gf256_add(w_oldd,gf256_multi(q,w_old,mx),mx)
            if len(w_now)!=8:
                w_now='0'*(8-len(w_now))+w_now
            if len(v_old)!=8:
                v_now='0'*(8-len(v_now))+v_now
            v_oldd=v_old
            v_old=v_now
            w_oldd=w_old
            w_old=w_now
            a=b
            b=r
           
    return w_now

def ip_pro(a):   #input process
    input_=[[None]*4 for i in range (4) ]
    r=0
    c=0
    tem=0
    for i in range(len(a)):
        if a[i]!=" ":
            if tem==0:
                input_[r][c]=a[i]
                tem=tem+1
            else:
                input_[r][c]=input_[r][c]+a[i]
                tem=tem+1
            if tem==2:
                r=r+1
                tem=0
                if r==4:
                    c=c+1
                    r=0
    return input_


        
        
def wex(a,b,mx):
    ans=''
    for i in range(4):
        tem1=a[2*i]+a[2*i+1]
        tem2=b[2*i]+b[2*i+1]
        temans=gf256_add(hex2bin(tem1),hex2bin(tem2),mx)
        ans=ans+bin2hex(temans)
    return ans
    
        
def w_key(key):
    input_key=ip_pro(key)
   # print('key',input_key)
    r=['01000000','02000000','04000000','08000000','10000000','20000000','40000000','80000000','1b000000','36000000']
    w_ma=[[None] for i in range(44)]
    w_ma[0]=input_key[0][0]+input_key[1][0]+input_key[2][0]+input_key[3][0]
    w_ma[1]=input_key[0][1]+input_key[1][1]+input_key[2][1]+input_key[3][1]
    w_ma[2]=input_key[0][2]+input_key[1][2]+input_key[2][2]+input_key[3][2]
    w_ma[3]=input_key[0][3]+input_key[1][3]+input_key[2][3]+input_key[3][3]
    for w in range (10):
        tem=w_ma[4+4*w-1]
        shift=tem[2:]+tem[0:2]
        
        inv=''
        for j in range(4):
            
            tem=hex2bin(shift[j*2]+shift[j*2+1])
            tem_inv=gf256_inv(tem,mx)
            tem_str='10001111'
            tem_mat=np.zeros((8,8))


            for i in range(8):
                for j in range(8):

                    tem_mat[i][j]=int(tem_str[j])

                tem_str=tem_str[7]+tem_str[0:7]
            y=np.zeros((1,8))
            a=[1,1,0,0,0,1,1,0]
            add_col=np.reshape(a,(1,8))   
                
                
            for i in range(8):
                temm=0
                for j in range(8):
                    inv_2bin=tem_inv

                    inv_2bin=inv_2bin[::-1]
                    temm=temm+tem_mat[i][j]*int(inv_2bin[j])

                y[0][i]=(temm+add_col[0][i])%2
                out=""
            for k in range(8):
                    out=out+str(y[0][7-k])[0]
                    t_inv=bin2hex(out)

            inv=inv+t_inv
      
        t_w=''
        for k in range(4):
            r_tem=r[w]
            r_tem2=r_tem[2*k]+r_tem[2*k+1]
            inv_tem=inv[2*k]+inv[2*k+1]
            rexor=gf256_add(hex2bin(inv_tem),hex2bin(r_tem2),mx)   #r exclusive or
            t_w=t_w+bin2hex(rexor)
        
        w_ma[4+4*w]=wex(w_ma[4*w],t_w,mx)
        w_ma[4+4*w+1]=wex(w_ma[4*w+1],w_ma[4+4*w],mx)
        w_ma[4+4*w+2]=wex(w_ma[4*w+2],w_ma[4+4*w+1],mx)
        w_ma[4+4*w+3]=wex(w_ma[4*w+3],w_ma[4+4*w+2],mx)
    return w_ma


wma=w_key(Key)
print(wma)




def sub(input_):
    inv_=[[None]*4 for i in range(4)]
    for jj in range(4):
        for ii in range(4):
            temp=hex2bin(input_[jj][ii])
            #print(temp)
            inv_[jj][ii]=bin2hex(gf256_inv(temp,mx))
    tem_col=np.zeros((1,8))

    #pdb.set_trace()


    bytesub=[[None]*4 for i in range(4)]
    tem_str='10001111'
    tem_mat=np.zeros((8,8))


    for i in range(8):
        for j in range(8):

            tem_mat[i][j]=int(tem_str[j])

        tem_str=tem_str[7]+tem_str[0:7]

    y=np.zeros((1,8))
    a=[1,1,0,0,0,1,1,0]
    add_col=np.reshape(a,(1,8))
    for s in range(4):
        for t in range(4):
            for i in range(8):
                tem=0
                for j in range(8):
                    inv_2bin=hex2bin(inv_[s][t])

                    inv_2bin=inv_2bin[::-1]
                    tem=tem+tem_mat[i][j]*int(inv_2bin[j])

                y[0][i]=(tem+add_col[0][i])%2
                out=""
            for k in range(8):
                    out=out+str(y[0][7-k])[0]
                    bytesub[s][t]=bin2hex(out)
    return bytesub

   

def shift(bytesub):
    shift_ma=[[None]*4 for i in range(4)]
    shift_ma[0][0:4]=bytesub[0][0:4]
    shift_ma[1][0:3]=bytesub[1][1:4]
    shift_ma[1][3]=bytesub[1][0]
    shift_ma[2][0:2]=bytesub[2][2:4]
    shift_ma[2][2:4]=bytesub[2][0:2]
    shift_ma[3][0]=bytesub[3][3]
    shift_ma[3][1:4]=bytesub[3][0:3]
    return shift_ma


def mix_col(shift_ma):
    mix_mx=[['02','03','01','01'],['01','02','03','01'],['01','01','02','03'],['03','01','01','02']]
    m_c=[[None]*4 for i in range(4)]
    for k in range(4):
        tem_ma=[i[k] for i in shift_ma]
        for i in range(4):
            tem_sum="00000000"
            for j in range(4):
                tem1=hex2bin(mix_mx[i][j])
                tem2=hex2bin(tem_ma[j])
                tem_mu=gf256_multi(tem1,tem2,mx)
                tem_sum=gf256_add(tem_sum,tem_mu,mx)
            m_c[i][k]=bin2hex(tem_sum)
    return m_c

def xorkey(p,k,mx):
    ptxt=p
    key=k
    pxork=[[None]*4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            pxork[i][j]=bin2hex(gf256_add(hex2bin(ptxt[i][j]),hex2bin(key[i][j]),mx))
    return pxork
pk=xorkey(ip_pro(Plaintext),ip_pro(Key),mx)
pk_=[[None]*4 for i in range(4)]
for i in range(4):
    for j in range(4):
        pk_[i][j]=pk[j][i]
print('S0',pk_)


for i in range (9):
    sub_ma=sub(pk)
    print('sub',i,sub_ma)
    sh_ma=shift(sub_ma)
    print('sh_ma',i,sh_ma)
    mi_ma=mix_col(sh_ma)
    print('mix',i,mi_ma)
    cur_key=wma[4*i+4]+wma[4*i+5]+wma[4*i+6]+wma[4*i+7]
    sub_key=ip_pro(cur_key)
    sub_c=xorkey(mi_ma,sub_key,mx)
    trans_sub_c=[[None]*4 for i in range(4)]
    for k in range(4):
        for j in range(4):
            trans_sub_c[k][j]=sub_c[j][k]
    pk=sub_c
    print('S',i+1,trans_sub_c)
# final round   
sub_ma=sub(pk)
sh_ma=shift(sub_ma)
cur_key=wma[40]+wma[41]+wma[42]+wma[43]
sub_key=ip_pro(cur_key)
cipher_text=xorkey(sh_ma,sub_key,mx)
trans_cipher_text=[[None]*4 for i in range(4)]
for i in range(4):
    for j in range(4):
        trans_cipher_text[i][j]=cipher_text[j][i]
print('ciphertext',trans_cipher_text)



def inv_sub(a,mx):
    a_ma=[[None]*4 for i in range(4)]
    out_ma=[[None]*4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            a_ma[i][j]=hex2bin(a[i][j])[::-1]
    inv_ma=[[0,0,1,0,0,1,0,1],[1,0,0,1,0,0,1,0],[0,1,0,0,1,0,0,1],[1,0,1,0,0,1,0,0],[0,1,0,1,0,0,1,0],[0,0,1,0,1,0,0,1],[1,0,0,1,0,1,0,0],[0,1,0,0,1,0,1,0]]
    a=[1,1,0,0,0,1,1,0]
    add_col=np.reshape(a,(1,8)) 
    add_tem=np.zeros((1,8))
    x=np.zeros((1,8))
    for i in range(4):
        for j in range(4):
            add_tem=np.zeros((1,8))
            x=np.zeros((1,8))
            cur_tern=a_ma[i][j]    #current tern
            for k in range(8):
               
             #   print(add_col)
                add_tem[0][k]=(int(cur_tern[k])+add_col[0][k])%2
            for l in range(8):
                cur_row=inv_ma[l][:]
                temp=0
                for p in range(8):
                   
                    temp=int(temp+cur_row[p]*add_tem[0][p])
                x[0][l]=temp%2
                
            ot=''
            for q in range(8):
                ot=ot+str(x[0][7-q])[0]
            out_ma[i][j]=bin2hex(gf256_inv(ot,mx))
    return out_ma



def inv_shift(in_ma):
    inv_ma=[[None]*4 for i in range(4)]
    inv_ma[0][0:4]=in_ma[0][0:4]
    inv_ma[1][0]=in_ma[1][3]
    inv_ma[1][1:4]=in_ma[1][0:3]
    inv_ma[2][0:2]=in_ma[2][2:4]
    inv_ma[2][2:4]=in_ma[2][0:2]
    inv_ma[3][0:3]=in_ma[3][1:4]
    inv_ma[3][3]=in_ma[3][0]
    return inv_ma
invshift=inv_shift(inv_sub(cipher_text,mx))
#print('inv_shift',inv_shift(inv_sub(cipher_text,mx)))

def inv_mixcol(inv_shift_ma,mx):
    inv_mix_ma=[['0e','0b','0d','09'],['09','0e','0b','0d'],['0d','09','0e','0b'],['0b','0d','09','0e']]
    inv_m_c=[[None]*4 for i in range(4)]
    for k in range(4):
        tem_ma=[i[k] for i in inv_shift_ma]
        for i in range(4):
            tem_sum="00000000"
            for j in range(4):
                tem1=hex2bin(inv_mix_ma[i][j])
                tem2=hex2bin(tem_ma[j])
                tem_mu=gf256_multi(tem1,tem2,mx)
                tem_sum=gf256_add(tem_sum,tem_mu,mx)
            inv_m_c[i][k]=bin2hex(tem_sum)
    return inv_m_c

cur_key=wma[40]+wma[41]+wma[42]+wma[43]
sub_key=ip_pro(cur_key)

                    
d0=xorkey(cipher_text,sub_key,mx)
de=d0
print('S_0',d0)
for d in range(9):
    cur_key=wma[39-4*d-3]+wma[39-4*d-2]+wma[39-4*d-1]+wma[39-4*d]
    sub_key=ip_pro(cur_key)
    inv_sub_ma=inv_sub(de,mx)
    inv_shift_ma=inv_shift(inv_sub_ma)
    inv_mixcol_ma=inv_mixcol(inv_shift_ma,mx)
    inv_key_mix=inv_mixcol(sub_key,mx)
    plaintext=xorkey(inv_mixcol_ma,inv_key_mix,mx)
    de=plaintext
    trans_plaintext=[[None]*4 for i in range(4)]
    for z in range(4):
        for x in range(4):
            trans_plaintext[z][x]=plaintext[x][z]
    
    print('S_',d+1,trans_plaintext)

cur_key=wma[0]+wma[1]+wma[2]+wma[3]    
sub_key=ip_pro(cur_key)
inv_sub_ma=inv_sub(de,mx)
inv_shift_ma=inv_shift(inv_sub_ma)
plaintext=xorkey(inv_shift_ma,sub_key,mx)
trans_plaintext=[[None]*4 for i in range(4)]
for z in range(4):
    for x in range(4):
        trans_plaintext[z][x]=plaintext[x][z]    
print('plaintext',trans_plaintext)
#pdb.set_trace()
# In[190]:






