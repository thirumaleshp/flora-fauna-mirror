# Contributing to Flora & Fauna Chatbot

Thank you for your interest in contributing to the Flora & Fauna Chatbot project! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Data Contribution Guidelines](#data-contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.8 or higher
- Git installed
- Basic knowledge of Streamlit, pandas, and Supabase
- Familiarity with bilingual applications (English/Telugu support)

### First Time Contributors

1. **Fork the repository** on GitLab
2. **Clone your fork** locally:
   ```bash
   git clone https://code.swecha.org/YOUR_USERNAME/flora.git
   cd flora
   ```
3. **Set up the upstream remote**:
   ```bash
   git remote add upstream https://code.swecha.org/DAYAKAR123/flora.git
   ```

## 🛠️ Development Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

1. **Supabase Setup**: Follow `CREATE_OWN_SUPABASE.md` for database setup
2. **Environment Variables**: Copy `secrets.template.toml` to `.streamlit/secrets.toml` and fill in your credentials
3. **Test Connection**: Run `python test_supabase.py` to verify setup

### 3. Running the Application

```bash
# Run the main application
streamlit run app.py

# Run deployment check
python check_deployment.py

# Test bilingual functionality
python test_bilingual.py
```

## 📝 Contributing Guidelines

### Types of Contributions

We welcome the following types of contributions:

1. **🌱 Data Contributions**: Add flora and fauna data, images, videos, audio recordings (HIGHEST PRIORITY)
2. **🐛 Bug Fixes**: Fix existing issues or bugs
3. **✨ New Features**: Add new functionality (please discuss in an issue first)
4. **📚 Documentation**: Improve or expand documentation
5. **🌐 Localization**: Add support for new languages
6. **🎨 UI/UX Improvements**: Enhance user interface and experience
7. **⚡ Performance**: Optimize code performance
8. **🧪 Testing**: Add or improve tests

### Areas for Contribution

#### Highest Priority - Data Contributions 🌱
- **Flora Data**: Plant species information, scientific names, local names (Telugu/English)
- **Fauna Data**: Animal species information, behavior patterns, habitat details
- **Media Files**: High-quality images, videos, audio recordings of plants and animals
- **Location Data**: Geographic information, GPS coordinates, habitat descriptions
- **Cultural Information**: Traditional uses, folklore, local knowledge
- **Seasonal Data**: Flowering seasons, migration patterns, breeding cycles

#### High Priority
- **Bilingual Support**: Improve Telugu language processing
- **Media Handling**: Enhance image/video/audio display
- **Search Algorithm**: Improve keyword extraction and matching
- **Error Handling**: Add robust error handling
- **Performance**: Database query optimization

#### Medium Priority
- **UI/UX**: Streamlit interface improvements
- **Documentation**: API documentation and guides
- **Testing**: Unit and integration tests
- **Accessibility**: Screen reader and keyboard navigation support

#### Low Priority
- **Additional Languages**: Support for more Indian languages
- **Export Features**: Data export functionality
- **Analytics**: Usage statistics and insights

## 🌱 Data Contribution Guidelines

**Data contributions are the most valuable contributions to this project!** We encourage researchers, students, botanists, zoologists, and nature enthusiasts to add their flora and fauna data.

### What Data We Need

#### Flora (Plant) Data
- **Species Information**: Scientific names, common names, family classification
- **Local Names**: Telugu names, regional variations, traditional names
- **Physical Description**: Size, color, leaf shape, flower characteristics
- **Habitat Information**: Soil type, climate requirements, natural distribution
- **Uses**: Medicinal uses, cultural significance, economic importance
- **Conservation Status**: Endangered, rare, or common species status

#### Fauna (Animal) Data  
- **Species Information**: Scientific names, common names, classification
- **Local Names**: Telugu names, regional bird/animal names
- **Behavior**: Feeding habits, migration patterns, social behavior
- **Habitat**: Natural habitat, nesting preferences, territory requirements
- **Conservation**: Population status, threats, protection measures
- **Cultural Significance**: Role in local culture, folklore, traditions

#### Media Files
- **High-Quality Images**: Clear photos of plants/animals in natural habitat
- **Videos**: Behavior recordings, growth time-lapses, feeding videos
- **Audio**: Bird calls, animal sounds, environmental recordings
- **File Requirements**: 
  - Images: JPG/PNG, min 1024x768, max 10MB
  - Videos: MP4, max 50MB, good lighting and focus
  - Audio: MP3/WAV, clear sound, max 20MB

#### Location Data
- **GPS Coordinates**: Precise location where species was observed
- **Geographic Region**: State, district, specific area names
- **Habitat Description**: Forest type, elevation, nearby landmarks
- **Date/Time**: When the observation was made
- **Weather Conditions**: Climate during observation

### How to Contribute Data

#### Method 1: Using the Web Application
1. Run the Flora & Fauna app: `streamlit run app.py`
2. Navigate to "📊 Data Collection" section
3. Fill in the species information form
4. Upload images/videos/audio files
5. Add location and habitat details
6. Submit your data entry

#### Method 2: Database Direct Entry
1. Contact maintainers for database access
2. Follow the database schema in `COMPLETE_SETUP.sql`
3. Use the provided data templates
4. Ensure data quality and completeness

#### Method 3: Bulk Data Submission
1. Prepare data in CSV format using our template
2. Contact maintainers with your dataset
3. We'll help import your bulk data
4. Perfect for research organizations and institutions

### Data Quality Standards

#### Required Information
- **Scientific Name**: Must be accurate and current
- **Location**: At least state/region level
- **Date**: When observation was made
- **Source**: Who provided the information

#### Recommended Information
- **Local Names**: Telugu and English common names
- **Images**: At least one clear photograph
- **Habitat Details**: Environmental conditions
- **Uses**: Traditional or modern applications

#### Data Validation
- **Accuracy**: Cross-reference with botanical/zoological databases
- **Originality**: Ensure you have rights to images/videos
- **Attribution**: Credit photographers and researchers
- **Verification**: Include references or expert verification

### Example Data Entry

```json
{
  "scientific_name": "Prosopis cineraria",
  "common_names": {
    "english": ["Khejri", "Ghaf", "Shami"],
    "telugu": ["జమ్మి చెట్టు", "షమి"]
  },
  "family": "Fabaceae",
  "description": "Drought-resistant tree native to arid regions",
  "habitat": "Semi-arid regions, sandy soils",
  "location": {
    "state": "Telangana",
    "district": "Rangareddy",
    "coordinates": "17.3850° N, 78.4867° E"
  },
  "uses": ["Medicinal", "Fodder", "Timber"],
  "conservation_status": "Least Concern",
  "cultural_significance": "Sacred tree in Hindu traditions"
}
```

### Data Contribution Recognition

- **Data Contributors**: Listed in project credits
- **Major Contributors**: Special recognition in documentation
- **Research Citations**: Academic publications will cite data sources
- **Community Impact**: Help preserve biodiversity knowledge

### Getting Started with Data Contribution

1. **Start Small**: Begin with species you know well
2. **Use Mobile App**: Collect data during field trips
3. **Join Community**: Connect with other contributors
4. **Ask Questions**: Contact maintainers for guidance
5. **Share Knowledge**: Help others learn about local flora/fauna

## 🔄 Pull Request Process

### Before Submitting

1. **Check existing issues** to avoid duplication
2. **Create an issue** for new features or major changes
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Follow code style** guidelines

### Pull Request Steps

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, focused commits:
   ```bash
   git add .
   git commit -m "feat: add bilingual keyword mapping for trees"
   ```

3. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitLab with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Test results

### Commit Message Format

Use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
- `feat(chatbot): add Telugu plant name recognition`
- `fix(ui): resolve image display issue in media section`
- `docs(readme): update installation instructions`

## 🐛 Issue Reporting

### Bug Reports

When reporting bugs, please include:

1. **Bug Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, browser
6. **Screenshots**: If applicable
7. **Error Messages**: Full error logs

### Feature Requests

For new features, please include:

1. **Feature Description**: Clear description of the proposed feature
2. **Use Case**: Why this feature would be useful
3. **Proposed Solution**: How you think it should work
4. **Alternatives**: Other solutions you've considered
5. **Additional Context**: Screenshots, mockups, or examples

## 🏗️ Development Workflow

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes

### Development Process

1. **Pick an Issue**: Choose from open issues or create one
2. **Discuss**: Comment on the issue to discuss approach
3. **Develop**: Work on your feature branch
4. **Test**: Ensure all tests pass
5. **Review**: Submit PR for code review
6. **Merge**: Maintainer merges after approval

## 🎨 Code Style

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation
- Maximum line length: **88 characters** (Black formatter)
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes

### Code Formatting

We use automated formatting tools:

```bash
# Install formatting tools
pip install black isort flake8

# Format code
black .
isort .

# Check style
flake8 .
```

### File Organization

```
├── app.py                 # Main Streamlit application
├── chatbot.py            # Chatbot logic and functionality
├── supabase_db.py        # Database operations
├── data_utils.py         # Data processing utilities
├── config.py             # Configuration management
├── tests/                # Test files
├── docs/                 # Documentation
└── .streamlit/           # Streamlit configuration
```

## 🧪 Testing

### Test Structure

```
tests/
├── test_chatbot.py       # Chatbot functionality tests
├── test_database.py      # Database operation tests
├── test_bilingual.py     # Language processing tests
└── test_ui.py           # UI component tests
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_chatbot.py

# Run with coverage
python -m pytest --cov=. tests/
```

### Test Guidelines

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **UI Tests**: Test user interface elements
- **Bilingual Tests**: Test language-specific functionality

## 📚 Documentation

### Documentation Standards

- **Clear and Concise**: Write in simple, understandable language
- **Examples**: Provide code examples where helpful
- **Up-to-date**: Keep documentation current with code changes
- **Bilingual**: Include Telugu examples where relevant

### Documentation Types

1. **API Documentation**: Function and class docstrings
2. **User Guides**: How to use the application
3. **Developer Guides**: Setup and development instructions
4. **Deployment Guides**: Production deployment steps

## 🌟 Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **Release Notes**: Major contribution highlights
- **Project Wiki**: Detailed contribution history

## 📞 Getting Help

### Communication Channels

- **Issues**: For bugs and feature requests
- **Discussions**: For general questions and ideas
- **Email**: For sensitive matters

### Maintainers

- **Thirumalesh Pinninti**: Project maintainer
- **DAYAKAR123**: Repository owner

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (GNU Affero General Public License v3.0).

## 🎯 Quick Start Checklist

### For Data Contributors (Recommended)
- [ ] Review data contribution guidelines
- [ ] Set up the application locally
- [ ] Start with species you know well
- [ ] Prepare images/videos/audio files
- [ ] Add flora or fauna data through the app
- [ ] Share your local knowledge

### For Code Contributors
- [ ] Fork the repository
- [ ] Set up development environment
- [ ] Read contributing guidelines
- [ ] Pick an issue or create one
- [ ] Create feature branch
- [ ] Make changes and test
- [ ] Submit pull request
- [ ] Respond to review feedback

## 🙏 Thank You

Thank you for contributing to the Flora & Fauna Chatbot project! Your contributions help make this tool better for researchers, students, and nature enthusiasts around the world.

---

**Happy Contributing! 🌿🦋**
