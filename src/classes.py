class Term():

    def __init__(self) -> None:

        self.is_constant = False
        self.is_variable = False
        self.is_compound = False


class ConstantTerm(Term):
    
    def __init__(self, val):
       
        super().__init__()
        self.is_constant = True
            
        self.val = val

    def __str__(self) -> str:
        return f"{self.val}"

    def __repr__(self) -> str:
        return f"ConstantTerm(val={self.val})"
    
    def __hash__(self):
        return hash((self.val,))

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

class VariableTerm(Term):
    count = 0
    
    def __init__(self, name, clause=None):
    
        super().__init__()
        self.is_variable = True
        self.name = name
        self.clause = clause
        self.__class__.count += 1
        self.id = self.__class__.count

    def __str__(self) -> str:
        return f"{self.name}{self.id}"
    
    def __repr__(self) -> str:
        return f"VariableTerm(name={self.name}, clause={self.clause})"

    def __hash__(self):
        return hash((self.name, self.clause, self.id))

    def __eq__(self, other):
        return (self.name, self.clause, self.id) == (other.name, other.clause, other.id)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

class CompoundTerm(Term):
    
    def __init__(self, name, args):
        super().__init__()
        self.is_compound = True
        self.is_predicate = False
        self.is_function = False
        self.name = name
        self.args = tuple(args)
        self.variables = set()

        for arg in args:
            if arg.is_variable:
                self.variables.add(arg)
            
            elif arg.is_compound:
                self.variables = self.variables.union(arg.variables)

    def __str__(self) -> str:
        args = f""
        for arg in self.args:
            args += f"{arg}, "
        return f"{self.name}({args[:-2]})"

    def __repr__(self) -> str:
        return f"CompoundTerm(name={self.name}, args={self.args})"
            
    def __hash__(self):
        return hash((self.name, self.args))

    def __eq__(self, other):
        return (self.name, self.args) == (other.name, other.args)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

class FunctionTerm(CompoundTerm):

    def __init__(self, name, args):
        super().__init__(name, args)

        self.is_function = True

    def __repr__(self) -> str:
        return f"FunctionTerm(name={self.name}, args={self.args})"


class PredicateTerm(CompoundTerm):

    def __init__(self, name, args):
        super().__init__(name, args)

        self.is_predicate = True

    def __repr__(self) -> str:
        return f"PredicateTerm(name={self.name}, args={self.args})"
