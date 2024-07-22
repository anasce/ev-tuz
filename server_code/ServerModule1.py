import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import anvil.email
import anvil.users
import anvil.server
from anvil.http import url_encode
import bcrypt
from random import SystemRandom
import anvil.pdf

random = SystemRandom()


def mk_token():
    """Generate a random 14-character token"""
    return "".join(
        [
            random.choice(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            )
            for i in range(14)
        ]
    )


@anvil.server.callable
def _send_password_reset(email):
    """Send a password reset email to the specified user"""
    user = app_tables.users.get(email=email)
    print(email)
    print(user)
    if user is not None:
        user["link_key"] = mk_token()
        anvil.users.send_password_reset_email(email)
        return True


@anvil.server.callable
def _send_email_confirm_link(email):
    """Send an email confirmation link if the specified user's email is not yet confirmed"""
    user = app_tables.users.get(email=email)
    if user is not None and not user["confirmed_email"]:
        if user["link_key"] is None:
            user["link_key"] = mk_token()
        anvil.email.send(
            to=user["email"],
            subject="Confirm your email address",
            text=f"""
Hi,

Thanks for signing up for our service. To complete your sign-up, click here to confirm your email address:

{anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&confirm={url_encode(user['link_key'])}

Thanks!
""",
        )
        return True


def hash_password(password, salt):
    """Hash the password using bcrypt in a way that is compatible with Python 2 and 3."""
    if not isinstance(password, bytes):
        password = password.encode()
    if not isinstance(salt, bytes):
        salt = salt.encode()
    result = bcrypt.hashpw(password, salt)
    if isinstance(result, bytes):
        return result.decode("utf-8")


@anvil.server.callable
def _do_signup(email, name, password):
    if name is None or name.strip() == "":
        return "Morate unijeti ime"
    pwhash = hash_password(password, bcrypt.gensalt())
    # Add the user in a transaction, to make sure there is only ever one user in this database
    # with this email address. The transaction might retry or abort, so wait until after it's
    # done before sending the email.

    @tables.in_transaction
    def add_user_if_missing():
        user = app_tables.users.get(email=email)
        if user is None:
            # user = app_tables.users.add_row(email=email, enabled=True, name=name, password_hash=pwhash)
            user = app_tables.users.add_row(
                email=email, enabled=False, name=name, password_hash=pwhash
            )
            return user

    user = add_user_if_missing()
    if user is None:
        return "Ova mail adresa je već registrovana u našem sistemu. Pokušajte da se prijavite."
    _send_email_confirm_link(email)
    # No error = success
    return None


def get_user_if_key_correct(email, link_key):
    user = app_tables.users.get(email=email)
    if user is not None and user["link_key"] is not None:
        # Use bcrypt to hash the link key and compare the hashed version.
        # The naive way (link_key == user['link_key']) would expose a timing vulnerability.
        salt = bcrypt.gensalt()
        if hash_password(link_key, salt) == hash_password(user["link_key"], salt):
            return user


@anvil.server.callable
def _is_password_key_correct(email, link_key):
    return get_user_if_key_correct(email, link_key) is not None


@anvil.server.callable
def _perform_password_reset(email, reset_key, new_password):
    """Perform a password reset if the key matches; return True if it did."""
    user = get_user_if_key_correct(email, reset_key)
    if user is not None:
        user["password_hash"] = hash_password(new_password, bcrypt.gensalt())
        user["link_key"] = None
        anvil.users.force_login(user)
        return True


@anvil.server.callable
def _confirm_email_address(email, confirm_key):
    """Confirm a user's email address if the key matches; return True if it did."""
    user = get_user_if_key_correct(email, confirm_key)
    if user is not None:
        user["confirmed_email"] = True
        user["link_key"] = None
        anvil.users.force_login(user)
        return True


@anvil.server.callable
def add_article(article_dict):
    app_tables.articles.add_row(created=datetime.now(), **article_dict)


@anvil.server.callable
def dodaj_tecaj(tecaj_t):
    app_tables.tecajevi.add_row(naziv=tecaj_t)


@anvil.server.callable
def get_articles():
    # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
    lista_а = list(
        app_tables.articles.search(tables.order_by("created", ascending=False))
    )
    lista_а_p = []
    br = 1
    for art in lista_а:
        if br <= 11:
            lista_а_p.append(art)
            br = br + 1
    return lista_а_p


@anvil.server.callable
def update_article(article, article_dict):
    # check that the article given is really a row in the ‘articles’ table
    if app_tables.articles.has_row(article):
        article_dict["updated"] = datetime.now()
        article.update(**article_dict)
    else:
        raise Exception("Article does not exist")


@anvil.server.callable
def delete_article(article):
    # check that the article being deleted exists in the Data Table
    if app_tables.articles.has_row(article):
        article.delete()
    else:
        raise Exception("Article does not exist")


@anvil.server.callable
def duplikat_a(pr, im):
    people_called_dave = app_tables.articles.get(title=pr, ime=im)
    return people_called_dave


@anvil.server.callable
def rola_k():
    if anvil.users.get_user()["role"] == "citac":
        return True
    else:
        return False


@anvil.server.callable
def prazna_kat():
    return app_tables.categories.get(name="")


@anvil.server.callable
def import_podataka(art_dict):
    org_jed_za_dave = app_tables.categories.get(name=art_dict["category"])
    art_dict["category"] = org_jed_za_dave
    art_dict["created"] = datetime.now()
    app_tables.articles.add_row(**art_dict)


@anvil.server.callable
def e_pretrage_f():
    org_jed_p = [(cat["name"], cat) for cat in app_tables.categories.search()]
    tecajevi_p = [(cat["naziv"], cat) for cat in app_tables.tecajevi.search()]
    return org_jed_p, tecajevi_p


@anvil.server.callable
def search_records(search_string):
    search_string = search_string.lower()
    return [
        r
        for r in app_tables.articles.search(tables.order_by("created", ascending=False))
        if search_string in r["title"].lower()
    ]
