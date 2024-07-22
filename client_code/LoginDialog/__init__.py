from ._anvil_designer import LoginDialogTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import login_flow

class LoginDialog(LoginDialogTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.

  def confirm_lnk_click (self, **event_args):
    """Close any alert we might be in with 'confirm_email' value."""
    self.raise_event('x-close-alert', value='confirm_email')

  def reset_pw_link_click (self, **event_args):
    """Close any alert we might be in with 'reset_password' value."""
    self.raise_event('x-close-alert', value='reset_password')
    
  def focus_password(self, **kws):
     """Focus on the password box."""
     self.password_box.focus()

  def close_alert(self, **kws):
     """Close any alert we might be in with 'login' value."""
     self.raise_event('x-close-alert', value='login')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    #anvil.users.login_with_form()
    anvil.users.send_password_reset_email("anash@t-com.me")
    anvil.users.send_password_reset_email("ana.scepanovic57@gmail.com")

  def fok(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.email_box.focus()

  def reset_pw_link_click_copy(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.login_with_form()

  def signup_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def reset_pw_link_click_r(self, **event_args):
    """This method is called when the link is clicked"""
    login_flow.signup_with_form()




