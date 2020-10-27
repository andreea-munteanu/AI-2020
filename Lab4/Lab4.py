"""
# TEST 1 - TRUE

constraints = [('WA', 'SA'), ('WA', 'NT'), ('SA', 'WA'), ('SA', 'NT'), ('NT', 'WA'), ('NT', 'SA')]
domain = {'WA': ['R', 'G', 'B'],
          'SA': ['R', 'G'],
          'NT': ['G']}
x_variables = ['WA', 'SA', 'NT']


# TEST 2 - FALSE

constraints = [('T', 'V'), ('WA', 'NT'), ('WA', 'SA'), ('NT', 'WA'), ('NT', 'Q'), ('NT', 'SA'), ('SA', 'WA'),
               ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('Q', 'NT'), ('Q', 'SA'), ('Q', 'NSW'),
               ('NSW', 'Q'), ('NSW', 'SA'), ('NSW', 'V'), ('V', 'SA'), ('V', 'NSW'), ('V', 'T')]
domain = {'WA': ['R'],
          'SA': ['R', 'G', 'B'],
          'NT': ['R', 'G', 'B'],
          'Q': ['G'],
          'NSW': ['R', 'G', 'B'],
          'V': ['R', 'G', 'B'],
          'T': ['R', 'G', 'B']}
x_variables = ['WA', 'SA', 'NT', 'T', 'Q', 'NSW', 'V']

"""
constraints = []
domain = {}
x_variables = []


# true if no inconsistencies are found
def arc_consistency3() :
    """
    queue = constraints as arcs
    while queue is not empty:
        (X[i],X[j]) <-- queue.pop()
        if revise(csp, X[i], X[j]):
            return False
        for each X[k] in X[i].neighbours\{X[j]}:
            queue.add(X[k],X[j])
    return True

    """
    while len(constraints) != 0 :                            # while (constraints = queue of arcs is not empty):
        print("constraints\n", constraints)
        current_i = constraints.pop(0)[0]                           # (X[i],X[j]) <-- queue.pop()
        current_j = constraints.pop(0)[1]
        print(current_i, "-", current_j)
        if revise((current_i, current_j)) :                         # if revise(csp, X[i], X[j]): return false
            print(domain)
            if len(domain[current_i]) == 0 :
                return False
            for x_k in neighbours(current_i, current_j) :           # for each X[k] in X[i].neighbours\{X[j]}:
                print(x_k)                                               # queue.add(X[k],X[j])
                constraints.append((current_j, current_i))
                constraints.append((x_k[1], current_i))
    return True                                               # return True


# returns true iff we revise the domain of X[i]
def revise(my_tuple) :
    """
    revised <-- False
    for each x(i,j) in D[i] do:
        if no value y in D[j] allows (x,y) to satisfy the constraint X[i]-X[j], then:
            delete x from D[i]
            revised <-- True
    return Revised
    """
    revised = False
    values_x_i = domain.get(my_tuple[0])
    values_x_j = domain.get(my_tuple[1])
    common_elements = [value for value in values_x_i
                       if value in values_x_j]
    if len(common_elements) != 0 :
        for i in common_elements :
            domain[my_tuple[0]].remove(i)
        revised = True
    return revised

# The arc-consistency algorithm AC-3. After applying AC-3, either every arc
# is arc-consistent, or some variable has an empty domain, indicating that the CSP cannot be
# solved. The name “AC-3” was used by the algorithm’s inventor (Mackworth, 1977) because
# it’s the third version developed in the paper.

def neighbours(x_i, x_j) :
    neighbour_list = x_variables.copy()
    neighbour_list.remove(x_i)
    neighbour_list.remove(x_j)
    return list(zip([x_i], neighbour_list))


print(arc_consistency3())
