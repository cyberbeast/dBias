import json
import numpy as np

class Suite:
    def __init__(self, dataFrame, suiteName):
        self.dataFrame = dataFrame
        self.suiteName = suiteName
        self.queries = []
        self.resulSets = []
        
    def add_query(self, query, name="query"):
        assert type(query) == dict
        self.queries.append((query,name))
    
    def run(self):
        print ("Initiating Run for test suite",self.suiteName)
        for query,name in self.queries:
            print ("Testing query:",name)
            q = Query(name)
            conditions = query['conditions']
            active_features_json = {}
            for feature in self.dataFrame.columns:
                active_features_json[feature] = {'name':feature, 'hidden':True}

            for condition in conditions:
                feature = condition['feature']
                active_features_json[feature]['hidden'] = False

            resultSet, resultCount = q.lookup(self.dataFrame, query)
            resultSet = resultSet
            ## to_json returns a str
            ## need to convert to json using loads
            jsonOut = json.loads(resultSet.to_json(orient='split',default_handler=MyEncoder))
            jsonOut['resultCount'] = resultCount
            del jsonOut['columns']
            jsonOut['columns'] = list(active_features_json.values())
            
            yield jsonOut

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

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
        resultCount = int(np.bincount(resultMask)[1])
        return dataFrame[resultMask], resultCount