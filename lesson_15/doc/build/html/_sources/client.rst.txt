Client module
=============

Clients's module.

Launch:
`python client.py localhost`

* arguments:
* -p - Number port. Default 7777

client.py
~~~~~~~~~~~~~~
Main client module

.. autoclass:: client.client.ClientVerifier
	:members:

.. autoclass:: client.client.processing_presence
	:members:

.. autoclass:: client.client.send_message
	:members:

.. autoclass:: client.client.processing_answer
	:members:

.. autoclass:: client.client.get_message
	:members:

.. autoclass:: client.client.Read
	:members:

.. autoclass:: client.client.Send
	:members:

client_db.py
~~~~~~~~~~~~~~

.. autoclass:: client.client_db.User
	:members:

.. autoclass:: client.client_db.UsersHistory
	:members:

.. autoclass:: client.client_db.add_users
	:members:

.. autoclass:: client.client_db.get_contact
	:members:

.. autoclass:: client.client_db.get_history
	:members:

main_window.py
~~~~~~~~~~~~~~

.. autoclass:: client.main_window.ClientMainWindow
	:members:
