from ._anvil_designer import ArticleViewTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ArticleEdit import ArticleEdit



class ArticleView(ArticleViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.

        self.slika = anvil.URLMedia(anvil.server.get_app_origin() + "/_/theme/av.png")
        self.init_components(**properties)
        # Any code you write here will run when the form opens
        self.set_event_handler("x-my-event", self.handle_my_event)
        

    def handle_my_event(self, **event_args):
        self.edit_article_button.enabled = False
        self.delete_article_button.enabled = False

    def edit_article_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Create a copy of the existing article from the Data Table        
        article_copy = dict(self.item)        
        if article_copy["tecaj"] is None:
            article_copy["tecaj"] = []
        upis_traje = True
        while upis_traje:
            save_clicked = alert(
                content=ArticleEdit(item=article_copy),
                title="Izmjena podataka",
                large=True,
                buttons=[("Čuvanje", True), ("Odustajanje", False)],
            )
            if save_clicked:
                anvil.server.call(
                        "update_article", self.item, article_copy
                    )
                upis_traje = False
                self.refresh_data_bindings()
               
            else:
                upis_traje = False

    def delete_article_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Get the user to confirm if they wish to delete the article
        # If yes, raise the 'x-delete-article' event on the parent
        # (which is the articles_panel on Homepage)

        result = alert(
            content=f"Jeste li sigurni da želite da izbrišete  {self.item['title']} {self.item['ime']} ?",
            buttons=[("Da", True), ("Ne", False)],
            role="alert-greska",
        )
        if result:
            self.parent.raise_event("x-delete-article", article=self.item)

    def vidljivost_tecaja(self, **event_args):

        if self.repeating_panel_1.visible:
            self.edit_article_button_copy.icon = "fa:angle-down"
            self.repeating_panel_1.visible = False
        else:
            self.edit_article_button_copy.icon = "fa:angle-up"
            self.repeating_panel_1.visible = True

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        pass
 
