
# Contributing to flyby-fingerprints-sandbox

Thank you for considering contributing to this project!
This repository is a sandbox environment for analyzing heating-rate datasets of trapped ions to identify fingerprints of fly-by (residual-gas) collisions.

---

## Maintainer
Ulrich Warring
University of Freiburg

---

## How to Contribute

### 1. Set up the environment
You can use either **conda** or **pip**:

**Conda (recommended):**
```bash
conda env create -f environment.yml
conda activate flyby-fingerprints
```

**Pip:**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2. Fork and clone the repository
- Fork the repository on GitHub.
- Clone your fork locally:
```bash
git clone https://github.com/<your-username>/flyby-fingerprints-sandbox.git
```

### 3. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make your changes
- Add or modify analysis scripts, data schemas, or documentation.
- Ensure that existing functionality still works.
- Run `python tools/format_gate.py` to check formatting and linting.
- Run `pytest` to execute the test suite.

### 5. Commit and push
```bash
git add .
git commit -m "Describe your changes clearly"
git push origin feature/your-feature-name
```

### 6. Open a Pull Request
- On GitHub, open a pull request from your branch into `main`.
- Describe the purpose of your contribution and any relevant details.

---

## Code of Conduct
- Be respectful, collaborative, and transparent.
- All contributions must be released under the GPLv3 license.
- Provide clear documentation for any new analysis or data formats.

---

Thank you for helping to make this sandbox a robust community resource!
