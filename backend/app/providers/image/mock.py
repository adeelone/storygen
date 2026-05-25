from html import escape

from app.providers.base import GeneratedImage, ImageProvider


class MockImageProvider(ImageProvider):
    model_name = "storygen-svg-illustrator-v1"
    supports_reference_conditioning = True

    async def render(
        self, prompt: str, seed: int, aspect_ratio: str, reference_url: str | None = None
    ) -> GeneratedImage:
        width, height = {"1:1": (720, 720), "16:9": (960, 540), "3:4": (720, 960)}.get(aspect_ratio, (720, 960))
        caption = escape(prompt[:125])
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs><linearGradient id="sky" y2="1"><stop stop-color="#fff4df"/><stop offset="1" stop-color="#cfdbc0"/></linearGradient></defs>
<rect width="100%" height="100%" rx="32" fill="url(#sky)"/>
<circle cx="{width * .75}" cy="{height * .22}" r="72" fill="#f9ce78" opacity=".75"/>
<path d="M0 {height*.72} Q {width*.25} {height*.58} {width*.5} {height*.72} T {width} {height*.69} V {height} H0Z" fill="#759567"/>
<ellipse cx="{width*.38}" cy="{height*.62}" rx="68" ry="100" fill="#a65d3c"/><circle cx="{width*.38}" cy="{height*.46}" r="57" fill="#bf7850"/>
<path d="M {width*.30} {height*.59} Q {width*.39} {height*.66} {width*.47} {height*.59}" fill="none" stroke="#e3bf65" stroke-width="13"/>
<rect x="{width*.6}" y="{height*.52}" width="94" height="104" rx="30" fill="#bd7652"/><circle cx="{width*.63}" cy="{height*.56}" r="10" fill="#8bd9e8"/><circle cx="{width*.7}" cy="{height*.56}" r="10" fill="#8bd9e8"/>
<text x="32" y="{height-70}" font-family="Georgia,serif" font-size="18" fill="#353a32">{caption}</text>
<text x="32" y="{height-37}" font-family="system-ui" font-size="13" fill="#59604f">StoryGen illustration | seed {seed}</text>
</svg>"""
        return GeneratedImage(svg.encode(), "image/svg+xml", {"seed": str(seed), "moderation": "safe"})
