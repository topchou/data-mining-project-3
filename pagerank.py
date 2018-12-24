#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 16:31:29 2018

@author: top
"""

import numpy as np
from scipy.sparse import csc_matrix
from scipy.linalg import norm


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


#change txt file to adjacency matrix type=np.array
#if i,j exist A[i-1][j-1]=1
'''
file would like
1,2
2,3
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

def pageRank(G, s = .85, maxerr = .05):
    """
    Computes the pagerank for each of the n states
    Parameters
    ----------
    G: matrix representing state transitions
       Gij is a binary value representing a transition from state i to j.
    s: probability of following a transition. 1-s probability of teleporting
       to another state.
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged.
    """
    n = G.shape[0]

    # transform G into markov matrix A
    A = csc_matrix(G,dtype=np.float)
    rsums = np.array(A.sum(1))[:,0]#calcualate outdegree of vertex x
#    print("rs",rsums)
    ri, ci = A.nonzero()
    A.data /= rsums[ri]
#    print(A)

    # bool array of sink states
    sink = rsums==0
#    sink=0.15
    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    interation=1

    while np.sum(np.abs(r-ro)) > maxerr:
#        print(interation)
#        print(np.sum(np.abs(r-ro)))
        ro = r.copy()
        # calculate each pagerank at a time
        for i in range(0,n):
            # inlinks of state i
            Ai = np.array(A[:,i].todense())[:,0]
           
            # account for sink states
            Di = sink / float(n)
        
            # account for teleportation to state i
#            Ei = np.ones(n) / float(n)
            
            
            #By definition of Quick reference 
            #s=1-d(damping factor)
            r[i] = ro.dot( Ai*s + Di*(1-s) )#+ Ei*(1-s) )
            #print(r)

        interation+=1
    # return normalized pagerank

#    return r/float(sum(r))
    return r/np.linalg.norm(r)




if __name__=='__main__':
    # Example extracted from 'Introduction to Information Retrieval'
    path='hw3dataset/k.txt'
#    path='hw3dataset/graph_4.txt'
#    G = np.array([[0,0,1,0,0,0,0],
#                  [0,1,1,0,0,0,0],
#                  [1,0,1,1,0,0,0],
#                  [0,0,0,1,1,0,0],
#                  [0,0,0,0,0,0,1],
#                  [0,0,0,0,0,1,1],
#                  [0,0,0,1,1,0,1]])
    G=FiletoAD(path)
#    print(G)
    k= pageRank(G,s=.85)
    for i in range(len(k)):
        k[i]=round(k[i],3)
    print('pagerank',k)
#    c=0

        