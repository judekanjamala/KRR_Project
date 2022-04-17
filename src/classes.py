class Term():

    def __init__(self) -> None:

        self.is_constant = False
        self.is_variable = False
        self.is_compound = False


class ConstantTerm(Term):
    
    def __init__(self, val, is_integer=False):
       
        super().__init__()
        self.is_constant = True
        self.is_integer = is_integer
        if is_integer:
            val = int(val)
            
        self.val = val

    def __repr__(self) -> str:
        return f"ConstantTerm(val={self.val})"

class VariableTerm(Term):
    count = 0
    
    def __init__(self, name, clause=None):
    
        super().__init__()
        self.is_variable = True
        self.name = name
        self.clause = clause
        self.__class__.count += 1
        self.id = self.__class__.count
    
    def __repr__(self) -> str:
        return f"VariableTerm(name={self.name}, clause={self.clause}, id={self.id})"

class CompoundTerm(Term):
    
    def __init__(self, name, args):
        super().__init__()
        self.is_compound = True
        self.name = name
        self.args = args
        self.variables = set()

        for arg in args:
            if arg.is_variable:
                self.variables.add(arg)
            
            elif arg.is_compound:
                self.variables = self.variables.union(arg.variables)

    def __repr__(self) -> str:
        return f"CompoundTerm(name={self.name}, args={self.args})"
            
