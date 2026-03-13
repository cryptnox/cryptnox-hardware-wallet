================================
Cryptnox Product Documentation
================================

.. toctree::
   :maxdepth: 3
   :caption: CONTENTS


Cryptnox Hardware Wallet card Wallet
=========================

*Cryptnox Hardware Wallet card Wallet* is a JavaCard Open Platform 3 smartcard with an EAL6+ Common Criteria
certified secure element. It provides Hardware Wallet card-secured private key storage and transaction signing
for cryptocurrency applications over NFC and contact (T=1) interfaces.

All communication is protected by a secure channel based on GlobalPlatform SCP03, ensuring
confidentiality, authentication, and integrity. The card supports SECP256k1 and SECP256r1 curves
with ECDSA and BIP340 Schnorr signing, BIP32/SLIP10 hierarchical key derivation, and multiple
authentication methods including PIN, user key challenge-response, and FIDO.

* **Hardware Wallet card Wallet Technical Reference** [`HTML <./Hardware Wallet card-wallet/index.html>`_]


-------------------------


Cryptnox CLI
=============

*Cryptnox CLI* is a command-line tool for interacting with Cryptnox smartcards from the terminal.
It handles card initialization, secure channel establishment, PIN management, seed generation,
key derivation, and transaction signing through a straightforward command interface.

* **Cryptnox CLI User Guide** [`HTML <./cryptnox-cli/index.html>`_]


-------------------------


Cryptnox SDK for Python
=========================

*Cryptnox SDK for Python* is a library that enables developers to integrate Cryptnox smartcard
functionality into their own applications. It provides programmatic access to secure channel
establishment, APDU communication, key derivation, and signing operations, allowing custom
wallet software and automation workflows to leverage the card's Hardware Wallet card security.

* **Cryptnox SDK for Python** [`HTML <./cryptnox-sdk-py/index.html>`_]


-------------------------


Other resources
===============

* `Cryptnox Website <https://www.cryptnox.com>`_
* `Cryptnox on GitHub <https://github.com/nicokempe>`_
