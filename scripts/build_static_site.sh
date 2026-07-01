#!/usr/bin/env bash
set -euo pipefail

rm -rf public
mkdir -p public
cp index.html public/
cp -R static public/
cp -R data public/
