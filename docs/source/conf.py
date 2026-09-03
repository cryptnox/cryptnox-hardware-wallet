# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Cryptnox Hardware Wallet'
copyright = '2026, Cryptnox SA'
author = 'Cryptnox'
release = '2.0.0'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx_multiversion', 'sphinx_sitemap']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- SEO meta tags -----------------------------------------------------------

# -- Canonical URL -----------------------------------------------------------
# The site is published at https://docs.cryptnox.com/cryptnox-hardware-wallet/<version>/
# (sphinx-multiversion writes every version branch into its own sub-folder and passes
# the branch name as smv_current_version). The canonical/og:url must include that
# sub-folder, otherwise every page points at a URL that does not exist (404).
# The fallback (no version) is only for local single-version builds.

_DOCS_ROOT = 'https://docs.cryptnox.com/cryptnox-hardware-wallet/'
html_baseurl = _DOCS_ROOT


def _set_versioned_baseurl(app, config):
    version = getattr(config, 'smv_current_version', '') or ''
    config.html_baseurl = _DOCS_ROOT + (version + '/' if version else '')


def setup(app):
    app.connect('config-inited', _set_versioned_baseurl)


# -- Sitemap -----------------------------------------------------------------
# sphinx-sitemap writes <version>/sitemap.xml from the versioned html_baseurl above.
# The docs hub (cryptnox.github.io) lists these files in docs.cryptnox.com/robots.txt.
sitemap_url_scheme = "{link}"
sitemap_excludes = ["search.html", "genindex.html"]
html_title = 'Cryptnox Hardware Wallet Docs'

html_meta = {
    'description': 'Cryptnox Hardware Wallet — APDU command reference, secure channel protocol, key derivation, signing, and authentication for JavaCard-based crypto wallet cards.',
    'keywords': 'Cryptnox, hardware wallet, smartcard, JavaCard, APDU, secure channel, BIP32, SLIP10, ECDSA, EdDSA, Schnorr, key derivation, cryptocurrency, NFC, cold storage',
    'author': 'Cryptnox',
    'robots': 'index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large',
}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# Logo configuration
html_logo = "_static/cryptnox-logo.png"
html_favicon = "_static/favicon.png"

# Custom CSS and JS
html_css_files = [
    'custom.css',
]

html_js_files = [
    'custom.js',
]

# Theme options
html_theme_options = {
    'analytics_id': 'GT-PJ7HDFB',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#101f2e',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Sitemap / SEO
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False

# -- sphinx-multiversion config ----------------------------------------------

smv_branch_whitelist   = r'^v\d+\.\d+$'
smv_tag_whitelist      = r'^v\d+\.\d+$'
smv_remote_whitelist   = r'^origin$'
smv_released_pattern   = r'^refs/(heads/v\d+\.\d+|tags/v\d+\.\d+)$'
smv_outputdir_format   = '{ref.name}'
smv_prefer_remote_refs = False
