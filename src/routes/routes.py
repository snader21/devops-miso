from src.resources.black_list_resource import BlackListResource


def add_resources(api):
    api.add_resource(BlackListResource, '/blacklists',
                     '/blacklists/<string:email>')
