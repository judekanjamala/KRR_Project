class Term():

    def __init__(self) -> None:

        self.is_constant = False
        self.is_variable = False
        self.is_compound = False


class ConstantTerm(Term):
    
    def __init__(self, val) -> None:
       
        super().__init__()
        self.is_constant = True
        self.val = val

    def __repr__(self) -> str:
        return f"ConstantTerm(val={self.val})"

class VariableTerm(Term):
    count = 0
    
    def __init__(self, name, clause_num=None) -> None:
    
        super().__init__()
        self.is_variable = True
        self.name = name
        self.clause_num = clause_num
        self.__class__.count += 1
        self.id = self.__class__.count
    
    def __repr__(self) -> str:
        return f"VariableTerm(name={self.name}, clause_num={self.clause_num}, id={self.id})"

class CompoundTerm(Term):
    
    def __init__(self, name, args) -> None:
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
            
