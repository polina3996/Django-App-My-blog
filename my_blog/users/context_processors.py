from stories import utils


def get_context(request):
    # a common dictionary that is available in ALL templates
    return {'mainmenu' : utils.menu}