
ITEMS_PER_PAGE = 3


def paginate(request,selection):
    page = request.args.get("page",1,type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return selection[start:end]  