
from collections import defaultdict
from functools import reduce
import itertools
import re
import random


class CSP():
    def __init__(self, variables, domains, neighbors, constraints):

        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):

        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):

        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):

        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))

        return count(conflict(v) for v in self.neighbors[var])

    def actions(self, state):

        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    

    def prune(self, var, value, removals):

        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def support_pruning(self):

        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):

        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals



    def choices(self, var):

        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):

        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):

        for B, b in removals:
            self.curr_domains[B].append(b)



    def conflicted_vars(self, current):

        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]
 def count(seq):
    return sum(bool(x) for x in seq)
    
def first(iterable, default=None):
    """Return the first element of an iterable or the next element of a generator; or default."""
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def AC3(csp, queue=None, removals=None):
    if queue is None:
        for i in csp.variables:
            for k in csp.neighbors[i]:
                queue.append((i,k))

    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if remove_inconsistent_values(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


def remove_inconsistent_values(csp, Xi, Xj, removals):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

# ______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering


def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])




def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0
                     for val in csp.domains[var])

# Value ordering


def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))

# Inference


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                #lw msh bt72a2 elconstrains htreturn true
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
   
    return True


def mac(csp, var, value, assignment, removals):
    """Maintain arc consistency."""
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)

# The search, proper

count_t=0
def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    global  count_t
    count_t=0
    def backtrack(assignment):
        
        global  count_t
        
        #base condition
        if len(assignment) == len(csp.variables):
            return assignment
        #variable selecting by heuristic 
        var = select_unassigned_variable(assignment, csp)
        #domain ordering heuristic
        for value in order_domain_values(var, assignment, csp):
            # check if there are no conflicts
            if  csp.nconflicts(var, value, assignment) == 0:
                #assign var, and update assignment set
                csp.assign(var, value, assignment)
                
                #keep track of removed assignments in case we want to backtrack
                removals = csp.suppose(var, value)
                #recursion
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    count_t+=1
                    #eldenyaa tamaaaaaaam
                
                    if result is not None:
                        return result
                #eldenya msh tmam (conflicts)
                # restore removals        
                csp.restore(removals)
                
        #unassign last assignment (hwa da elbacktrack b3eno)        
        csp.unassign(var, assignment)
        print('mn gher', count_t)
        return None
    #initially assignment set is empty
    result = backtrack({})
    assert result is None or csp.goal_test(result)
    print('result', result)
    return result
