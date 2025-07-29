# Changelog

All notable changes to the Flora & Fauna Chatbot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md file for version tracking
- CONTRIBUTING.md with comprehensive data contribution guidelines

### Changed
- Updated project documentation structure

## [2.1.0] - 2025-01-29

### Added
- 🌱 **Data Contribution Focus**: Emphasized data contributions as highest priority
- 📋 **CONTRIBUTING.md**: Comprehensive contributor guidelines
- 🔍 **Deployment Check Script**: `check_deployment.py` for environment validation
- 🛡️ **Error Handling**: Robust handling for missing dependencies (pandas, supabase)
- 📄 **LICENSE**: GNU Affero General Public License v3.0

### Enhanced
- 🤖 **Chatbot Interface**: Improved user experience and error handling
- 🔧 **Dependency Management**: Graceful degradation when dependencies are missing
- 📚 **Documentation**: Updated setup and deployment guides

### Fixed
- 🐛 **Import Errors**: Better handling of missing pandas dependency
- 🔄 **Session State**: Improved Streamlit session state management
- 🎯 **Error Messages**: More user-friendly error messages

## [2.0.0] - 2025-01-28

### Added
- 🌍 **Bilingual Support**: Complete English and Telugu language support
- 🎵 **Media Integration**: Support for images, videos, and audio files
- 🔍 **Enhanced Search**: Improved keyword extraction and database search
- 🏠 **Default Landing Page**: AI Chatbot as the main interface
- 📱 **Responsive Design**: Better mobile and desktop experience

### Enhanced
- 🧠 **AI Chatbot**: Advanced natural language processing
- 🔤 **Keyword Mapping**: Bilingual plant and animal name recognition
- 📊 **Database Integration**: Optimized Supabase queries
- 🎨 **User Interface**: Cleaner, more intuitive design
- 🚀 **Performance**: Faster response times and caching

### Changed
- ♻️ **Code Cleanup**: Removed unnecessary debug prints and unused variables
- 🗑️ **UI Simplification**: Removed suggestion buttons for cleaner interface
- 📐 **Project Structure**: Better organized codebase

### Removed
- 🧹 **Unused Code**: Cleaned up redundant functions and variables
- 📝 **Debug Output**: Removed development-only print statements

## [1.5.0] - 2025-01-27

### Added
- 🤖 **Flora & Fauna Chatbot**: Initial AI assistant implementation
- 💾 **Database Caching**: 5-minute cache for improved performance
- 🔧 **Session Management**: Conversation history tracking
- 📱 **Streamlit Interface**: Web-based user interface

### Enhanced
- 🗃️ **Database Queries**: Optimized search algorithms
- 🎯 **Relevance Scoring**: Better result ranking system
- 📝 **Response Generation**: Natural language responses

### Fixed
- 🔌 **Database Connection**: Improved connection stability
- 🐛 **Error Handling**: Better exception management

## [1.4.0] - 2025-01-26

### Added
- 🌐 **Supabase Integration**: Cloud database connectivity
- 📊 **Data Collection Interface**: Web form for data entry
- 📍 **Location Services**: GPS coordinate capture
- 🖼️ **Media Upload**: Image and file upload functionality

### Enhanced
- 🏗️ **Database Schema**: Comprehensive flora and fauna tables
- 🔐 **Security**: Row Level Security (RLS) implementation
- 📱 **Mobile Support**: Better mobile data collection experience

### Fixed
- 🔧 **Configuration**: Environment variable management
- 📤 **File Upload**: Improved file handling and validation

## [1.3.0] - 2025-01-25

### Added
- 🗄️ **MongoDB Atlas**: Alternative database option
- 📈 **Analytics Dashboard**: Basic usage statistics
- 🔄 **Data Synchronization**: Multi-database support
- 🛡️ **Data Validation**: Input validation and sanitization

### Enhanced
- 🎯 **Search Functionality**: Improved search algorithms
- 📊 **Data Visualization**: Better charts and graphs
- 🔧 **Configuration Management**: Centralized config system

### Fixed
- 🐛 **Data Import**: Fixed bulk data import issues
- 🔌 **Connection Pooling**: Improved database connection management

## [1.2.0] - 2025-01-24

### Added
- 📱 **Mobile Interface**: Responsive design for mobile devices
- 🌍 **Offline Mode**: Basic offline functionality
- 📤 **Data Export**: CSV and JSON export options
- 🔍 **Advanced Search**: Filter and sort capabilities

### Enhanced
- 🎨 **User Interface**: Improved visual design
- ⚡ **Performance**: Faster loading times
- 📝 **Data Entry**: Better form validation

### Fixed
- 🐛 **Image Display**: Fixed image rendering issues
- 📱 **Mobile Bugs**: Resolved mobile-specific problems

## [1.1.0] - 2025-01-23

### Added
- 🖼️ **Image Gallery**: Browse uploaded images
- 📝 **Rich Text Editor**: Better content editing
- 🏷️ **Tagging System**: Categorize entries with tags
- 🔔 **Notifications**: User feedback system

### Enhanced
- 📊 **Dashboard**: Improved data overview
- 🔍 **Search**: Better search results
- 📱 **Navigation**: Streamlined user flow

### Fixed
- 🔧 **File Upload**: Resolved upload failures
- 🎨 **CSS Issues**: Fixed styling problems

## [1.0.0] - 2025-01-22

### Added
- 🌱 **Initial Release**: Basic flora and fauna data collection
- 📊 **Data Entry Forms**: Web forms for species information
- 🗃️ **Database Storage**: Local data storage
- 📷 **Image Upload**: Basic image attachment
- 🔍 **Search Function**: Simple text search
- 📱 **Streamlit App**: Web application interface

### Features
- **Species Information**: Scientific and common names
- **Location Data**: Geographic information capture
- **Basic UI**: Simple, functional interface
- **Data Validation**: Input checking and validation

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes
- **Enhanced** for improvements to existing features

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Contributing to Changelog

When contributing to this project:

1. **Add entries** to the "Unreleased" section
2. **Use appropriate categories** (Added, Changed, Fixed, etc.)
3. **Include emoji prefixes** for visual clarity
4. **Reference issues** when applicable: `fixes #123`
5. **Keep descriptions concise** but informative

## Release Process

1. Move items from "Unreleased" to new version section
2. Update version numbers in code
3. Tag the release in Git
4. Deploy to production
5. Announce the release

---

**Note**: This changelog is maintained manually. For detailed commit history, see the Git log.
