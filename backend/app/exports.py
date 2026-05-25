import io
import zipfile
from html import escape

from app.models import StoryRecord


def render_pdf(story: StoryRecord) -> bytes:
    text = f"{story.plan.title if story.plan else story.slug}\n\n" + "\n\n".join(
        " ".join(scene.paragraphs) for scene in story.scenes
    )
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").replace("\n", ") Tj T* (")
    stream = f"BT /F1 14 Tf 50 750 Td ({escaped}) Tj ET"
    content = stream.encode("latin-1", "replace")
    return (
        b"%PDF-1.4\n1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        + f"4 0 obj << /Length {len(content)} >> stream\n".encode()
        + content
        + b"\nendstream endobj\n5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\nxref\n0 6\n0000000000 65535 f \ntrailer << /Root 1 0 R /Size 6 >>\nstartxref\n0\n%%EOF"
    )


def render_epub(story: StoryRecord) -> bytes:
    title = escape(story.plan.title if story.plan else story.slug)
    sections = "".join(
        f"<section><h2>{escape(scene.outline.title)}</h2><p>{escape(' '.join(scene.paragraphs))}</p></section>"
        for scene in story.scenes
    )
    html = f"<html xmlns='http://www.w3.org/1999/xhtml'><head><title>{title}</title></head><body><h1>{title}</h1>{sections}</body></html>"
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        archive.writestr(
            "META-INF/container.xml",
            "<?xml version='1.0'?><container><rootfiles><rootfile full-path='content.xhtml'/></rootfiles></container>",
        )
        archive.writestr("content.xhtml", html)
    return output.getvalue()
