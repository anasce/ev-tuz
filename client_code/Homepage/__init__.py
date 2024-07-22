from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ArticleEdit import ArticleEdit
from .. import login_flow
import anvil.media


class Homepage(HomepageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        # Brisanje čitave tabele Articles, potrebno promijeniti prava korisnika
        # app_tables.articles.delete_all_rows()
        # app_tables.categories.delete_all_rows()
        self.refresh_articles()
        # Set an event handler on the RepeatingPanel (our 'articles_panel')
        self.articles_panel.set_event_handler("x-delete-article", self.delete_article)
        login_flow.login_with_form()        
        if anvil.server.call("rola_k"):
            self.add_article_button.enabled = False
            self.tecaj_button.enabled = False
            self.articles_panel.raise_event_on_children("x-my-event")
        self.cat=None
 

    def add_article_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Initialise an empty dictionary to store the user inputs
        if self.cat is None:
             self.cat=anvil.server.call("prazna_kat")
        new_article = {
            "title": "",
            "ime": "",
            "tecaj": [],
            "category": self.cat,
        }
        # Open an alert displaying the 'ArticleEdit' Form
        upis_traje = True
        while upis_traje:
            save_clicked = alert(
                content=ArticleEdit(item=new_article),
                title="Dodavanje podataka",
                large=True,
                buttons=[("Čuvanje", True), ("Odustajanje", False)],
            )
            # If the alert returned 'True', the save button was clicked.
 
            if save_clicked:
                
                    upis_traje = False
                    anvil.server.call(
                        "add_article", new_article
                    )
                    self.refresh_articles()
        
            else:
                upis_traje = False

    def refresh_articles(self):
        # Load existing articles from the Data Table,
        # and display them in the RepeatingPanel
        self.articles_panel.items = anvil.server.call("get_articles")

    def delete_article(self, article, **event_args):
        # Delete the article
        anvil.server.call("delete_article", article)
        self.refresh_articles()

   

    def dodaj_tecaj_dugme(self, **event_args):
        """This method is called when the button is clicked"""
        # Initialise an empty dictionary to store the user inputs
        # Open an alert displaying the 'ArticleEdit' Form
        t = TextBox(placeholder=" ")
        alert(
            content=t, title="Unesite novi tečaj", large=True, buttons=["U redu", True]
        )
        print(f"You entered: {t.text}")
        anvil.server.call("dodaj_tecaj", t.text)

    def error_handler(self):
        r = alert(
            str(self), title="Greška", buttons=["U redu", True], role="alert-greska"
        )

    set_default_error_handling(error_handler)

    def pret(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('Form1')

    def pret_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      #alert(self.text_box_pret.text)
      lista_pret=[]
      lista_pret=anvil.server.call("search_records",self.text_box_pret.text)
      self.articles_panel.items=lista_pret

      
    def pdf_download(self, **event_args):
      """This method is called when the button is clicked"""
      
      lista_pdf=self.articles_panel.items
      ls=[]
      for lp in lista_pdf:
           
           lpt=lp["tecaj"]
           lt=[] 
           if lpt is not None:
              
              for tp in lpt:
                 lt.append(tp["naziv"])
           lp1=[lp["title"],lp["image"],lp["ime"],lp["category"]["name"],lt]
           ls.append(lp1)
      #alert(ls)  
      c=anvil.server.call("pdf_article",ls)
      anvil.media.download(c)
  

