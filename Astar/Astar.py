Scale = []
Opened = []
Op_gn = []
Op_fn = []
Op_parent = []#the parent of the opened node,it's in the visited list
Visited = []
Vi_fn = []
Vi_parent = [] #the parent of the visited node
temp = [[]] #the list for output
correct = [] #the correct moving sequence

def Astar(Goal):
    Opened.clear()
    Op_gn.clear()
    Op_fn.clear()
    Op_parent.clear()
    Visited.clear()
    Vi_fn.clear()
    Vi_parent.clear()

    Container = 0   # original state
    Opened.append(0)
    Op_gn.append(0)
    Op_parent.append(-1) #let -1 be parent of root
    Op_fn.append(Goal)
    correct.clear()

    while Container != Goal:
        min_fn = min(Op_fn)     # value of min f(n)
        min_index = Op_fn.index(min_fn) # index of min f(n)
        vi_target = Opened[min_index] # #kg of min_fn
        min_gn = Op_gn[min_index] # get g(n) for calculate
        min_parent = Op_parent[min_index]
        Container = vi_target  # update the Container

        del Opened[min_index]
        del Op_fn[min_index]
        del Op_gn[min_index]
        del Op_parent[min_index]

        Visited.append(vi_target)  # put the node in visited list
        Vi_fn.append(min_fn)  # and its f(n)
        Vi_parent.append(min_parent)
        if Container == Goal:
            break

        parent_to_new = (len(Visited)-1) #get the last index, it's the parent index of new nodes in opened list
        print("Now, visit:"+str(vi_target)+"kg,f(n):"+str(min_fn))

        for i in range(len(Scale)):#add nodes to opened list with gn,fn,parent，      #g(n) = g(n) + Scale[i]       f(n) = g(n) + |#kg - goal|
            Opened.append(Scale[i] + vi_target)
            Op_gn.append(min_gn + Scale[i])
            Op_fn.append(Op_gn[-1] + abs(Opened[-1] - Goal))
            Op_parent.append(parent_to_new)
            if vi_target - Scale[i] >= 0: # the #kg in the container needs >=0
                Opened.append(vi_target - Scale[i])
                Op_gn.append(min_gn + Scale[i])
                Op_fn.append(Op_gn[-1] + abs(Opened[-1] - Goal))
                Op_parent.append(parent_to_new)

        print("Opened list after visit:")
        temp = list(zip(Opened, Op_fn))  #merger the #kg and f(n)
        print(temp)
        temp.clear()

    print("Visited list:")
    temp = list(zip(Visited, Vi_fn))
    print(temp)
    temp.clear()

    correct.append(len(Visited)-1)
    while Vi_parent[correct[-1]] != -1:
        p = Vi_parent[correct[-1]]
        correct.append(p)
    correct.reverse()
    print("the correct sequence：\n(Difference between two adjacent numbers is the amount of rice that is moved)")
    for i in correct:
        print(Visited[i])
    print("the total cost:")
    print(Vi_fn[-1])

    #Starting from the last node, locate the position of each parent node, that is, the last bit of correct
    #Record until find -1, and output in reverse order of the record list, output Vi_fn(-1)


if __name__=='__main__':
    #input Scales and Goals
    Str_scale = input("input the #kg of the scales splited with space:")
    Scale = Str_scale.split(" ")
    for i in range(len(Scale)):
        Scale[i] = int(Scale[i])
    Goal_1 = int(input("input the GOAL #kg of the container No.1:"))
    Goal_2 = int(input("input the GOAL #kg of the container No.2:"))

    print("Container No.1 Start:")
    Astar(Goal_1)
    print("Container No.1 "+str(Goal_1)+"kg completed\n")
    print("Container No.2 Start:")
    Astar(Goal_2)
    print("Container No.2 "+str(Goal_2)+"kg completed")

