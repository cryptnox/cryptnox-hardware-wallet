MuSig2 commands (BIP-327)
=========================

The card implements the on-card half of the BIP-327 MuSig2 multi-signature protocol. MuSig2
produces a single Schnorr (BIP-340) signature that is indistinguishable from a non-MuSig
signature on-chain, while requiring two communication rounds between cosigners. The card acts
as one of the cosigners holding its share of the aggregate private key; key aggregation, nonce
aggregation and the host-side Taproot tweak are performed off-card.

The protocol uses three commands run in sequence:

1. :ref:`NONCE GEN <cmd-musig2-nonce-gen>` (INS 0xC7) — the card generates its own pair of
   secret nonces ``(k1, k2)`` and returns the matching public pair ``(R1, R2)``.
2. :ref:`LOAD COSIGNER KEY <cmd-musig2-load-cosigner>` (INS 0xC8 P1=01) — the host sends each
   cosigner public key (including the card's own) so the card can build the KeyAgg list hash
   ``L`` incrementally.
3. :ref:`PARTIAL SIGN <cmd-musig2-partial-sign>` (INS 0xC8 P1=02) — the host sends the
   aggregate nonce ``(aggR1, aggR2)``, the aggregate public key ``Q``, and the message hash.
   The card returns its 32-byte partial signature.

.. note::

   The card is curve-fixed on secp256k1 for MuSig2. Only the wallet's k1 key (or the pinless
   k1 key if applicable) is usable as the signing key. The card never aggregates the partial
   signatures itself --- aggregation is the host's responsibility.

**Protocol state machine**

The card enforces the protocol order with an internal state machine. Calls outside the
expected sequence are rejected with ``0x6985``.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - State
     - Set by
     - Accepts
   * - IDLE
     - Card reset, after PARTIAL SIGN, after rejected PARTIAL SIGN
     - NONCE GEN
   * - NONCE_GENERATED
     - Successful NONCE GEN
     - LOAD COSIGNER KEY, NONCE GEN (restarts)
   * - WAIT_COSIGNERS
     - First successful LOAD COSIGNER KEY
     - LOAD COSIGNER KEY (more), PARTIAL SIGN

After an applet deselect between LOAD COSIGNER KEY and PARTIAL SIGN, the card auto-demotes
back to NONCE_GENERATED so the host can resend the cosigner list. The secret nonces
``k1, k2`` and the card's own public key snapshot survive the deselect, so NONCE GEN does
not need to be re-issued.

----

.. _cmd-musig2-nonce-gen:

NONCE GEN
---------

**Request APDU** (encrypted)

.. list-table::
   :header-rows: 1
   :widths: 12 12 12 12 12 40

   * - CLA
     - INS
     - P1
     - P2
     - LC
     - Data
   * - ``0x80``
     - ``0xC7``
     - ``0x00``
     - ``0x00``
     - ``0x00``
     - MAC

**Preconditions**: Secure Channel opened, seed loaded, PIN or user-key authentication
performed (or pinless path active).

Generates the card's MuSig2 secret nonce pair ``(k1, k2)`` and returns the corresponding
public points ``(R1, R2)``. Internally the card also stores the compressed form of its own
public key ``pk = sk*G`` so that ``LOAD COSIGNER KEY`` can detect it in the cosigner list and
so that ``PARTIAL SIGN`` can verify the signing key has not changed in between (BIP-327
requires ``pk == secnonce[64:97]``).

The secret nonces are derived per BIP-327 ``NonceGen``. Two successive ``NONCE GEN`` calls
always produce different nonce pairs.

**Response Data** --- 66 bytes

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Size
     - Description
   * - R1
     - 33B
     - Compressed EC point ``k1 * G``
   * - R2
     - 33B
     - Compressed EC point ``k2 * G``

.. note::

   An active nonce pair ``(k1, k2)`` survives an applet deselect. It is zeroed after
   ``PARTIAL SIGN`` (successful or rejected), after a full reset, and at the start of any
   new ``NONCE GEN`` call. The host is expected to use each nonce pair exactly once;
   reusing nonces across two different messages leaks the private key by linear algebra.
   The card enforces this by zeroing the nonces after each sign.

**Status Words**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - SW
     - Description
   * - ``0x9000``
     - Success
   * - ``0x6985``
     - PIN or user-key auth not performed, or seed not loaded

----

.. _cmd-musig2-load-cosigner:

LOAD COSIGNER KEY
-----------------

**Request APDU** (encrypted)

.. list-table::
   :header-rows: 1
   :widths: 12 12 12 12 12 40

   * - CLA
     - INS
     - P1
     - P2
     - LC
     - Data
   * - ``0x80``
     - ``0xC8``
     - ``0x01``
     - ``0x00``
     - ``0x21``
     - MAC | Encrypted data

**Preconditions**: Secure Channel opened, PIN or user-key authentication performed (or
pinless path active), state is NONCE_GENERATED or WAIT_COSIGNERS.

Feeds one cosigner public key (33-byte compressed) into the incremental KeyAgg list hash
``L = sha256("KeyAgg list" || pk1 || pk2 || ... || pkN)``. Must be called once per cosigner,
including the card's own key. The order must match the order the host uses to compute the
aggregate public key ``Q``.

A maximum of 32 cosigners can be loaded in a single session; the 33rd call is rejected with
``0x6985``.

While processing each key, the card compares it against its own stored ``pk`` snapshot. If a
match is found, an internal flag is raised; ``PARTIAL SIGN`` later requires this flag to be
set, mirroring the BIP-327 ``Sign`` algorithm's check ``pk in pubkeys``.

**Request Data --- 33 bytes**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Size
     - Description
   * - Cosigner pubkey
     - 33B
     - Compressed EC point (``02|X`` or ``03|X``)

**Status Words**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - SW
     - Description
   * - ``0x9000``
     - Success
   * - ``0x6700``
     - Data length is not 33 bytes
   * - ``0x6985``
     - State is not NONCE_GENERATED or WAIT_COSIGNERS, PIN / user-auth not performed, or
       cosigner-count limit (32) reached

----

.. _cmd-musig2-partial-sign:

PARTIAL SIGN
------------

**Request APDU** (encrypted)

.. list-table::
   :header-rows: 1
   :widths: 12 12 12 12 12 40

   * - CLA
     - INS
     - P1
     - P2
     - LC
     - Data
   * - ``0x80``
     - ``0xC8``
     - ``0x02``
     - ``0x00``
     - ``0xC3``
     - MAC | Encrypted data

**Preconditions**: Secure Channel opened, state is WAIT_COSIGNERS, PIN or user-key auth
performed (or pinless path active), card's own key seen via ``LOAD COSIGNER KEY``.

Computes and returns the card's partial signature ``s_i`` per BIP-327 ``Sign``:

.. code-block:: none

   b   = tagged_hash("MuSig/noncecoef", aggR1 || aggR2 || Q.x || msg) mod n
   R   = aggR1 + b * aggR2
   e   = tagged_hash("BIP0340/challenge", R.x || Q.x || msg) mod n
   a_i = tagged_hash("KeyAgg coefficient", L || pk_i) mod n
   s_i = (k1 + b * k2 + e * a_i * sk) mod n

The card never returns ``R``, ``e``, ``a_i`` or any other intermediate; only ``s_i``. After
the call, the secret nonces ``k1, k2`` and the card's public key snapshot are zeroed, and
the state machine returns to IDLE regardless of the outcome.

**Request Data --- 195 bytes**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Size
     - Description
   * - aggR1
     - 65B
     - Uncompressed EC point (``04 | X | Y``), sum of cosigners' R1
   * - aggR2
     - 65B
     - Uncompressed EC point (``04 | X | Y``), sum of cosigners' R2
   * - aggPubKey Q
     - 33B
     - Compressed aggregate public key (host-computed, must already be tweaked if Taproot)
   * - Message
     - 32B
     - Message hash (typically a Taproot ``sig_msg``)

**Response Data** --- 32 bytes

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Size
     - Description
   * - Partial signature s_i
     - 32B
     - Scalar ``mod n``

.. note::

   The aggregate public key ``Q`` provided in the request must already include the host-side
   Taproot tweak when applicable. The card does not apply BIP-341 tweaks. Sending an
   un-tweaked ``Q`` for a Taproot output yields a signature that will not verify under the
   on-chain key.

.. important::

   ``PARTIAL SIGN`` is single-use per ``NONCE GEN`` call. The nonces are zeroed before the
   function returns and the state goes back to IDLE, so a second ``PARTIAL SIGN`` against
   the same ``aggR1, aggR2`` is rejected. To sign another message, run a full
   ``NONCE GEN`` → ``LOAD COSIGNER KEY`` (× N) → ``PARTIAL SIGN`` cycle.

**Status Words**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - SW
     - Description
   * - ``0x9000``
     - Success
   * - ``0x6700``
     - Data length is not 195 bytes
   * - ``0x6985``
     - State is not WAIT_COSIGNERS, card's own key not in cosigner list, PIN/user-auth
       not performed, or BIP-327 internal check failed (``R`` at infinity, ``a_i == 0``,
       ``pk != secnonce[64:97]``, ``s >= n``, etc.)
   * - ``0x6F00``
     - Internal computation failure (operands out of range); secrets are zeroed on this path

----

References
----------

* BIP-327 — *MuSig2 for BIP340-compatible Multi-Signatures*
* BIP-340 — *Schnorr Signatures for secp256k1*
* BIP-341 — *Taproot: SegWit version 1 spending rules* (host-side tweak only)
