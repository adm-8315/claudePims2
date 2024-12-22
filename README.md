# Claude PIMS2 Project

This repository is dedicated to the PIMS2 project integration with Claude AI.

## Project Structure

- `src/pims2_claude/`: Main package directory
  - `config.py`: Configuration management
  - `interface.py`: PIMS2-Claude interface implementation
- `tests/`: Test directory
  - `test_interface.py`: Interface tests

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Development

This project is under active development. Key features will include:
- PIMS2 system integration
- Claude AI communication interface
- Data processing and transformation
- Configuration management

## Testing

Run tests using pytest:
```bash
pytest tests/
```