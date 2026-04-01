Cryptographic assets
====================

The Cryptnox Hardware Wallet card manages several cryptographic assets throughout its
lifecycle. This section provides an overview of all key material, credentials, and
derived secrets handled by the card.

.. raw:: html

   <style>
     .wy-table-responsive table td { white-space: normal !important; }
   </style>

----

Factory Dual Basic Group Secret
-------------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Secure Element (factory-loaded)
   * - **Description**
     - EC secret used for the dual generation protocol and to sign public material
       exchanged between paired cards. Protects the integrity of the dual-gen exchange.
   * - **Notes**
     - Loaded at factory; used in dual generation signatures.

----

Card long-term attestation key
------------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Secure Element (card keypair)
   * - **Description**
     - Card's permanent EC keypair (R1) used to sign the card certificate and
       authenticate ephemeral session keys.
   * - **Notes**
     - Readable only as the certificate via ``GET MANUFACTURER CERTIFICATE`` /
       ``GET CARD CERTIFICATE``.

----

Session ephemeral private key
-----------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Secure Element (ephemeral, per session)
   * - **Description**
     - Short-lived EC private key generated inside the card and used for ECDH in the
       secure channel. Never exported.
   * - **Notes**
     - Exposed externally only as the card's ephemeral public key inside the basic
       card certificate (``GET CARD CERTIFICATE``).

----

Pairing key
-----------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Card secure storage (32 bytes)
   * - **Description**
     - The 32-byte secret used to derive AES/MAC session keys with a host for the
       authenticated secure channel. There is one pairing key slot; can be public if
       desired but normally kept secret.
   * - **Notes**
     - Set at ``INIT``; used in ``OPEN SECURE CHANNEL`` key derivation; changeable
       with ``CHANGE PAIRING KEY``. Fallback: a PUK-derived pairing key
       (SHA-256\ :sup:`32` of PUK) can be used (index ``0xFF``).

----

Secure Channel session keys (AES / MAC)
---------------------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Volatile (session only)
   * - **Description**
     - Keys derived from ECDH(SessionCardPriv, SessionUserPub) || PairingKey ||
       SessionSalt via SHA-512, split into AES and MAC keys. Protect confidentiality
       and integrity of APDUs while the channel is open.
   * - **Notes**
     - Derived during ``OPEN SECURE CHANNEL``. Not persistent.

----

PIN
---

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Card secure storage
   * - **Description**
     - User numeric PIN (4--9 digits) used to authenticate the user for most protected
       operations. PIN verification state is session-valid until a signature or
       deselect/power-off.
   * - **Notes**
     - ``INIT``, ``VERIFY PIN``, ``CHANGE PIN``, ``UNBLOCK PIN``. Retry counters and
       power-cycle rules apply.

----

PUK
---

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Card secure storage (12 bytes)
   * - **Description**
     - Card reset/unblock secret. Used to unblock PIN, authorize PUK-protected changes
       (e.g., change pairing key, set pinless path, set pub export), and perform
       ``RESET``.
   * - **Notes**
     - ``INIT``, ``RESET``, ``CHANGE PAIRING KEY``, ``SET PIN AUTH``. Unlimited
       attempts but throttled with power-cycle behavior.

----

PUK-derived pairing fallback
-----------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Derived (fallback)
   * - **Description**
     - Deterministic pairing key obtained by hashing the PUK 32 times with SHA-256;
       usable as pairing key index ``0xFF`` if pairing information is lost.
   * - **Notes**
     - Used via ``OPEN SECURE CHANNEL`` with ``P1=0xFF``.

----

User private keys (off-card)
----------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Host device (e.g., TPM / Secure Enclave)
   * - **Description**
     - Private keys kept on a host device used to perform challenge-response
       authentication against the card. The card stores only the corresponding public
       key. These act as PIN replacements.
   * - **Notes**
     - Card stores public keys in slots via ``ADD USER KEY``; verification via
       ``CHECK USER KEY``. Private keys must be protected by the host.

----

FIDO credential (slot 3)
------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Card slot (credential ID + public key)
   * - **Description**
     - FIDO credential identifier and associated EC public key. Used to verify
       WebAuthn-style signatures for PIN replacement or signing authorization.
   * - **Notes**
     - ``ADD USER KEY`` (slot 3) stores credential ID length, credential ID, EC
       public key, and PUK. Verified via ``CHECK USER KEY``.

----

Pinless path derivation settings
--------------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Card secure storage
   * - **Description**
     - The BIP32 derivation path used for PIN-less signing (e.g.,
       ``m/43'/60'/1581'/...``); guarded by PUK to set/unset. Enables transactions
       without PIN when used via the pinless ``SIGN`` mode.
   * - **Notes**
     - ``SET PINLESS PATH`` with PUK. Pinless signing via ``SIGN`` with ``P1=0x03``.

----

Dual-generation partial secrets
-------------------------------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Secure Element (temporary during dual-gen)
   * - **Description**
     - During the dual-generation protocol, two cards each generate a partial secret
       and exchange signed public material to produce a shared seed
       (SHA-256(ECDH)). Each card stores its part; the final shared seed becomes the
       card seed.
   * - **Notes**
     - ``LOAD KEY`` with ``P1=0x04`` / ``P1=0x05`` sequence. Signature checks use the
       Basic Group Secret.

----

Master seed
-----------

.. list-table::
   :widths: 20 80

   * - **Scope**
     - Secure Element (non-exportable)
   * - **Description**
     - The 256-bit master seed (BIP32 / SLIP-0010) -- the root of all derived
       blockchain keys. From this single seed, three independent key hierarchies are
       derived: secp256k1 (Bitcoin, Ethereum), secp256r1 (FIDO, secure messaging),
       and EdDSA (Ed25519, Solana, Cardano). This is the ultimate cryptographic asset:
       it cannot be read or exported, only destroyed via ``RESET`` with PUK.
   * - **Notes**
     - Generated on-card (``GENERATE KEY``) or loaded (``LOAD KEY`` with
       ``P1=0x03``). Once set, it cannot be changed except by ``RESET`` with PUK.

----

.. important::

   All cryptographic assets stored in the Secure Element are strictly non-exportable.
   Private keys and seeds never leave the card boundary. Recovery is only possible
   through dual-generated backup cards or re-importing an externally held seed.
