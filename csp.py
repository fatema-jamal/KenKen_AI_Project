
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