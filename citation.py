from scholarly import scholarly
import re

user_id = "2BZcUuAAAAAJ"

author = scholarly.search_author_id(user_id, filled=True)

total_citations = author.get('citedby', 0)
h_index = author.get('hindex', 0)
i10_index = author.get('i10index', 0)

badge_md = (
    f"![Citations](https://img.shields.io/badge/citations-{total_citations}-brightgreen) "
    f"![h-index](https://img.shields.io/badge/h--index-{h_index}-blue) "
    f"![i10-index](https://img.shields.io/badge/i10--index-{i10_index}-orange)"
)

publications = []
for i, pub in enumerate(author.get('publications', []), 1):
    try:
        filled_pub = scholarly.fill(pub)
        bib = filled_pub.get('bib', {})
        title = bib.get('title', 'Unknown Title')
        year = bib.get('pub_year', 'N/A')
        citations = filled_pub.get('num_citations', 0)

        venue = bib.get('venue') or bib.get('journal') or bib.get('booktitle') or ""

        publications.append({
            'title': title,
            'year': year,
            'venue': venue,
            'citations': citations
        })
    except Exception as e:
        print(f"Error processing publication {i}: {e}")
        continue

publications.sort(key=lambda x: x['citations'], reverse=True)

citation_list_md = "### 📝 Publications\n\n"
if publications:
    for i, pub in enumerate(publications, 1):
        venue_text = f" *{pub['venue']}*" if pub['venue'] else ""
        citation_list_md += f"{i}. **{pub['title']}** ({pub['year']}){venue_text} - {pub['citations']} citations\n\n"
else:
    citation_list_md += "No publications found.\n\n"

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

if "![Citations]" in content:
    content = re.sub(r"!\[Citations\][^\n]*", badge_md, content)
else:
    content = badge_md + "\n\n" + content

if "### 📝 Publications" in content:
    start_pos = content.find("### 📝 Publications")
    next_section_pos = content.find("\n### ", start_pos + 1)
    if next_section_pos != -1:
        content = content[:start_pos] + citation_list_md + content[next_section_pos:]
    else:
        content = content[:start_pos] + citation_list_md
else:
    content += "\n" + citation_list_md

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("README.md updated successfully!")


