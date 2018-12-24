#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 13:41:33 2018

@author: top
"""


import numpy as np
from scipy.linalg import norm
from scipy.sparse import csc_matrix
import matplotlib.pyplot as plt


# Input to HITS algorithm is consistency matrix where entry (i,j) indicates \
# edge from i->j
# Consistency Matrix PhiMat is assumed to be a sparse matrix in CSC format


#if __name__ == "__main__":

     #Generating dense adjacency matrix MM
#MM = np.zeros([3, 3])
##MM[0] = [0, 0.5, 0.125]
##MM[1] = [0.5, 0, 0.25]
##MM[2] = [0.125, 0.25, 0]
#MM[0] = [0, 0, 1]
#MM[1] = [0, 0, 1]
#MM[2] = [0, 0, 0]
adj_list_path='hw3dataset/k.txt'



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
        '''
        #if you want your graph to be bi-directed 
        #just add this line
        '''
#        A[int(line1[1])-1][int(line1[0])-1]=1
    fp.close()
    return A
    

MM=FiletoAD(adj_list_path)
print(MM)

#change matrix to sparse matrix representation
PhiMat = csc_matrix(MM)
#print(PhiMat)
#print(PhiMat.transpose())
hubs=[]
auths=[]
def HITS_coherence(MM):

    if (MM.sum()==0):
        return np.array([0])

    #print MM
    # Converting dense matrix to sparse matrix
    PhiMat = MM
    # epsilon is the tolerance between the successive vectors of hubs abd authorities
    epsilon = 0.0001

    # auth is a vector of authority score of dimension Mx1
    # hub is a vector of hub score of dimension Mx1
    M, N = PhiMat.shape

    # Normalizing the authorities and hubs vector by their L2 norm
    auth0 = np.ones([M, 1])
    hubs0 = np.ones([M, 1])
   
    auth1=np.dot(PhiMat.transpose(), hubs0)
    hubs1=np.dot(PhiMat, auth1)
    
    #normalization
    hubs1 = (1.0/norm(hubs1, 2))*hubs1
    auth1 = (1.0/norm(auth1, 2))*auth1
    iteration = 0

    # Calculating the hub and authority vectors until convergence
    while(   (norm (auth1-auth0, 2)+(norm(hubs1-hubs0, 2))) > epsilon):
#    while(iteration<5):
        iteration += 1
        auth0 = auth1
        hubs0 = hubs1
        auth1=np.dot(PhiMat.transpose(), hubs0) #at=A.t h(t-1)
        hubs1=np.dot(PhiMat, auth0 )#ht=A a(t-1)

        #normalization
        hubs1 = hubs1/np.linalg.norm(hubs1)
        auth1 = auth1/np.linalg.norm(auth1)

        #append to list for show vertex1's hubs&auths
        hubs.append(hubs1[1][0])
        auths.append(auth1[1][0])
        print("iter%s"%iteration)
    print ('hub of vertexs:',hubs1.transpose())
    print ('auth of vertexs:',auth1.transpose())
    print('--')
#
#
#

k=HITS_coherence(MM)



#plt show
#plt.figure()
plt.figure(figsize=[12,6])
plt.title("Hubs & Auths\n")
plt.plot(hubs,'-ro',label='hubs of vetext1')
plt.plot(auths,'-go',label='auths of vetext1')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


