"""Rebuild Ahad Rahman's two résumés with ReportLab, matching the original
layout: US Letter, Liberation Serif, same positions and spacing.

python3 build_resume.py <out_dir> [original|updated] [--public]

--public leaves out the phone number, for the copies served on the website.
"""
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_DIR = Path('/usr/share/fonts/truetype/liberation')
for name, file in [('Serif', 'LiberationSerif-Regular.ttf'), ('Serif-Bold', 'LiberationSerif-Bold.ttf'),
                   ('Serif-Italic', 'LiberationSerif-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))

PAGE_W, PAGE_H = letter
BODY, HEAD, NAME = 10.3, 12.3, 19.0
LINE = 12.2
ASC = 0.784                     # baseline offset below a line's top, em units (matches the originals)
LEFT_ENTRY, RIGHT = 50, 562     # bold entry rows span 50 to 562
LEFT, RULE_RIGHT = 56, 556
TEXT_X, WRAP_RIGHT = 78, 556


def wrap(text, font, size, width):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        trial = f'{cur} {w}'.strip()
        if stringWidth(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


class Page:
    def __init__(self, path, title):
        self.c = canvas.Canvas(str(path), pagesize=letter)
        self.c.setTitle(title)
        self.c.setAuthor('Ahad Rahman')
        self.top = 42.1  # pdfplumber-style top of the next line

    def base(self, top, size):
        return PAGE_H - (top + ASC * size)

    def name(self, text, contact, links=None):
        self.c.setFont('Serif-Bold', NAME)
        self.c.drawCentredString(PAGE_W / 2, self.base(42.1, NAME), text)
        self.c.setFont('Serif', BODY)
        y = self.base(62.2, BODY)
        self.c.drawCentredString(PAGE_W / 2, y, contact)
        # Clickable areas over each link in the contact line.
        x0 = PAGE_W / 2 - stringWidth(contact, 'Serif', BODY) / 2
        for label, url in (links or {}).items():
            start = x0 + stringWidth(contact[:contact.index(label)], 'Serif', BODY)
            end = start + stringWidth(label, 'Serif', BODY)
            self.c.linkURL(url, (start, y - 2.5, end, y + BODY * 0.8), relative=0, thickness=0)
        self.top = 81.7

    def section(self, title, first=False):
        if not first:
            self.top += LINE + 6.5  # 18.7 from the last line's top
        self.c.setFont('Serif-Bold', HEAD)
        self.c.drawString(LEFT, self.base(self.top, HEAD), title)
        self.c.setLineWidth(0.7)
        y = PAGE_H - (self.top + 13.0)
        self.c.line(LEFT, y, RULE_RIGHT, y)
        self.top += 17.2  # first row 4.2 below the rule
        self._fresh = True

    def _next(self):
        if self._fresh:
            self._fresh = False
        else:
            self.top += LINE

    def row(self, left, right, font='Serif-Bold'):
        self._next()
        self.c.setFont(font, BODY)
        y = self.base(self.top, BODY)
        self.c.drawString(LEFT_ENTRY, y, left)
        self.c.drawRightString(RIGHT, y, right)

    def bullet(self, text):
        for i, line in enumerate(wrap(text, 'Serif', BODY, WRAP_RIGHT - TEXT_X)):
            self._next()
            if i == 0:
                self.c.setFont('Helvetica', 8)
                self.c.drawString(LEFT, PAGE_H - (self.top + 6.85), '•')
            self.c.setFont('Serif', BODY)
            self.c.drawString(TEXT_X, self.base(self.top, BODY), line)

    def labeled(self, label, text):
        """Bold label, then regular text, wrapping back to the left margin."""
        self._next()
        lw = stringWidth(label, 'Serif-Bold', BODY)
        first_width = WRAP_RIGHT - LEFT - lw
        words, first = text.split(' '), ''
        while words and stringWidth(f'{first} {words[0]}', 'Serif', BODY) <= first_width:
            first = f'{first} {words.pop(0)}'
        y = self.base(self.top, BODY)
        self.c.setFont('Serif-Bold', BODY)
        self.c.drawString(LEFT, y, label)
        self.c.setFont('Serif', BODY)
        self.c.drawString(LEFT + lw, y, first)
        if words:
            for line in wrap(' '.join(words), 'Serif', BODY, WRAP_RIGHT - LEFT):
                self.top += LINE
                self.c.drawString(LEFT, self.base(self.top, BODY), line)

    def save(self):
        assert self.top < 740, f'content overflows the page (last line top {self.top:.1f})'
        self.c.showPage()
        self.c.save()
        return self.top


# ----------------------------------------------------------------------------
# Content. ORIGINAL reproduces the uploaded PDFs; UPDATED carries the changes.
# ----------------------------------------------------------------------------

def content(version, public=False):
    upd = version == 'updated'
    contact = 'aar15@rice.edu • (832) 379-8593 • Houston, TX • linkedin.com/in/ahad-rahman-rice'
    links = {}
    if upd:
        # Houston, TX moves off this line to make room; the Education row still shows it.
        contact = ('aar15@rice.edu • (832) 379-8593 • ahadatapple.dev • linkedin.com/in/ahad-rahman-rice • '
                   'github.com/ahadatapple')
        if public:
            # No phone number online; that frees room for the city again.
            contact = ('aar15@rice.edu • Houston, TX • ahadatapple.dev • linkedin.com/in/ahad-rahman-rice • '
                       'github.com/ahadatapple')
        links = {
            'aar15@rice.edu': 'mailto:aar15@rice.edu',
            'ahadatapple.dev': 'https://ahadatapple.dev',
            'linkedin.com/in/ahad-rahman-rice': 'https://www.linkedin.com/in/ahad-rahman-rice',
            'github.com/ahadatapple': 'https://github.com/ahadatapple',
        }

    nest = [
        'Shipped a redesigned resources page for NEST360, a newborn-health nonprofit, adding topic filtering, sorting, and '
        'color-coded tags with in-browser filtering by implementing a Figma design across '
        + ('6' if upd else '2') + ' merged pull requests.',
        'Built reusable resource-gallery frontend components with a student team, using Git pull requests and code review.',
    ]
    ascentup = [
        ('Surfaced 20 bugs across 7 modules of a partner health startup\'s app, including a high-severity blocker, through UI '
         'testing, Next.js codebase tracing, and SQL checks against a 41-table Supabase (PostgreSQL) database.'
         if upd else
         'Surfaced 20+ bugs across 7 app modules, including a high-severity blocker, by running full QA with UI testing, '
         'Next.js codebase tracing, and SQL verification against a 41-table Supabase (PostgreSQL) database.'),
        'Unblocked 3 dependent bug fixes and shipped 2 production fixes by resolving ' + ('6' if upd else '6+')
        + ' dev-environment blockers (Docker, Supabase, Git) through systematic log analysis, documenting each fix for the team.',
    ]
    gomoku = [
        ('Raised the win rate against the hardest bot from 70% to 100% by using playtesting to find and fix a directional bias '
         'in the opening play of a Python (NumPy) minimax engine.'
         if upd else
         'Raised the win rate against the hardest bot from 70% to 100% by finding and removing a directional bias in the '
         'attack/defense scoring of an object-oriented Python (NumPy) minimax engine.'),
        ('Measured every strategy change with tournament testing (n=20 games per matchup), reaching 100% against peer bots; '
         'earned one of 38 first-year presentation spots at Rice\'s STEM Symposium.'
         if upd else
         'Measured every strategy change with a tournament-testing framework (n=20 games per matchup), reaching 100% '
         'against peer bots; earned one of 38 first-year presentation spots at Rice\'s STEM Symposium.'),
    ]
    ecodash = [
        'Won 3rd place by building and pitching a full-stack marketplace matching unwanted items with neighbors, haulers, '
        'and recyclers in Next.js, React, TypeScript, and Supabase within the hackathon time limit.',
    ]
    leadership = [
        ('Program Manager & Research Intern – Teens in Health', 'Jul. 2024 – Aug. 2026', [
            'Guided cohorts of 80+ interns to completed medical projects by setting timelines and reviewing deliverables; '
            'authored a 17-page research paper synthesizing 30+ sources.']),
        ('Academic Tutor – IQ Viet My Tutoring Center', 'Mar. 2026 – Jun. 2026', [
            'Raised student scores by 30% in math, science, ELA, and history by tutoring students ages 11–14 on STAAR standards.']),
        ('Founder & President – Red Cross Club, Klein Forest High School', 'Sep. 2024 – May 2026', [
            'Grew the club to 70+ active members and raised $300+ for the Measles & Rubella Initiative by organizing '
            'fundraisers, donation drives (700+ items for veterans), and first-aid training.']),
    ]
    honors = ('Gates Scholar; Amazon Future Engineer Scholar (incoming Amazon intern, Summer 2027); Rice Emerging '
              'Scholars Program')

    swe = dict(
        file='resume.pdf', contact=contact, links=links, honors=honors,
        coursework='Computational Thinking (Python), Fundamentals of Computer Engineering (computer architecture), '
                   'Multivariable Calculus, Mechanics, Bias and Medical Device Design',
        experience=('EXPERIENCE', [
            ('Software Engineer – RiceApps (NEST360)', 'Sep. 2026 – Present', nest),
            ('Undergraduate Researcher – Yamagami Lab, Rice University', 'Sep. 2026 – Present', [
                'Building a gesture-recognition pipeline for accessible XR input for patients with motor disabilities, comparing '
                'SVM, Random Forest, and MiniRocket time-series classifiers trained on video-sensing data in '
                + ('Python.' if upd else 'Python and C++.'),
                ('Collected and processed a self-recorded dataset of 121 videos across 3 gestures; all three classifiers exceed '
                 '95% accuracy on held-out recordings in preliminary results, presented in lab meetings.'
                 if upd else
                 'Collected and processed a self-recorded gesture dataset to train and validate models, and present results in lab '
                 'meetings.'),
            ]),
            ('Software Engineering Intern – AscentUP', 'Jul. 2026 – Aug. 2026', ascentup),
        ]),
        projects=[('Gomoku AI – RESP Program, Rice University', 'Jun. 2026 – Aug. 2026', gomoku),
                  ('ECODASH – Klein Hacks (3rd Place, Group Innovation)', 'Feb. 2026', ecodash)],
        leadership=leadership,
        skills=[('Languages:', 'Python (NumPy), C++, TypeScript/JavaScript, SQL, HTML/CSS'),
                ('Frameworks & Tools:', 'Next.js, React, Supabase (PostgreSQL), Git/GitHub, Docker, Figma'),
                ('Concepts:', 'Object-oriented design, algorithms (minimax search), machine learning (SVM, Random Forest, '
                              'MiniRocket), debugging and QA testing'),
                ('Activities:', 'RiceApps, HackRice, SHPE, RSA Communications Team')],
    )
    ee = dict(
        file='resume-ee.pdf', contact=contact, links=links, honors=honors,
        coursework='Fundamentals of Computer Engineering (digital logic, computer architecture), Mechanics, Multivariable '
                   'Calculus, Computational Thinking (Python), Bias and Medical Device Design',
        experience=('RESEARCH & ENGINEERING EXPERIENCE', [
            ('Undergraduate Researcher – Yamagami Lab, Rice University', 'Sep. 2026 – Present', [
                'Developing sensing-based gesture recognition so patients with motor disabilities (stroke, Parkinson\'s, spinal-cord '
                'injury) can control XR systems, by processing video-sensing data and training classifiers in '
                + ('Python.' if upd else 'Python and C++.'),
                ('Comparing SVM, Random Forest, and MiniRocket time-series models on a self-recorded dataset of 121 videos across '
                 '3 gestures; all three exceed 95% held-out accuracy in preliminary results presented in lab meetings.'
                 if upd else
                 'Comparing SVM, Random Forest, and MiniRocket time-series models on a self-recorded gesture dataset to select '
                 'the most accurate approach for real-time patient input; present results in lab meetings.'),
            ]),
            ('Software Engineer – RiceApps (NEST360)', 'Sep. 2026 – Present', nest),
            ('Software Engineering Intern – AscentUP', 'Jul. 2026 – Aug. 2026', ascentup),
        ]),
        projects=[('Gomoku AI – RESP Program, Rice University', 'Jun. 2026 – Aug. 2026', gomoku),
                  ('ECODASH – Klein Hacks (3rd Place, Group Innovation)', 'Feb. 2026', ecodash)],
        leadership=leadership,
        skills=[('Hardware & Signals:', 'Arduino, sensor integration, video/time-series sensing data, digital logic, computer architecture'),
                ('Programming:', 'C++, Python (NumPy), SQL, TypeScript/JavaScript'),
                ('Data & ML:', 'Signal-based classification (SVM, Random Forest, MiniRocket), model evaluation, data analysis'),
                ('Tools:', 'Git/GitHub, Docker, Supabase'),
                ('Activities:', 'SHPE, RiceApps, Owl Edge Externship with GE Vernova (Winter 2026)')],
    )
    return [swe, ee]


def render(spec, out_dir):
    p = Page(Path(out_dir) / spec['file'], 'Ahad Rahman - Resume')
    p.name('Ahad Rahman', spec['contact'], spec['links'])
    p.section('EDUCATION', first=True)
    p.row('Rice University', 'Houston, TX')
    p.row('Bachelor of Science, Electrical and Computer Engineering', 'Expected May 2030', font='Serif-Italic')
    p.labeled('Honors:', spec['honors'])
    p.labeled('Coursework:', spec['coursework'])
    title, entries = spec['experience']
    for heading, block in [(title, entries), ('PROJECTS', spec['projects']), ('LEADERSHIP', spec['leadership'])]:
        p.section(heading)
        for left, right, bullets in block:
            p.row(left, right)
            for b in bullets:
                p.bullet(b)
    p.section('TECHNICAL SKILLS')
    for label, text in spec['skills']:
        p.labeled(label, text)
    return p.save()


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--public']
    out, version = args[0], (args[1] if len(args) > 1 else 'updated')
    public = '--public' in sys.argv
    Path(out).mkdir(parents=True, exist_ok=True)
    for spec in content(version, public):
        last = render(spec, out)
        print(f"{spec['file']}: last line at {last:.1f} pt from top")
