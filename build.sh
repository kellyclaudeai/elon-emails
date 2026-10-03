#!/bin/bash
# The site in public/ is prebuilt; nothing to do at deploy time.
echo "static site: $(ls public/e | wc -l) email pages"
