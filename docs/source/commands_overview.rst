Command overview
================

The following table provides a summary of all APDU commands supported by the Cryptnox
Hardware Wallet card, along with their authentication and security requirements.

.. raw:: html

   <style>
     .wy-table-responsive table td { white-space: normal !important; }
   </style>

Application & info
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - SELECT
     - Selects the Cryptnox applet.
     - ✗
     - ✗
     - ✗
   * - Get Card Public Key
     - Retrieves the card factory EC public key.
     - ✗
     - ✗
     - ✗
   * - Get Manufacturer Certificate
     - Reads Cryptnox X509 manufacturer certificate (paged).
     - ✗
     - ✗
     - ✗
   * - Get Card Certificate
     - Retrieves ephemeral session certificate (for secure channel setup).
     - ✗
     - ✗
     - ✗

Initialization
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - INIT
     - Initializes card with PIN, PUK, and pairing key.
     - ✓ One-shot
     - ✗
     - ✓ Set initial
   * - Open Secure Channel
     - Establishes Secure Channel with pairing key.
     - ✗
     - ✗
     - ``0xFF`` fallback
   * - Mutually Authenticate
     - Confirms Secure Channel integrity with challenge/response.
     - ✗
     - ✗
     - ✗
   * - Change Pairing Key
     - Updates Secure Channel pairing key.
     - ✓
     - ✗
     - ✗

User authentication
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - Verify PIN
     - Verifies user PIN, unlocks card for session.
     - ✓
     - ✓ PIN
     - ✗
   * - Change PIN / PUK
     - Changes PIN or PUK.
     - ✓
     - ✓ PIN or PUK
     - ✓ To change PUK
   * - Unblock PIN
     - Unblocks PIN with PUK and new PIN.
     - ✓
     - ✗
     - ✓
   * - Add User Key
     - Stores external user public key (ECDSA, RSA, FIDO).
     - ✓
     - ✓ PIN / User Key
     - ✓ If PIN disabled
   * - Check User Key
     - Performs challenge-response authentication using user key.
     - ✓
     - ✓ User Key sig
     - ✗
   * - Delete User Key
     - Deletes a registered user key slot.
     - ✓
     - ✗
     - ✓
   * - Set Pin Auth
     - Enables/disables PIN auth (forces User Key only).
     - ✓
     - ✗
     - ✓

Key management
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - Load Key
     - Loads seed, keypair, or performs dual seed generation.
     - ✓
     - ✓
     - ✗
   * - Generate Key
     - Generates new seed internally.
     - ✓
     - ✓
     - ✗
   * - Set Pinless Path
     - Configures EIP-1581 pinless derivation path.
     - ✓
     - ✗
     - ✓
   * - Set Pub Export
     - Enables xpub or clear pubkey output.
     - ✓
     - ✗
     - ✓
   * - Get Public Key
     - Reads current or derived public key, xpub.
     - ✓ Except pinless
     - ✓ Except pinless
     - ✗
   * - Derive Key
     - Derives new key pair from seed (BIP32 / SLIP-0010).
     - ✓
     - ✓
     - ✗
   * - Generate TRNG Random
     - Outputs random data (16--64 bytes).
     - ✓
     - ✗
     - ✗

Signing & decryption
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - Sign
     - Signs hash (ECDSA / Schnorr).
     - ✓ Except pinless
     - ✓ Except pinless
     - ✗
   * - Decrypt
     - ECIES-like decryption / symmetric key output.
     - ✓
     - ✓
     - ✗

Data & history
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - Get Card Info / Read Data
     - Reads owner info, key source, counters, user slot info.
     - ✓
     - ✓ Protected slots
     - ✗
   * - Get History
     - Reads signing history slots.
     - ✓
     - ✓
     - ✗
   * - Write Data
     - Writes user data slot or custom bytes.
     - ✓
     - ✓
     - ✗

Administration
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 13 13 14

   * - Command
     - Description
     - Secure Channel
     - PIN / User Key
     - PUK
   * - Reset
     - Full factory reset of the card.
     - ✓
     - ✗
     - ✓
   * - Disable Reset
     - Permanently disables reset capability.
     - ✓
     - ✗
     - ✓

.. note::

   For detailed APDU specifications, parameters, and response codes of each command,
   refer to the dedicated command pages:
   :doc:`commands_setup`, :doc:`commands_crypto`, :doc:`commands_data`, and
   :doc:`commands_user_keys`.
