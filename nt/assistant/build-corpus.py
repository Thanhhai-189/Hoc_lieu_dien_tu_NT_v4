"""Rebuild the offline index with Python, lxml and PyMuPDF."""

import json
import re
import unicodedata
from pathlib import Path

import fitz
from lxml import html


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = json.loads((ROOT / 'tuong_tac/lesson-data.json').read_text(encoding='utf-8'))
LESSONS = DATA['lessons']
RECORDS = []
# Some pages straddle lesson boundaries. These captions were checked in Tập 2.
FIGURE_LESSONS = {'9.8': '9.2.4', '10.57': '10.3.5', '10.58': '10.3.5',
                  '11.1': '11.2.1', '11.21': '11.3.1', '11.32': '11.3.2'}


def clean(text):
    return ' '.join(unicodedata.normalize('NFC', text).replace('\u00ad', '').split())


def words(text):
    return set(re.findall(r'\w+', clean(text).lower()))


def chunks(text, limit=870):
    text = clean(text)
    parts = re.split(r'(?<=[.?!])\s+(?=[A-ZÀ-Ỹ0-9(])', text)
    pending = ''
    for part in parts:
        if len(part) > limit:
            if pending:
                yield pending
                pending = ''
            line = ''
            for word in part.split():
                if len(line) + len(word) + 1 > limit and line:
                    yield line
                    line = ''
                line = (line + ' ' + word).strip()
            if line:
                pending = line
        elif len(pending) + len(part) + 1 > limit:
            yield pending
            pending = part
        else:
            pending = (pending + ' ' + part).strip()
    if pending:
        yield pending


def record(kind, code, title, text, **extra):
    body = clean(text)
    if not body:
        return
    RECORDS.append({
        'id': f's{len(RECORDS) + 1}',
        'kind': kind,
        'lesson': code,
        'title': clean(title),
        'text': body,
        **extra,
    })


def lesson_name(lesson):
    return f"{lesson['chapterTitle']} · {lesson['title']}"


def caption_number(value):
    found = re.match(r'^Hình\s+(\d+\.\d+[a-z]?)\b', value, re.I)
    return found[1].lower() if found else None


def index_lesson(lesson):
    code = lesson['code']
    section = lesson_name(lesson)
    record('lesson', code, section, ' '.join(lesson['objectives']))
    note = lesson.get('expertNote')
    if note:
        record('note', code, note['title'], note['text'])
    for sim in lesson['simulations']:
        steps = ' '.join(
            f"{i}. {step['title']}. {step['text']}"
            for i, step in enumerate(sim['steps'], 1)
        )
        record('simulation', code, sim['title'], steps)
    for figure in lesson['figures']:
        caption = figure['caption']
        number = caption_number(caption)
        parts = figure['parts']
        figure_data = {'image': figure['image'], 'caption': caption}
        if number:
            figure_data['number'] = number
        if parts:
            record('figure', code, caption,
                   ' '.join(f"{p['id']}. {p['name']}. {p['description']}" for p in parts),
                   figure=figure_data)
        for part in parts:
            record('part', code, part['name'], part['description'],
                   keywords=part.get('aliases', []), figure=figure_data)

    if lesson.get('reference2026'):
        return
    document = html.parse(str(ROOT / lesson['file']))
    for article in document.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," box ")]'):
        title_node = article.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," box-title ")]')
        title = clean(title_node[0].text_content()) if title_node else ''
        if not title or title == 'Text':
            title = section
        else:
            title = f'{lesson["title"]} · {title}'
        content = article.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," box-content ")]')
        if not content:
            content = [article]
        paragraphs = []
        for box in content:
            for node in box.xpath('.//p | .//li[not(.//p) and not(.//li)] | .//tr'):
                if node.tag == 'tr':
                    value = ' | '.join(clean(cell.text_content()) for cell in node.xpath('./td|./th'))
                else:
                    value = clean(node.text_content())
                number = caption_number(value)
                if number:
                    record('figure', code, value, value, anchor=article.get('id') or '',
                           figure={'number': number, 'caption': value})
                elif len(value) >= 32:
                    paragraphs.append(value)
        if not paragraphs:
            paragraphs = [clean(' '.join(box.text_content() for box in content))]
        for chunk in chunks(' '.join(paragraphs)):
            record('html', code, title, chunk, anchor=article.get('id') or '')


def choose_lesson(candidates, value):
    if len(candidates) == 1:
        return candidates[0]
    text_words = words(value)
    return max(candidates, key=lambda code: len(words(LESSONS[code]['title']) & text_words))


def index_pdf():
    page_lessons = {}
    for code, lesson in LESSONS.items():
        for page in lesson.get('reference2026', {}).get('pages', []):
            page_lessons.setdefault(page, []).append(code)
    path = ROOT / 'nt/tai-lieu-tap2-2026.pdf'
    with fitz.open(path) as pdf:
        page_count = len(pdf)
        for page_number, codes in sorted(page_lessons.items()):
            page = pdf[page_number - 1]
            blocks = []
            for block in page.get_text('blocks', sort=True):
                if block[6] != 0:
                    continue
                value = clean(block[4])
                if len(value) < 25:
                    continue
                number = caption_number(value)
                if number:
                    code = FIGURE_LESSONS.get(number) or choose_lesson(codes, value)
                    record('figure', code, value, value, pages=[page_number],
                           figure={'number': number, 'caption': value})
                    continue
                blocks.append(value)
            for chunk in chunks(' '.join(blocks)):
                code = choose_lesson(codes, chunk)
                record('pdf', code, lesson_name(LESSONS[code]), chunk, pages=[page_number])

    for figure in DATA.get('referenceFigures', []):
        codes = page_lessons.get(figure['page'])
        if not codes:
            continue
        code = FIGURE_LESSONS.get(figure['number']) or choose_lesson(codes, figure['caption'])
        record('figure', code, figure['caption'], figure['caption'], pages=[figure['page']],
               figure={k: figure[k] for k in ('image', 'caption', 'number')})
    return page_count


def main():
    for lesson in LESSONS.values():
        index_lesson(lesson)
    page_count = index_pdf()
    cards = json.loads((HERE / 'topics.json').read_text(encoding='utf-8'))
    for card in cards:
        fields = dict(card)
        code = fields.pop('lesson')
        title = fields.pop('title')
        body = fields.pop('text')
        assert code in LESSONS, code
        record('topic', code, title, body, **fields)
    corpus = {'version': 2, 'pdfPages': page_count, 'records': RECORDS}
    output = 'window.NT_ASSISTANT_CORPUS = ' + json.dumps(corpus, ensure_ascii=False, separators=(',', ':')) + ';\n'
    (HERE / 'corpus.js').write_text(output, encoding='utf-8')
    print(f'{len(RECORDS)} excerpts from {len(LESSONS)} lessons, including {len(cards)} curated topics')


if __name__ == '__main__':
    main()
