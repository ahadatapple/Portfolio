// Facts shown on the home page. Every value here comes from your résumés or
// from what you confirmed. Optional fields render only when they are set.

export const profile = {
  name: 'Ahad Rahman',
  hero: 'I build software and machine-learning systems, and I test them until the numbers hold.',
  identity: [
    'Electrical and Computer Engineering, Rice University ’30',
    'Incoming Amazon intern, Summer 2027',
    'Gates Scholar',
    'Amazon Future Engineer Scholar',
  ],
  location: 'Houston, TX',
  email: 'aar15@rice.edu',
  linkedin: 'https://www.linkedin.com/in/ahad-rahman-rice',
  github: 'https://github.com/ahadatapple' as string | null,
  resume: '/resume.pdf',
  resumeEE: '/resume-ee.pdf',
};

export const meta = {
  title: 'Ahad Rahman · Software and ML engineering',
  description:
    'First-year ECE student at Rice. Gesture recognition for accessible XR, a Gomoku engine, and production QA, each with its numbers.',
};

export interface ShortCard {
  title: string;
  context: string;
  dates: string;
  body: string;
  links: { label: string; href: string }[];
}

export const alsoShipped: ShortCard[] = [
  {
    title: 'NEST360 resources page',
    context: 'RiceApps',
    dates: 'Sep 2026 to present',
    body: 'A redesigned resources page for NEST360, a newborn-health nonprofit. I implemented the Figma design with topic filtering, sorting and colour-coded tags, and built reusable gallery components with a student team. Six pull requests merged through code review.',
    links: [],
  },
  {
    title: 'ECODASH',
    context: 'Klein Hacks',
    dates: 'Feb 2026',
    body: 'A marketplace that matches unwanted items with neighbors, haulers and recyclers. Built and pitched in Next.js, React, TypeScript and Supabase within the hackathon time limit. 3rd place, Group Innovation.',
    links: [],
  },
];

export const skills: { skill: string; evidence: string }[] = [
  { skill: 'Python, NumPy', evidence: 'Gomoku engine, gesture pipeline' },
  { skill: 'Machine learning (SVM, Random Forest, MiniRocket)', evidence: 'Gesture recognition' },
  { skill: 'Game-tree search, heuristic design', evidence: 'Gomoku engine' },
  { skill: 'Next.js, React, TypeScript', evidence: 'ECODASH, AscentUP fixes' },
  { skill: 'SQL, Supabase (PostgreSQL)', evidence: 'AscentUP, ECODASH' },
  { skill: 'Docker, Git, debugging and QA', evidence: 'AscentUP' },
  { skill: 'Figma to code, frontend components', evidence: 'NEST360' },
];

export const about: string[] = [
  'I am a first-year Electrical and Computer Engineering student at Rice University, graduating in May 2030. I do research in the Yamagami Lab on gesture recognition for accessible XR, write frontend code for RiceApps, and will intern at Amazon in Summer 2027.',
  'I work the same way on every project. I build the thing, build a way to measure it, and report what the measurement says, including where it falls short. Every Gomoku change ran through a 20-game tournament. The AscentUP bug reports have SQL checks behind them. The gesture results state how many recordings were held out.',
];

export interface Role {
  title: string;
  org: string;
  dates: string;
  body: string;
}

export const experience: Role[] = [
  {
    title: 'Incoming Intern',
    org: 'Amazon',
    dates: 'Summer 2027',
    body: '',
  },
  {
    title: 'Undergraduate Researcher',
    org: 'Yamagami Lab, Rice University',
    dates: 'Sep 2026 to present',
    body: 'Building a gesture-recognition pipeline for accessible XR input. Recorded and processed a dataset of 121 gesture videos. Comparing SVM, Random Forest and MiniRocket classifiers in Python. Present results in lab meetings.',
  },
  {
    title: 'Software Engineer',
    org: 'RiceApps (NEST360)',
    dates: 'Sep 2026 to present',
    body: 'Shipped a redesigned resources page for a newborn-health nonprofit from a Figma design, with topic filtering, sorting and colour-coded tags. Built reusable gallery components. Six pull requests merged through code review.',
  },
  {
    title: 'Software Engineering Intern',
    org: 'AscentUP',
    dates: 'Jul to Aug 2026',
    body: 'Worked on the web app of a health startup AscentUP partnered with. Ran QA across 7 modules of its Next.js and Supabase app using UI testing, code tracing and SQL checks against a 41-table database, and found 20 bugs. Resolved 6 Docker, Supabase and Git environment blockers. Shipped 2 production fixes and documented each fix for the team.',
  },
  {
    title: 'Rice Emerging Scholars Program',
    org: 'Rice University',
    dates: 'Jun to Aug 2026',
    body: 'Built a Gomoku engine in Python with a hand-written evaluation. Found a weak opening by playtesting and fixed it, taking the engine from 14 of 20 to 20 of 20 against the hardest bot from an empty board. Presented at Rice’s STEM Symposium in one of 38 first-year spots.',
  },
];

export const education = {
  school: 'Rice University',
  degree: 'B.S. Electrical and Computer Engineering',
  dates: 'Expected May 2030',
  coursework:
    'Computational Thinking (Python), Fundamentals of Computer Engineering (digital logic, computer architecture), Multivariable Calculus, Mechanics, Bias and Medical Device Design.',
};

export const honors: string[] = [
  'Gates Scholar',
  'Amazon Future Engineer Scholar',
  'Rice Emerging Scholars Program',
  '3rd place, Group Innovation, Klein Hacks 2026',
  'Owl Edge Externship with GE Vernova, Winter 2026',
  'RiceApps, HackRice, SHPE, RSA Communications Team',
];
