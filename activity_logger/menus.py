from django.urls import reverse
from menu import Menu, MenuItem
from .urls import app_name

child_items = (
    MenuItem('Summary', reverse(f'{app_name}:summary-view')),
)

Menu.add_item(
    'main',
    MenuItem(
        'Actvity App',
        url=f'/{app_name}',
        children=child_items
    )
)
