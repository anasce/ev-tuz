from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate5(ItemTemplate5Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.parent.raise_event("x-delete-tecaj", tecaj=self.item)
