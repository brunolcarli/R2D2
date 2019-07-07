'''
Defines the queries and mutations to be send as request to the
API
'''

def get_quote_mutation(message):
    '''
    Returns the mutation for creation a quote.
    param: message : <str> The input message to be saved on database.
    return: <str>
    '''
    part_1 = "{\"query\":\"mutation{\\n  createR2Quote(input:{\\n    quote: \\\" " 
    part_2 = "\\\"\\n  }){\\n    response\\n  }\\n}\"}"
    mutation = part_1 + message + part_2
    return mutation
