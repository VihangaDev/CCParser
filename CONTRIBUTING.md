# Contributing to CCParser

Thank you for considering contributing to CCParser! We welcome all contributions, whether it's reporting a bug, improving documentation, adding a feature, or fixing an issue. Follow the guidelines below to ensure a smooth contribution process.

## 🛠 How to Contribute

### 1. Fork the Repository

- Click the **Fork** button on the top right of the repository page.
- Clone your fork locally:

  ```bash
  git clone https://github.com/your-username/CCParser.git
  cd CCParser
  ```

### 2. Set Up Development Environment

- Create a virtual environment:

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- Install in development mode with all dependencies:

  ```bash
  pip install -e ".[dev,api]"
  ```

### 3. Create a New Branch

- Always work in a new branch for each contribution:

  ```bash
  git checkout -b feature-or-fix-name
  ```

### 4. Make Your Changes

- Follow best practices and ensure your code is clean and documented.
- Stick to the existing code style.
- Add type hints to all new functions and methods.
- Write docstrings for all public functions and classes.
- Test your changes thoroughly.

### 5. Run Tests

- Make sure all tests pass before submitting:

  ```bash
  pytest
  ```

- Run linting:

  ```bash
  flake8 ccparser tests
  ```

### 6. Commit Your Changes

- Write clear, concise commit messages:

  ```bash
  git add .
  git commit -m "Brief description of changes"
  ```

### 7. Push to Your Fork

- Push your changes to your forked repository:

  ```bash
  git push origin feature-or-fix-name
  ```

### 8. Create a Pull Request

- Go to the original CCParser repository.
- Click on the **Pull Requests** tab.
- Click **New Pull Request** and select your branch.
- Provide a meaningful title and description of your changes.
- Submit the pull request for review.

## 📝 Contribution Guidelines

- Follow the [PEP 8](https://peps.python.org/pep-0008/) coding style guide.
- Keep PRs focused and minimal; avoid including unrelated changes.
- Write descriptive commit messages.
- Ensure all functions and classes have proper docstrings.
- Add type hints to all function signatures.
- If adding a new feature, update the documentation accordingly.
- Include tests for new functionality.

## 🐞 Reporting Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/VihangaDev/CCParser/issues) and provide:

- A clear title and description.
- Steps to reproduce (if it's a bug).
- Expected vs. actual behavior.
- Any relevant logs or screenshots.

## 🏆 Thank You

Your contributions help improve CCParser and make it better for everyone. Thank you for your support! 🚀
