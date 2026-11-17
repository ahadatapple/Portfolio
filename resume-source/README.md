# Résumé source

`build_resume.py` generates both résumés in `public/` with ReportLab. With the
content set to the original wording, it reproduces the original PDFs line for line.

```sh
pip install reportlab
python3 build_resume.py ../public --public   # website copies, without the phone number
python3 build_resume.py ~/Desktop            # copies for applications, with the phone number
python3 build_resume.py /tmp/orig original   # the pre-update wording, for comparison
```

Edit the text in `content()`. The script stops with an error if anything runs past one page.
It needs the Liberation Serif fonts (`fonts-liberation` on Debian and Ubuntu); on macOS,
install them or change `FONT_DIR`.
