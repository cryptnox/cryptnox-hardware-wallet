<p align="center">
  <img src="https://github.com/user-attachments/assets/6ce54a27-8fb6-48e6-9d1f-da144f43425a"/>
</p>

<h3 align="center">cryptnox-hardware-wallet</h3>
<p align="center">Documentation for the Cryptnox Hardware Wallet smart card</p>

<br/>

[![Documentation status](https://img.shields.io/badge/docs-latest-blue)](https://cryptnox.github.io/cryptnox-hardware-wallet/)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

This repository contains the technical documentation for the Cryptnox Hardware Wallet card, available on the [Cryptnox documentation portal](https://cryptnox.github.io/cryptnox-hardware-wallet/).

---

## Contents

| Section | Description |
|---------|-------------|
| **Introduction** | Security model, supported algorithms and curves |
| **Technical specifications** | Cryptographic capabilities, communication protocols, Secure Element features |
| **Lifecycle management** | Card states and transitions |
| **Secure channel** | Session establishment, key derivation, APDU encryption |
| **Authentication** | PIN, PUK, user keys, FIDO2 |
| **Seed management** | Seed generation, dual generation mode, key sources |
| **Key derivation** | BIP32 / SLIP-0010, dual curve support, parent key caching |
| **EC signature** | Signature types, output formats, pinless signing |
| **Command overview** | Summary of all APDU commands and their security requirements |
| **APDU commands** | Setup, crypto, data, and user key commands |
| **Status codes reference** | Response codes and error handling |
| **Cryptographic assets** | Key material, credentials, and derived secrets managed by the card |
| **License** | CC BY-NC-ND 4.0 |

---

## Build locally

```bash
pip install -r requirements.txt
sphinx-build -b html docs/source docs/build/html
```

Then open `docs/build/html/index.html` in your browser.

---

## License

`cryptnox-hardware-wallet` is licensed under [CC BY-NC-ND 4.0](LICENSE):

- **Attribution** for appropriate credit to Cryptnox SA
- **NonCommercial** for non-commercial use only
- **NoDerivatives** for unmodified redistribution only

For inquiries, contact: contact@cryptnox.com
