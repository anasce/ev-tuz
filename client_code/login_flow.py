from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


from LoginDialog import LoginDialog
from SignupDialog import SignupDialog
from ForgottenPasswordDialog import ForgottenPasswordDialog
from PasswordResetDialog import PasswordResetDialog


def login_with_form(allow_cancel=False):
  """Log in by popping up the custom LoginDialog"""
  d = LoginDialog()

  BUTTONS = [("Prijava", "login", "primary")]
  if allow_cancel:
    BUTTONS += [("Odustajanje", None)]
  
  while anvil.users.get_user() is None:
    choice = alert(d, title="Prijava", dismissible=allow_cancel, buttons=BUTTONS)
    
    if choice == 'login':
      try:
        anvil.users.login_with_email(d.email_box.text, d.password_box.text, remember=True)
      except anvil.users.EmailNotConfirmed:
        d.confirm_lnk.visible = True
      except anvil.users.AuthenticationFailed as e:
        if str(e.args[0]) == "Incorrect email address or password":
            d.login_err_lbl.text = "El pošta ili šifra nisu u redu "
        elif str(e.args[0]) == "This account has not been enabled by an administrator":
            d.login_err_lbl.text = "Ovaj korisnički nalog nije odobren za korišćenje"
        else:  
            d.login_err_lbl.text = str(e.args[0])
        #This account has not been enabled by an administrator
        #d.login_err_lbl.text = "Ел пошта или шифра нису "
        d.login_err_lbl.visible = True
        
    elif choice == 'reset_password':
      fp = ForgottenPasswordDialog(d.email_box.text)
      
      if alert(fp, title='Zaboravljena šifra', buttons=[("Promjena šifre", True, "primary"), ("Odustajanje", False)]):
        
        if anvil.server.call('_send_password_reset', fp.email_box.text):
        ##alert(fp.email_box.text)
        ##if True:
        #if anvil.users.send_password_reset_email("ana.scepanovic57@gmail.com"):
        #if anvil.users.send_password_reset_email("anash@t-com.me"):
          #anvil.users.send_password_reset_email("abc@example.com")
          alert(f"Mail za resetovanje šifre je poslan na {fp.email_box.text}.")
        else:
          alert("To korisničko ime ne postoji u našoj evidenciji.")
        
    elif choice == 'confirm_email':
      if anvil.server.call('_send_email_confirm_link', d.email_box.text):
        alert(f"Novi mail za potvrdu je poslan na {d.email_box.text}.")
      else:
        alert(f"'{d.email_box.text}' nije nepotvrđen mail nalog.")
      d.confirm_lnk.visible = False
    
    elif choice is None and allow_cancel:
      break

      
def signup_with_form():
  d = SignupDialog()

  while True:
    if not alert(d, title="Registracija", buttons=[("Registrovanje", True, 'primary'), ("Odustajanje", False)]):
      return
    
    if d.password_box.text != d.password_repeat_box.text:
      d.signup_err_lbl.text = 'Šifre se ne poklapaju. Pokušajte ponovo.'
      d.signup_err_lbl.visible = True
      continue
    
    err = anvil.server.call('_do_signup', d.email_box.text, d.name_box.text, d.password_box.text)
    if err is not None:
      d.signup_err_lbl.text = err
      d.signup_err_lbl.visible = True
    else:
      alert(f"1111111Poslali smo mail za potvrdu na {d.email_box.text}.\n\nProvjerite svoj mail i kliknite na link.")
      return
  
    
def do_email_confirm_or_reset():
  """Check whether the user has arrived from an email-confirmation link or a password reset, and pop up any necessary dialogs.
     Call this function from the 'show' event on your startup form.
  """
  h = anvil.get_url_hash()
  if isinstance(h, dict) and 'email' in h:
    if 'pwreset' in h:
      if not anvil.server.call('_is_password_key_correct', h['email'], h['pwreset']):
        alert("Ovo nije valjan link za potvrdu šifre")
        return

      while True:
        pwr = PasswordResetDialog()
        if not alert(pwr, title="Promijenite Vašu šifru", buttons=[("Reset password", True, 'primary'), ("Cancel", False)]):
          return
        if pwr.pw_box.text != pwr.pw_repeat_box.text:
          alert("Šifre se ne poklapaju. Pokušajte ponovo.")
        else:
          break
  
      if anvil.server.call('_perform_password_reset', h['email'], h['pwreset'], pwr.pw_box.text):
        alert("Vaša šifra je promijenjena. Prijavljeni ste.")
      else:
        alert("Ovo nije valjan link za potvrdu šifre")

        
    elif 'confirm' in h:
      if anvil.server.call('_confirm_email_address', h['email'], h['confirm']):
        alert("Hvala što ste potvrditi vašu mail adresu. Sada ste prijavljeni..")
      else:
        alert("Ovaj link za potvrdu nije valjan. Možda ste već potvrdili Vašu mail adresu?\n\nPokušajte normalno da se prijavite..")
 
     
  