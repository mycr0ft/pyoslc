from authlib.integrations.flask_oauth1 import AuthorizationServer
from authlib.oauth1 import TemporaryCredential

from pyoslc_oauth.database import db
from pyoslc_oauth.models import Client, cache, TokenCredential


def query_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


auth_server = AuthorizationServer(query_client=query_client)


def _create_exists_nonce_func(cache, key_prefix='nonce:', expires=86400):
    def exists_nonce(nonce, timestamp, client_id, oauth_token):
        key = key_prefix + nonce
        if cache.get(key):
            return True
        cache.set(key, True, timeout=expires)
        return False
    return exists_nonce


def _register_temporary_credential_hooks(auth_server, cache, key_prefix='temporary_credential:'):
    def create_temporary_credential(token, client_id, redirect_uri):
        key = key_prefix + token['oauth_token']
        token['client_id'] = client_id
        if redirect_uri:
            token['oauth_callback'] = redirect_uri
        cache.set(key, token, timeout=86400)
        return TemporaryCredential(token)

    def get_temporary_credential(oauth_token):
        if not oauth_token:
            return None
        key = key_prefix + oauth_token
        value = cache.get(key)
        if value:
            return TemporaryCredential(value)

    def delete_temporary_credential(oauth_token):
        if oauth_token:
            key = key_prefix + oauth_token
            cache.delete(key)

    def create_authorization_verifier(credential, grant_user, verifier):
        key = key_prefix + credential.get_oauth_token()
        credential['oauth_verifier'] = verifier
        credential['user_id'] = grant_user.get_user_id()
        cache.set(key, credential, timeout=86400)
        return credential

    auth_server.register_hook('create_temporary_credential', create_temporary_credential)
    auth_server.register_hook('get_temporary_credential', get_temporary_credential)
    auth_server.register_hook('delete_temporary_credential', delete_temporary_credential)
    auth_server.register_hook('create_authorization_verifier', create_authorization_verifier)


def _register_token_credential_hooks(auth_server):
    def create_token_credential(token, temporary_credential):
        item = TokenCredential(
            oauth_token=token['oauth_token'],
            oauth_token_secret=token['oauth_token_secret'],
            client_id=temporary_credential.get_client_id()
        )
        item.set_user_id(temporary_credential.get_user_id())
        db.session.add(item)
        db.session.commit()
        return item

    auth_server.register_hook('create_token_credential', create_token_credential)


def init_app(app):
    auth_server.init_app(app)
    auth_server.register_hook('exists_nonce', _create_exists_nonce_func(cache))
    _register_temporary_credential_hooks(auth_server, cache)
    _register_token_credential_hooks(auth_server)
