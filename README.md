<<<<<<< HEAD
# flora



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://code.swecha.org/DAYAKAR123/flora.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://code.swecha.org/DAYAKAR123/flora/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# Multi-Media Data Collection App with Location Tracking

A comprehensive Streamlit application for collecting various types of data including text, audio, video, and images with location information for research and internship projects.

## Features

### 📍 Location Tracking
- Manual location entry
- Coordinate input (latitude, longitude)
- Country and city specification
- Location statistics and analytics
- Location data validation

### 📝 Text Data Collection
- Single text entry with categories
- Multi-line text input for longer content
- CSV file upload for bulk data import
- Automatic timestamping and categorization
- Location capture for each entry

### 🎵 Audio Data Collection
- Upload audio files (MP3, WAV, OGG, M4A)
- Audio preview functionality
- Metadata collection (duration, category, description)
- Support for various audio categories
- Location information for each recording

### 🎥 Video Data Collection
- Upload video files (MP4, AVI, MOV, WMV)
- Video preview functionality
- Detailed metadata (duration, resolution, tags)
- Category-based organization
- Location tracking for video content

### 🖼️ Image Data Collection
- Multiple image upload support
- Image preview gallery
- Tagging and categorization system
- Support for various image formats (PNG, JPG, JPEG, GIF, BMP)
- Location data for image capture

### 📈 Data Management
- View all collected data in a unified dashboard
- Filter data by type
- Export data to CSV
- Summary statistics
- Metadata tracking with timestamps
- Location-based analytics and statistics

## Installation

1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the sidebar to select the type of data you want to collect:
   - **📝 Text Data**: Enter text manually or upload CSV files
   - **🎵 Audio Data**: Upload audio recordings
   - **🎥 Video Data**: Upload video files
   - **🖼️ Image Data**: Upload single or multiple images
   - **📈 View Collected Data**: Review and export collected data

4. For each data type, provide location information:
   - Enter location manually (e.g., "New York, NY")
   - Input coordinates (latitude, longitude)
   - Specify country and city
   - View location statistics in the data overview

## Data Storage

All collected data is stored locally in the `data/` directory:
- `data/text/` - Text files and CSV uploads
- `data/audio/` - Audio recordings
- `data/video/` - Video files
- `data/images/` - Image files
- `data/metadata.json` - Metadata for all collected files

## File Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── location_utils.py     # Location processing utilities
├── data_utils.py         # Data processing utilities
├── analytics.py          # Analytics dashboard
├── config.py             # Configuration settings
└── data/                 # Data storage directory (created automatically)
    ├── text/
    ├── audio/
    ├── video/
    ├── images/
    └── metadata.json
```

## Features in Detail

### Metadata Tracking
Each uploaded file includes comprehensive metadata:
- Timestamp of upload
- Data type and category
- Original filename
- Location information (manual entry, coordinates, country/city)
- Additional attributes (duration, resolution, tags, etc.)
- Custom descriptions and notes

### Location Features
- **Manual Entry**: Type your current location
- **Coordinates**: Enter GPS coordinates
- **Country/City**: Specify geographic details
- **Statistics**: View location-based analytics
- **Validation**: Coordinate format checking
- **Export**: Location data included in CSV exports

### User Interface
- Clean, intuitive interface with clear navigation
- Responsive design that works on different screen sizes
- Real-time preview of uploaded content
- Progress indicators and success messages
- Organized layout with helpful instructions

### Data Export
- Export metadata to CSV format
- Filter data before export
- Download collected data summaries
- Comprehensive data overview dashboard

## Customization

You can easily customize the application by:
- Adding new data categories in the selectbox options
- Modifying the metadata fields collected
- Changing the file storage structure
- Adding new data types or input methods

## Requirements

- Python 3.7+
- Streamlit 1.28.1+
- Pandas 2.1.1+
- Matplotlib 3.7.1+
- Requests 2.31.0+
- Standard Python libraries (os, datetime, pathlib, json)

## License

This project is created for educational and internship purposes.
>>>>>>> 5fc8c29 (Data Collection tool)
