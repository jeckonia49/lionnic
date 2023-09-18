""" Useage """
"""
    # Declare our item
    store = Store.objects.get(pk=pk)
    # Define our models
    stores = Store.objects.all()
    # Ask for the next item
    new_store = get_next_or_prev(stores, store, 'next')
    # If there is a next item
    if new_store:
        # Replace our item with the next one
        store = new_store
"""

""" Function """


def get_next_or_prev(models, item, direction):
    """
    Returns the next or previous item of
    a query-set for 'item'.

    'models' is a query-set containing all
    items of which 'item' is a part of.

    direction is 'next' or 'prev'

    """

    getit = False
    if direction == "prev":
        models = models.reverse()
    for m in models:
        if getit:
            return m
        if item == m:
            getit = True
    if getit:
        # This would happen when the last
        # item made getit True
        return models[0]
    return False
