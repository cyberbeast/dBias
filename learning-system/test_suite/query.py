class Query:
    
    def __init__(self, queryName):
        self.queryName = queryName

    def mask(self, feature, value, operation='eq'):
        operationsDict = {
            'eq': feature == value,
            'lt': feature < value,
            'gt': feature > value,
            'neq': feature != value,
            'gte': feature >= value,
            'lte': feature <= value
        }
        resultMask = operationsDict[operation]
        return resultMask
    
    def lookup(self, dataFrame, query_params):

        self.conjunctions = query_params['conjunctions']        
        self.conditions = query_params['conditions']
        
        assert len(self.conjunctions) == len(self.conditions) - 1, "Mismatch in conditions and conjunctions"

        resultMask = np.ones((len(dataFrame),),dtype=bool)
        conjunctions = [c for c in self.conjunctions]
        
        # adding True mask and dummy 'and'
        conjunctions.insert(0, 'and')
        
        for condition, conjunction in zip(self.conditions, conjunctions):
            feature, value, operation = condition['feature'], condition['value'], condition['operation']
            feature = dataFrame[feature]
            currentMask = self.mask(feature, value, operation)
            if conjunction == 'and':
                resultMask &= currentMask
            elif conjunction == 'or':
                resultMask |= currentMask
        
        return dataFrame[resultMask], np.bincount(resultMask)[1]