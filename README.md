# Smart File Organizer

Organize, inspect, and find files using Google Gemini AI.

## Installation

```bash
conda env create -f environment.yml
conda activate file-organizer
```

## Setup

Create a `.env` file and add your key:
```
GEMINI_API_KEY=your_key_here
```

## Usage

```bash
python src/main.py
```

### Commands
- `organize`: Sorts files into folders by content.
- `inspect`: AI summary of file contents.
- `find`: Find file by description.
