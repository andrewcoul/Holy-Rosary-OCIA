import os
import json
import mammoth

ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(ROOT, "resources")
CLASSES_DIR = os.path.join(ROOT, "classes")
READINGS_DIR = os.path.join(ROOT, "readings")
MANIFEST_PATH = os.path.join(READINGS_DIR, "manifest.json")

CLASSES = [
    {"num": 1,  "key": "class-01", "title": "Intro, Faith and Reason I",
     "docx": ["Class Notes #1 - Intro, Faith and Reason I.docx"]},
    {"num": 2,  "key": "class-02", "title": "Faith and Reason II",
     "docx": ["Class Notes #2 - Faith and Reason II.docx"]},
    {"num": 3,  "key": "class-03", "title": "Interpreting Scripture",
     "docx": ["Class Notes #3 - Interpreting Scripture.docx"]},
    {"num": 4,  "key": "class-04", "title": "Prayer, Parts of the Mass",
     "docx": ["Class Notes #4 - Prayer, Parts of the Mass.docx"]},
    {"num": 5,  "key": "class-05", "title": "The Human Person",
     "docx": ["Class Notes #5 - The Human Person.docx"]},
    {"num": 6,  "key": "class-06", "title": "Original Sin I",
     "docx": ["Class Notes #6 - Original Sin I.docx"]},
    {"num": 7,  "key": "class-07", "title": "Original Sin II",
     "docx": ["Class Notes #7 - Original Sin II.docx"]},
    {"num": 9,  "key": "class-09", "title": "Messianic Promise",
     "docx": ["Class Notes #9 - Messianic Promise.docx"]},
    {"num": 10, "key": "class-10", "title": "Christology",
     "docx": ["Class Notes #10 - Christology.docx"]},
    {"num": 11, "key": "class-11", "title": "Soteriology",
     "docx": ["Class Notes #11 - Soteriology.docx"]},
    {"num": 12, "key": "class-12", "title": "Crucifixion, Resurrection",
     "docx": ["Class Notes #12 - Crucifixion, Resurrection.docx"]},
    {"num": 13, "key": "class-13", "title": "Trinity I",
     "docx": ["Class Notes #13 - Trinity I.docx"]},
    {"num": 14, "key": "class-14", "title": "Trinity II",
     "docx": ["Class Notes #14 - Trinity II.docx"]},
    {"num": 15, "key": "class-15", "title": "Church Founding",
     "docx": ["Class Notes #15 - Church Founding.docx"]},
    {"num": 16, "key": "class-16", "title": "Marks of the Church",
     "docx": [
         "Class Notes #16 - Marks of the Church.docx",
         "Class Notes #16 - OCIA 2025-2026 - Personal Notes.docx",
     ]},
    {"num": 17, "key": "class-17", "title": "Church Hierarchy",
     "docx": ["Class Notes #17 - Church Hierarchy.docx"]},
    {"num": 18, "key": "class-18", "title": "Church Hierarchy, Conscience",
     "docx": ["Class Notes #18 - Church Hierarchy, Conscience.docx"]},
    {"num": 19, "key": "class-19", "title": "Moral Conscience, Justification",
     "docx": ["Class Notes #19 - Moral Conscience, Justification.docx"]},
    {"num": 20, "key": "class-20", "title": "Grace, Sacraments, Reconciliation",
     "docx": ["Class Notes #20 - Grace, Sacraments, Reconciliation.docx"]},
    {"num": 21, "key": "class-21", "title": "Baptism and Confirmation",
     "docx": ["Class Notes #21 - Baptism and Confirmation.docx"]},
    {"num": 22, "key": "class-22", "title": "The Eucharist",
     "docx": ["Class Notes #22 - The Eucharist.docx"]},
    {"num": 24, "key": "class-24", "title": "Holy Orders",
     "docx": ["Class Notes #24 - Holy Orders.docx"]},
    {"num": 25, "key": "class-25", "title": "Holy Orders, Mary",
     "docx": ["Class Notes #25 - Holy Orders, Mary.docx"]},
    {"num": 26, "key": "class-26", "title": "Eschatology",
     "docx": ["Class Notes #26 - Eschatology.docx"]},
    {"num": 27, "key": "class-27", "title": "Mystagogy I",
     "docx": ["Class Notes #27 - Mystagogy I.docx"]},
    {"num": 28, "key": "class-28", "title": "Mary",
     "docx": ["Class Notes #28 - Mary.docx"]},
    {"num": 29, "key": "class-29", "title": "Christian Spirituality and Synthesis",
     "docx": ["Class Notes #29 - Christian Spirituality and Synthesis.docx"]},
]

CLASS_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Class {class_num_display} — {class_title} · OCIA</title>
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header>
    <a href="../index.html" class="back-link">← All Classes</a>
    <h1>Class {class_num_display} — {class_title}</h1>
  </header>
  <main>
    <div class="tabs">
      <div class="tab-bar">
        <button class="tab-btn active" data-tab="notes">Notes</button>
        <button class="tab-btn" data-tab="readings">Readings</button>
      </div>
      <div class="tab-panel active" id="tab-notes">
        <div class="notes-body">
{notes_html}
        </div>
      </div>
      <div class="tab-panel" id="tab-readings">
        <div id="readings-container" data-class="{class_key}"></div>
      </div>
    </div>
  </main>

  <nav class="page-nav">
    <span class="prev-link">{prev_link}</span>
    <span class="next-link">{next_link}</span>
  </nav>

  <footer><p>Personal notes — not for redistribution.</p></footer>

  <script>
    (function () {{
      // Tab switching
      document.querySelectorAll('.tab-btn').forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          document.querySelectorAll('.tab-btn').forEach(function (b) {{ b.classList.remove('active'); }});
          document.querySelectorAll('.tab-panel').forEach(function (p) {{ p.classList.remove('active'); }});
          btn.classList.add('active');
          document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
        }});
      }});

      // Load readings from manifest
      var key = document.getElementById('readings-container').dataset.class;
      fetch('../readings/manifest.json')
        .then(function (r) {{ return r.json(); }})
        .then(function (manifest) {{
          var container = document.getElementById('readings-container');
          var pdfs = manifest[key] || [];
          if (!pdfs.length) {{
            container.innerHTML = '<p class="no-readings">No readings have been added yet.</p>';
          }} else {{
            var html = '';
            pdfs.forEach(function (pdf) {{
              html += '<div class="pdf-viewer">'
                + '<h3>' + pdf.title + '</h3>'
                + '<iframe src="../' + pdf.file + '" width="100%" height="800px" title="' + pdf.title + '">'
                + '<p>Your browser cannot display this PDF inline. '
                + '<a href="../' + pdf.file + '">Download it here</a>.</p>'
                + '</iframe></div>';
            }});
            container.innerHTML = html;
          }}
        }})
        .catch(function () {{
          document.getElementById('readings-container').innerHTML =
            '<p class="no-readings">Readings unavailable (open via a web server, not file://).</p>';
        }});
    }})();
  </script>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OCIA — Class Notes</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>OCIA — Class Notes</h1>
    <p class="subtitle">Order of Christian Initiation of Adults · 2025–2026</p>
  </header>
  <main>
    <nav class="class-list">
      <ol>
{class_list_items}
      </ol>
    </nav>
  </main>
  <footer><p>Personal notes — not for redistribution.</p></footer>
</body>
</html>
"""


def convert_docx(filename):
    path = os.path.join(RESOURCES, filename)
    style_map = (
        "p[style-name='Heading 1'] => h2:fresh\n"
        "p[style-name='Heading 2'] => h3:fresh\n"
        "p[style-name='Heading 3'] => h4:fresh\n"
    )
    with open(path, "rb") as f:
        result = mammoth.convert_to_html(f, style_map=style_map)
    if result.messages:
        for msg in result.messages:
            print(f"  [mammoth] {filename}: {msg}")
    return result.value


def build():
    os.makedirs(CLASSES_DIR, exist_ok=True)
    os.makedirs(READINGS_DIR, exist_ok=True)

    # Create per-class readings subfolders
    for cls in CLASSES:
        os.makedirs(os.path.join(READINGS_DIR, cls["key"]), exist_ok=True)

    # Write starter manifest only if one doesn't exist yet
    if not os.path.exists(MANIFEST_PATH):
        starter = {cls["key"]: [] for cls in CLASSES}
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(starter, f, indent=2)
        print("Created manifest.json")

    # Build class pages
    for i, cls in enumerate(CLASSES):
        print(f"Building class-{cls['num']:02d}: {cls['title']} ...")

        parts = []
        for j, docx in enumerate(cls["docx"]):
            html = convert_docx(docx)
            if j > 0:
                html = ('<hr class="notes-separator">'
                        '<h3 class="notes-label">Personal Notes</h3>\n') + html
            parts.append(html)
        notes_html = "\n".join(parts)

        prev_cls = CLASSES[i - 1] if i > 0 else None
        next_cls = CLASSES[i + 1] if i < len(CLASSES) - 1 else None

        prev_link = (
            f'<a href="{prev_cls["key"]}.html">← Class #{prev_cls["num"]}: {prev_cls["title"]}</a>'
            if prev_cls else ""
        )
        next_link = (
            f'<a href="{next_cls["key"]}.html">Class #{next_cls["num"]}: {next_cls["title"]} →</a>'
            if next_cls else ""
        )

        page = CLASS_PAGE_TEMPLATE.format(
            class_title=cls["title"],
            class_num_display=f'#{cls["num"]}',
            notes_html=notes_html,
            class_key=cls["key"],
            prev_link=prev_link,
            next_link=next_link,
        )

        out_path = os.path.join(CLASSES_DIR, f'{cls["key"]}.html')
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page)

    # Build index.html
    items = []
    for cls in CLASSES:
        items.append(
            f'        <li><a href="classes/{cls["key"]}.html">'
            f'Class #{cls["num"]} — {cls["title"]}</a></li>'
        )

    index = INDEX_TEMPLATE.format(class_list_items="\n".join(items))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)

    print(f"\nDone. Generated {len(CLASSES)} class pages + index.html")
    print("To preview: python -m http.server 8000  (then open http://localhost:8000)")


if __name__ == "__main__":
    build()
