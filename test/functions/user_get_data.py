'''
test function for getting user data
'''
from pprint import pprint
from test.functions.user_test_data import access
def get_user_data(user):
    return access

if __name__=='__main__':
    pprint(get_user_data('foo.bar'))
    