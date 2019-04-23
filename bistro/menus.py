from django.urls import reverse
from menu import Menu, MenuItem
from .urls import app_name

child_items = (
    MenuItem('Get Bistro', reverse(f'{app_name}:random_bistro')),
    MenuItem('Add Bistro', reverse(f'{app_name}:add_place')),
)

Menu.add_item(
    'main',
    MenuItem('Bistro App', url=f'/{app_name}', children=child_items)
)
