from django.urls import reverse
from menu import Menu, MenuItem

bistro_menu_items = (
    MenuItem('Get Bistro', reverse('bistro:random_bistro')),
    MenuItem('Add Bistro', reverse('bistro:add_place')),
)

Menu.add_item(
    'main',
    MenuItem('Bistro App', url='#', children=bistro_menu_items)
)