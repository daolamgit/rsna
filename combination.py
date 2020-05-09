def comb_nonorder_bottomup_yield(a,k):
    '''
    combinations that has no order generate bottom up and use yield
    '''
    def bt(currentIndex=0, curr=[]):
        if len(curr) == k: #one of the result
            # print (curr)
            yield curr
        else:
            for i in range(currentIndex, len(a)): # range(current Index so that they are not duplicate in order
                curr.append(a[i]) #build up the result
                # print( curr)
                yield from bt(i+1, curr) #when use yield, recursive make call yield from to call or else it will not work
                curr.pop() # back track
    return bt( )

def comb_nonorder_bottomup(a,k):
    '''
    bottom up recursive for normal combination generation
    '''
    res = []
    def bt(currentIndex=0, curr=[]):
        if len(curr) == k: #one of the result
            # print (curr)
            res.append( curr[:]) #remember : to copy curr to res or else it is just an address
            return # return to stop recursive
        for i in range(currentIndex, len(a)): # range(current Index so that they are not duplicate in order
            curr.append(a[i]) #build up the result
            bt(i+1, curr) #i+1 to move the index forward
            curr.pop() # back track


    bt()
    return res

def comb_order_bottomup( a, k):
        '''
    bottom up recursive for normal combination generation wither ordering 
    '''
    res = []
    def bt( currentIndex = 0, currCombine = []):
        # print( currentIndex)
        if len (currCombine) == k:
            # print( currCombine)
            res.append(currCombine[:])
            return

        for i in range( 0, len(a)): #range start from 0 so that res can be duplicate in order
            if a[i] in currCombine: #check so that no duplicate in a result
                continue # move on
            currCombine.append(a[i])
            bt(i+1, currCombine) #i+1 to move the next index
            currCombine.pop()
    bt()
    return res

def comb_order_rep_bottomup( a, k):
    '''
    bottom up recursive for normal combination generation with ordering and repetition
    '''
    res = []
    def bt( currentIndex = 0, currCombine = []):
        # print( currentIndex)
        if len (currCombine) == k:
            # print( currCombine)
            res.append(currCombine[:])
            return

        for i in range( 0, len(a)):
            currCombine.append(a[i]) #here is no check for duplicate so duplicate is allowed
            bt(i+1, currCombine)
            currCombine.pop()
    bt()
    return res

def comb_nonorder_topdown_yield(A,K):
    '''
    Questions: how to stop at k if we start base case at 0????
    A: start from
    '''
    def bt( a, k):
        if k==0: #first element in queue/list
            yield []
        else: #without else, it would over flow as the 2nd call of yield will call for loop next line
            for currentIndex in range(k-1, len( a)): #just use from k-1 onward to swap in
                # cura = a[:currentIndex] + a[currentIndex+1:]
                cura = a[:currentIndex] # only use cura from 0 to but not current index to build the prev sol
                # cura = a
                for p in bt(cura, k-1):
                    # print(p)
                    yield p + [a[currentIndex]]

    return bt(A, K)

def comb_nonorder_topdown(A,K):
    '''
    Questions: how to stop at k if we start base case at 0????
    A: start from
    '''
    def bt( a, k):
        if k==0: #first element in queue/list
            return [[]]
        ls = []

        for currentIndex in range(k-1, len( a)): #just use from k-1 onward to swap in
            # cura = a[:currentIndex] + a[currentIndex+1:]
            cura = a[:currentIndex] # only use cura from 0 to but not current index to build the prev sol
            # cura = a
            for p in bt(cura, k-1):
                # print(p)
                ls.append( p + [a[currentIndex]])
        return ls

    return bt(a, k)

def comb_order_topdown(A,K):
    '''
    Questions: how to stop at k if we start base case at 0????
    A: start from
    '''
    def bt( a, k):
        if k==0: #first element in queue/list
            return [[]]
        ls = []

        for currentIndex in range( len( a)): #any index can be used to swap in
            cura = a[:currentIndex] + a[currentIndex+1:] #not include the currentIndex, indicate no repetition
            # cura = a[:currentIndex]
            for p in bt(cura, k-1):
                # print(p)
                ls.append( p + [a[currentIndex]])
        return ls

    return bt(a, k)

def comb_order_rep_topdown(A,K):
    '''
    Questions: how to stop at k if we start base case at 0????
    A: start from
    '''
    def bt( a, k):
        if k==0: #first element in queue/list
            return [[]] #return a list of list as the result is a list of list
        ls = []

        for currentIndex in range( len( a)): #range start at 0 indicates repetition
            cura = a #we use all the indices, ie. repetition , redundance, just for cf. to other problems clear
            for pre in bt(cura, k-1): #k-1 shows that we get one element a[currentindex]
                # print(p)
                ls.append( pre+ [a[currentIndex]]) #build the result from previous result
        return ls

    return bt(a, k)

a = [1,2,3]
# a = ['a','b','c','d']
# a = range(8)
k= 2

# print( comb_order_bottomup(a, k))

# print( comb_nonorder_topdown_leet(4, 2))

print( comb_nonorder_topdown(a,k))

# print( comb_order_topdown(a, k))
# print( comb_order_rep_topdown(a, k))

assert sorted(comb_nonorder_topdown(a,k)) == [[1,2],[1,3],[2,3]]
assert sorted(comb_order_topdown(a,k)) == [[1,2],[1,3],[2,1],[2,3],[3,1],[3,2]]
assert sorted(comb_order_rep_topdown(a,k)) == [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]]

assert sorted(comb_nonorder_bottomup(a,k)) == [[1,2],[1,3],[2,3]]
assert sorted(comb_order_bottomup(a,k)) == [[1,2],[1,3],[2,1],[2,3],[3,1],[3,2]]
assert sorted(comb_order_rep_bottomup(a,k)) == [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]]

print ('all passed!')
