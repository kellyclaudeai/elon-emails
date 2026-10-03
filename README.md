# Elon Emails

Static site for https://elonemails.com: a searchable archive of publicly available Elon Musk emails.

- `public/` is the deployed site (prebuilt): `index.html` (search), `all.html` (plain list), `e/` (one page per email), `elon-mails.pdf`, `emails.json`, `sitemap.xml`.
- `src/` holds the dataset and the scripts that generate `public/`.

To rebuild after editing `src/emails.json` or the template:

    cd src && BASE_URL=https://elonemails.com/ python3 build.py && python3 pdf.py && cp out/elon-mails.pdf site/ && rm -rf ../public && cp -r site ../public

`pdf.py` needs `reportlab` and the DejaVu fonts (set `FONTDIR` if they are not in /usr/share/fonts/truetype/dejavu/).
