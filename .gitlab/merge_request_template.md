# Merge Request Template

Thank you for your contribution to the **Flora & Fauna Chatbot** project!

Please ensure you've read our [Contributing Guidelines](../CONTRIBUTING.md) before submitting this merge request.

---

## Title (Semantic Format)

Please use [Conventional Commits](https://conventionalcommits.org/) format:

**Examples:**
- `feat(chatbot): add support for Telugu plant name recognition`
- `fix(ui): resolve image display issue in media gallery`
- `docs(readme): update installation instructions`
- `data: add medicinal plants from Telangana region`
- `chore: update dependencies to latest versions`

---

## Related Issue

**Closes**: #<issue_number>

**Example**: `Closes: #42`

**If no related issue exists, please create one first or explain why this MR is needed.**

---

## Description

### Summary
Provide a short summary of the changes:

<!-- What feature/bug does this MR address? -->
<!-- What changes were made? -->
<!-- Why are these changes necessary? -->

### Type of Change
Please check the relevant option:

- [ ] 🐛 **Bug Fix** - Non-breaking change that fixes an issue
- [ ] ✨ **New Feature** - Non-breaking change that adds functionality
- [ ] 🌱 **Data Contribution** - Adding flora/fauna data or media files
- [ ] 💥 **Breaking Change** - Change that would cause existing functionality to not work
- [ ] 📚 **Documentation** - Documentation only changes
- [ ] 🎨 **UI/UX** - User interface improvements
- [ ] ⚡ **Performance** - Code changes that improve performance
- [ ] 🔧 **Refactoring** - Code changes that neither fix bugs nor add features
- [ ] 🧪 **Tests** - Adding missing tests or correcting existing tests
- [ ] 🌐 **Localization** - Telugu/English language support changes

---

## Changes Made

### Code Changes
<!-- List the main code changes -->
- 
- 
- 

### Data Changes
<!-- If adding data, describe what was added -->
- **Species Added**: 
- **Media Files**: 
- **Location Coverage**: 

### UI/UX Changes
<!-- If changing the interface -->
- 
- 

---

## Testing

### Test Environment
- [ ] **Local Testing** - Tested on local development environment
- [ ] **Production-like** - Tested on staging/production-like environment
- [ ] **Multiple Browsers** - Tested on Chrome, Firefox, Safari
- [ ] **Mobile Testing** - Tested on mobile devices
- [ ] **Bilingual Testing** - Tested with both English and Telugu inputs

### Test Cases
<!-- Describe how you tested your changes -->
- [ ] **Manual Testing**: Describe what you tested manually
- [ ] **Automated Tests**: List any automated tests added/updated
- [ ] **Regression Testing**: Confirmed existing functionality still works
- [ ] **Performance Testing**: Verified no performance degradation

### Test Results
<!-- Paste test outputs, screenshots, or describe results -->

---

## Screenshots/Media

### Before
<!-- Screenshots or descriptions of the state before your changes -->

### After  
<!-- Screenshots or descriptions of the state after your changes -->

### Additional Media
<!-- Any videos, audio samples, or other media demonstrating the changes -->

---

## Bilingual Considerations

**If your changes affect language support:**
- [ ] **English Support** - Functionality works in English
- [ ] **Telugu Support** - Functionality works in Telugu
- [ ] **Mixed Language** - Handles mixed English/Telugu input
- [ ] **Cultural Sensitivity** - Appropriate for diverse users
- [ ] **Translation Quality** - Telugu translations are accurate

---

## Database Impact

**If your changes affect the database:**
- [ ] **Schema Changes** - Database structure modifications
- [ ] **Data Migration** - Requires data migration
- [ ] **Performance Impact** - Database query performance considered
- [ ] **Backup Required** - Database backup recommended before deployment

### Migration Details
<!-- If database changes are needed -->
- **Migration Type**: 
- **Rollback Plan**: 
- **Data Safety**: 

---

## Deployment Considerations

### Environment Variables
- [ ] **New Variables** - Added new environment variables
- [ ] **Updated Variables** - Modified existing environment variables
- [ ] **Documentation Updated** - Environment setup docs updated

### Dependencies
- [ ] **New Dependencies** - Added new packages to requirements.txt
- [ ] **Updated Dependencies** - Updated existing package versions
- [ ] **Removed Dependencies** - Removed unused packages

### Configuration Changes
- [ ] **Streamlit Config** - Changes to .streamlit/ configuration
- [ ] **Supabase Setup** - Database configuration changes
- [ ] **File Structure** - New files or directories added

---

## Code Quality

### Code Review Checklist
- [ ] **Code Style** - Follows project style guidelines (PEP 8)
- [ ] **Documentation** - Functions and classes have docstrings
- [ ] **Error Handling** - Appropriate error handling implemented
- [ ] **Security** - No security vulnerabilities introduced
- [ ] **Performance** - Code is efficient and performant

### Static Analysis
- [ ] **Linting** - Code passes linting checks (flake8)
- [ ] **Formatting** - Code is properly formatted (black, isort)
- [ ] **Type Hints** - Type hints added where appropriate

---

## Breaking Changes

**If this MR introduces breaking changes:**
- [ ] **API Changes** - Changes to function signatures or behavior
- [ ] **Configuration Changes** - Changes to required configuration
- [ ] **Database Schema** - Changes to database structure
- [ ] **File Format Changes** - Changes to data file formats

### Migration Guide
<!-- Instructions for users to adapt to breaking changes -->

---

## Additional Context

### Related MRs
<!-- Link to any related merge requests -->

### References
<!-- Links to documentation, issues, or external resources -->

### Future Work
<!-- Any follow-up work that should be done -->

---

## Reviewer Notes

### Areas of Focus
**Please pay special attention to:**
- 
- 
- 

### Questions for Reviewers
<!-- Any specific questions or concerns -->

### Review Checklist for Maintainers
- [ ] **Functionality** - Feature works as described
- [ ] **Code Quality** - Code meets project standards
- [ ] **Testing** - Adequate testing performed
- [ ] **Documentation** - Documentation updated if needed
- [ ] **Security** - No security issues introduced
- [ ] **Performance** - No performance regressions
- [ ] **Bilingual** - Proper language support if applicable

---

## Final Checklist

Before requesting review:
- [ ] I have read the contributing guidelines
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

---

**Thank you for contributing to the Flora & Fauna Chatbot! 🌿🦋**
