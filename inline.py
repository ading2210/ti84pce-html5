import pathlib
import json
import base64

import httpx
from lxml import html

base_path = pathlib.Path(__file__).parent.resolve()
html_path = base_path / "index.html"
out_path = base_path / "bundled.html"
html_str = html_path.read_text()

document = html.document_fromstring(html_str)
links = document.cssselect("link")
scripts = document.cssselect("script")

def get_resource(url):
  if url.startswith("http"):
    response = httpx.get(url)
    response.raise_for_status()
    return response.content
  
  resource_path = base_path / url
  return resource_path.read_bytes()

for link in links:
  href = link.get("href")
  rel = link.get("rel")
  if rel == "stylesheet" and href:
    print(f"Downloading CSS: {href}")
    css_str = get_resource(href).decode()
    css_str = css_str.replace('url("../images/global/body-bg.png")', "")

    new_style = link.makeelement("style")
    new_style.text = css_str
    link.getparent().replace(link, new_style)
  
  elif rel == "icon" and href:
    print(f"Downloading icon: {href}")
    icon_bytes = get_resource(href)
    icon_b64 = base64.b64encode(icon_bytes).decode()
    icon_type = link.get("type")
    link.set("href", f"data:{icon_type};base64,{icon_b64}")

for script in scripts:
  src = script.get("src")
  target_url = script.get("data-url")

  if not target_url and src:
    print(f"Downloading JS: {src}")
    js_str = get_resource(src).decode()

    new_script = link.makeelement("script")
    new_script.text = js_str
    script.getparent().replace(script, new_script)

  elif target_url:
    print(f"Downloading generic data: {target_url}")
    data_str = json.dumps(get_resource(target_url).decode())
    script.text = data_str
  
out_path.write_bytes(html.tostring(document))