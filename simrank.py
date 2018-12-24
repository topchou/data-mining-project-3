#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 13:14:30 2018

@author: top
"""
import numpy as np

path='hw3dataset/graph_5.txt'



#determine the size of adj
def File_max(path):
    A=list()
    fp = open(path, "r")
    for line in iter(fp):
        line1=line.strip().split(",")
        for i in range(len(line1)):
            if int(line1[i]) not in A:
                A.append( int(line1[i]) )      
    fp.close()
    return max(A)

#change txt file to adjacency matrix
#if i,j exist A[i-1][j-1]=1
'''
file would like
1,2
2,3
.
.
.

'''    
def FiletoAD(path):
    size=File_max(path)
    A=np.zeros((size,size))
    fp = open(path, "r")
    for line in iter(fp):
        line1=line.strip().split(",")
        A[int(line1[0])-1][int(line1[1])-1]=1
    fp.close()
    return A


def simrank(C=10):
    Matrix=FiletoAD(path)
    #with transpose() each sum of each row represent indegree of vertexi
    Mt=Matrix.transpose()
    print(Mt)
    
    #calculate indegree of vertex i
    ind_vi=[]
    for i in Mt:
        ind_vi.append(sum(i))
    print((ind_vi))
    
    
    #initial of matrix S
    #S[a][a]=1
    size=Matrix.shape[0]
    S=np.zeros((size,size))
    for i in range(size):
        S[i][i]=1
    
    
    #calculate S_matrix's lower (S is a symetric matrix)
    for i in range(size):
        for j in range(size):
            if (i==j):
                break
            summation=0
            #calculate summation of same indegree vertex of vertex(i,j)
            for index in range(len(ind_vi)):
#                print(Mt[i][index],Mt[j][index])
                if ( (Mt[i][index]==1) and (Mt[j][index]==1) ):
                    summation+=1
#                print(summation)
            #By defenision to calculate similarity of vertex(i,j)
            S[i][j]= round  ( C / (ind_vi[i]*ind_vi[j]) *summation  ,3 )
   
    
    
    
    #reflection upper for S
    for i in range(size):
        for j in range(size):
            if (j>i):
                S[i][j]=S[j][i]
    print(S)
    return S
    
    
simrank()
    
