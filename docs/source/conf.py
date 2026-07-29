# Configuration file for the Sphinx documentation builder.

# Derive the navy PDF cover logo from the white HTML SVG at build time, so only the
# SVG is a committed source asset (needs cairosvg + Pillow, both in the docs requirements).
import os as _os
try:
    import io as _io
    import cairosvg
    from PIL import Image as _Image
except ImportError as _e:
    raise RuntimeError(
        "Docs build requires cairosvg and Pillow to generate the PDF cover logo; "
        "install them (pip install cairosvg pillow)."
    ) from _e
_static = _os.path.join(_os.path.dirname(__file__), "_static")
with open(_os.path.join(_static, "cryptnox-logo.svg"), encoding="utf-8") as _f:
    _svg = _f.read()
_png = cairosvg.svg2png(
    bytestring=_svg.replace('fill="white"', 'fill="#101f2e"').encode(),
    output_width=1200, output_height=226,
)
_Image.open(_io.BytesIO(_png)).save(
    _os.path.join(_static, "cryptnox-logo-dark.png"), dpi=(400, 400)
)

# -- Project information -----------------------------------------------------

project = 'Cryptnox Hardware Wallet'
copyright = '2026, Cryptnox SA'
author = 'Cryptnox'
release = '1.6.1'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx_multiversion']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- SEO meta tags -----------------------------------------------------------

html_baseurl = 'https://cryptnox.github.io/cryptnox-hardware-wallet/'
html_title = 'Cryptnox Hardware Wallet Docs'

html_meta = {
    'description': 'Cryptnox Hardware Wallet v1.6.1 — APDU command reference, secure channel protocol, key derivation, signing, and authentication for JavaCard-based crypto wallet cards.',
    'keywords': 'Cryptnox, hardware wallet, smartcard, JavaCard, APDU, secure channel, BIP32, SLIP10, ECDSA, Schnorr, key derivation, cryptocurrency, NFC, cold storage',
    'author': 'Cryptnox',
    'robots': 'index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large',
}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# Logo configuration
html_logo = "_static/cryptnox-logo.svg"
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

# -- Options for PDF (LaTeX) output ------------------------------------------
# Built by CI with pdflatex, same as Yubico's tech manual. Output: cryptnox-hardware-wallet.pdf

today = 'June 20, 2026'  # fixed doc date on the cover

latex_engine = 'pdflatex'
latex_logo = '_static/cryptnox-logo-dark.png'  # white logo is invisible on white PDF title page
latex_domain_indices = False  # no Python Module Index in the PDF (kept in HTML)
latex_documents = [
    ('index', 'cryptnox-hardware-wallet.tex',
     'Cryptnox Hardware Wallet — API Reference', author, 'manual'),
]
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'figure_align': 'H',
    'sphinxsetup': 'pre_border-radius=0pt',  # sharp rectangle corners on code-block (command-line) frames
    'extraclassoptions': 'oneside,openany',  # no blank filler pages (web PDF)
    'printindex': '',  # drop the general Index from the PDF (kept in HTML)
    'fncychap': '',  # no fancy chapter rules; titlesec styles chapters instead
    'preamble': r'''
% Symbols pdflatex can't render natively: map check/cross marks and drop emoji
\usepackage{pifont}
\DeclareUnicodeCharacter{2713}{\ding{51}}% check mark
\DeclareUnicodeCharacter{2717}{\ding{55}}% ballot X
\DeclareUnicodeCharacter{1F4C4}{}% page facing up
% Left-align body text (ragged right instead of justified)
\usepackage[document]{ragged2e}
% Drop the "(continues on next page)" / "(continued from previous page)" labels (parens included) on code blocks
\AtBeginDocument{\renewcommand*\sphinxstylecodecontinued[1]{}\renewcommand*\sphinxstylecodecontinues[1]{}}
% Whole document in the sans font (TeX Gyre Heros)
\renewcommand{\familydefault}{\sfdefault}
% Literals, tables and code blocks in DejaVu Sans Mono instead of Sphinx's default txtt;
% scaled down since DejaVu runs large next to Heros
\usepackage[scaled=0.82]{DejaVuSansMono}
% Sans-serif TOC entries
\AtBeginDocument{\addtocontents{toc}{\protect\sffamily}}
% Left-aligned chapter headings
\usepackage{titlesec}
\titleformat{\chapter}[hang]{\sffamily\bfseries\huge}{\thechapter}{1em}{}
\titlespacing*{\chapter}{0pt}{0pt}{20pt}
\usepackage{fancyhdr}
\def\headruleskip{4pt}\def\footruleskip{4pt}% gap between header/footer text and rule
\makeatletter
% Centered page header (doc title) + copyright footer
\AtBeginDocument{%
  \fancypagestyle{normal}{%
    \fancyhf{}%
    \fancyhead[C]{\sffamily\nouppercase{\@title}}%
    \fancyfoot[L]{\sffamily\copyright{} 2026 Cryptnox SA}%
    \fancyfoot[R]{\sffamily\thepage}%
    \renewcommand{\headrulewidth}{0.4pt}%
    \renewcommand{\footrulewidth}{0.4pt}%
  }%
  \fancypagestyle{plain}{%
    \fancyhf{}%
    \fancyfoot[L]{\sffamily\copyright{} 2026 Cryptnox SA}%
    \fancyfoot[R]{\sffamily\thepage}%
    \renewcommand{\headrulewidth}{0pt}%
    \renewcommand{\footrulewidth}{0.4pt}%
  }%
  \pagestyle{normal}%
}
% Centered title page (default is right-aligned); author line removed (logo brands it)
\renewcommand{\sphinxmaketitle}{%
  \let\sphinxrestorepageanchorsetting\relax
  \ifHy@pageanchor\def\sphinxrestorepageanchorsetting{\Hy@pageanchortrue}\fi
  \hypersetup{pageanchor=false}%
  \begin{titlepage}%
    \let\footnotesize\small \let\footnoterule\relax
    \begingroup
      \def\endgraf{ }\def\and{\& }%
      \pdfstringdefDisableCommands{\def\\{, }}%
      \hypersetup{pdfauthor={\@author}, pdftitle={\@title}}%
    \endgroup
    \noindent\rule{\textwidth}{1pt}\par
    \begin{flushright}%
      \vskip 1em%
      \includegraphics[width=7cm]{cryptnox-logo-dark}\par
      \vskip 2em%
      {\LARGE\py@HeaderFamily \@title \par}%
      \vskip 0.5em%
      {\large\itshape \py@release\releaseinfo \par}%
      \vfill
      {\large \@date \par}%
    \end{flushright}%
    \@thanks
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \let\thanks\relax\let\maketitle\relax
  \clearpage
  \ifdefined\sphinxbackoftitlepage\sphinxbackoftitlepage\fi
  \if@openright\cleardoublepage\else\clearpage\fi
  \sphinxrestorepageanchorsetting
}
\makeatother
''',
}

# -- sphinx-multiversion config ----------------------------------------------

smv_branch_whitelist   = r'^v\d+\.\d+$'
smv_tag_whitelist      = r'^v\d+\.\d+$'
smv_remote_whitelist   = r'^origin$'
smv_released_pattern   = r'^refs/(heads/v\d+\.\d+|tags/v\d+\.\d+)$'
smv_outputdir_format   = '{ref.name}'
smv_prefer_remote_refs = False
