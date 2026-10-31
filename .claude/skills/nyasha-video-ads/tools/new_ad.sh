#!/usr/bin/env bash
# Start a new Nyasha ad: an OpenFilm project with the brand kit, the renders, an end card and a starter ad.json.
# usage: new_ad.sh <folder> "<end-card sign-off html>" "<CTA label>" <render: c2|c3-square|c3-wide|c4>
#   e.g. new_ad.sh nyasha-ads/e-free-audit 'Get your <span class="hl">free audit.</span>' 'Book a free call' c3-wide
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
folder="$1"; signoff="${2:-Let\'s get you <span class=\"hl\">found.</span>}"; cta="${3:-Book a free call}"; render="${4:-c3-wide}"
case "$render" in
  c2) img=c2-portrait.jpg; fx=0.5 ;; c3-square) img=c3-wave-square.jpg; fx=0.52 ;;
  c3-wide) img=c3-wave-wide.jpg; fx=0.6 ;; c4) img=c4-closeup.jpg; fx=0.5 ;;
  *) echo "render must be c2, c3-square, c3-wide or c4" >&2; exit 2 ;;
esac

# OpenFilm's Chromium build may differ from the one installed in a cloud container: point it at the installed one
if [ -d /opt/pw-browsers ] && [ -z "${PLAYWRIGHT_BROWSERS_PATH:-}" ]; then
  pw="${TMPDIR:-/tmp}/openfilm-pw"; mkdir -p "$pw"
  want=$(node -e "const b=require(require('path').join(process.env.HOME,'.npm/_npx/'+require('fs').readdirSync(process.env.HOME+'/.npm/_npx').find(d=>require('fs').existsSync(process.env.HOME+'/.npm/_npx/'+d+'/node_modules/openfilm')),'node_modules/playwright-core/browsers.json'));console.log(b.browsers.find(x=>x.name==='chromium').revision)" 2>/dev/null || true)
  have=$(ls /opt/pw-browsers | sed -n 's/^chromium-\([0-9]*\)$/\1/p' | head -1)
  if [ -n "$want" ] && [ -n "$have" ]; then
    ln -sfn "/opt/pw-browsers/chromium_headless_shell-$have" "$pw/chromium_headless_shell-$want"
    ln -sfn "/opt/pw-browsers/chromium-$have" "$pw/chromium-$want"
    echo "export PLAYWRIGHT_BROWSERS_PATH=$pw   # run this in the shell before openfilm commands"
  fi
  export PLAYWRIGHT_BROWSERS_PATH="$pw"
fi

OPENFILM_NO_BROWSER=1 npx -y openfilm@latest open "$folder" | grep -E '^(project|Studio)' || true
cp -r "$here/kit/lib" "$here/kit/chrome.html" "$folder/"
mkdir -p "$folder/assets/nyasha"
cp "$here/kit/renders/"*.jpg "$folder/assets/nyasha/"
sed -e "s#IMG#assets/nyasha/$img#; s#FX#$fx#; s#SIGNOFF#$signoff#; s#CTA#$cta#; s#DURATION#4#" "$here/kit/endcard.html" > "$folder/endcard.html"
[ -f "$folder/ad.json" ] || cat > "$folder/ad.json" <<'JSON'
{
  "title": "",
  "shots": [
    {"page": "hook", "min": 3, "line": ""},
    {"page": "endcard", "min": 4, "line": ""}
  ],
  "sfx": [
    [1, "whoosh", -0.15],
    [1, "pop", 0.4]
  ],
  "music_volume": 0.3
}
JSON
echo "ready: $folder  (write the shot pages, fill ad.json, then build.py)"
