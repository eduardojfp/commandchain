__author__ = 'awhite'

from chain_of_command.models import Order, Post, Position


def get_orders_for_Position(position, showold=False):
    """
    Get orders relevant to a position
    :param position: the position in question
    :param showold: whether or not to show the orders whose deadlines have
    already passed
    :return: a list of orders
    """
    from datetime import datetime

    orders = []
    i = position
    while i is not None:
        for c in position.order_set.all():
            if c.Deadline > datetime.now() or showold:
                orders.append(c)
        i = i.Boss
        if i.Percolates == False:
            break
    return orders

