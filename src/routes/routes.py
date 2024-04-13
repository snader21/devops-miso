from src.resources.black_list_resource import BlackListResource, BlackListHealthResource


def add_resources(api):
    api.add_resource(BlackListResource, '/blacklists',
                     '/blacklists/<string:email>')
    api.add_resource(BlackListHealthResource, '/blacklists/ping')
