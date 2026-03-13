<p align="center">
  <img src="https://github.com/user-attachments/assets/6ce54a27-8fb6-48e6-9d1f-da144f43425a"/>
</p>

<h3 align="center">cryptnox-hardware-wallet</h3>
<p align="center">Documentation for the Cryptnox Hardware Wallet smart card</p>

<br/>

[![Documentation status](https://img.shields.io/badge/docs-latest-blue)](https://docs.cryptnox.com/cryptnox-hardware-wallet/)
[![License: GPLv3](https://img.shields.io/badge/License-LGPLv3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

This repository contains the **Sphinx-based technical documentation** for the Cryptnox Hardware Wallet card, served as a sub-path of the Cryptnox documentation portal at [docs.cryptnox.com/cryptnox-hardware-wallet](https://docs.cryptnox.com/cryptnox-hardware-wallet/).

---

## Contents

| Section | Description |
|---------|-------------|
| **Introduction** | Security model, supported algorithms and curves |
| **Technical Specifications** | Cryptographic capabilities, communication protocols, Secure Element features |
| **Lifecycle** | Card states and transitions |
| **Secure Channel** | Session establishment, key derivation, APDU encryption |
| **Authentication** | PIN, PUK, user keys, FIDO2 |
| **Seed Management** | Seed generation, dual generation mode, key sources |
| **Key Derivation** | BIP32 / SLIP-0010, dual curve support, parent key caching |
| **Signing** | Signature types, output formats, pinless signing |
| **APDU Commands** | Setup, crypto, data, and user key commands |
| **Status Codes** | Response codes and error handling |

---

## Build locally

```bash
pip install -r requirements.txt
sphinx-build -b html docs/source docs/build/html
```

Then open `docs/build/html/index.html` in your browser.

---

## License

cryptnox-hardware-wallet is dual-licensed:

- **LGPL-3.0** for open-source projects and proprietary projects that comply with LGPL requirements
- **Commercial license** for projects that require a proprietary license without LGPL obligations (see COMMERCIAL.md for details)

For commercial inquiries, contact: contact@cryptnox.com
