from ._anvil_designer import ArticleEditTemplate
from anvil import *
import anvil.users
import anvil.server
from anvil.tables import app_tables



class ArticleEdit(ArticleEditTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.slika = anvil.URLMedia(anvil.server.get_app_origin() + "/_/theme/av.png")
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        otl=anvil.server.call("e_pretrage_f")
        self.categories = otl[0]
        self.category_box.items = self.categories        
        self.tecaj = otl[1]
        self.drop_down_tecajevi.items = self.tecaj
        self.repeating_panel_tecajevi.set_event_handler(
            "x-delete-tecaj", self.brisi_tecaj
        )

    def image_uploader_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        self.item["image"] = file
        self.refresh_data_bindings()

    def dodaj_tecaj_dugme_click_bb(self, **event_args):
        niz = self.item["tecaj"]
        niz.append(self.drop_down_tecajevi.selected_value)
        self.refresh_data_bindings()

    def brisi_tecaj(self, tecaj, **event_args):
        niz = self.item["tecaj"]
        niz = niz.remove(tecaj)
        self.refresh_data_bindings()

    def vidljivost_tecaja_e(self, **event_args):
        if self.repeating_panel_tecajevi.visible:
            self.edit_article_button_copy.icon = "fa:angle-down"
            self.repeating_panel_tecajevi.visible = False
            self.flow_panel_1.visible = False
        else:
            self.edit_article_button_copy.icon = "fa:angle-up"
            self.repeating_panel_tecajevi.visible = True
            self.flow_panel_1.visible = True

    def drop_down_tecajevi_change(self, **event_args):
        
        niz = self.item["tecaj"]
        niz.append(self.drop_down_tecajevi.selected_value)
        self.refresh_data_bindings()

    def title_box_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def title_box_focus(self, **event_args):
      """This method is called when the TextBox gets focus alalaltra"""
      pass
  

  

 
