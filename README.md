# Textify

## Overview
Welcome to _**Textify**_! _**Textify**_ extracts text from images and compiles them into searchable _**PDFs**_, facilitating efficient _**Document Management**_ and accessibility in applications requiring _**Image Text Extraction**_. Whether you are a developer or contributor, this _**README.md**_ will guide you through the essentials of the project.

## Table of Content
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Contribution](#contribution)

## Introduction
_**Textify**_ leverages _**EasyOCR**_ for _**Image Text Extraction**_, integrates _**OpenAI's**_ language model for text formatting, and converts the extracted text into _**PDFs**_. It offers a seamless solution for converting images to formatted _**PDF Documents**_ with enhanced accuracy and efficiency.

## Getting Started
Before diving into the project, ensure you have the following prerequisites:
- Programming Language: [Python 3.X](https://www.python.org/)
- Package Manager: [pip](https://pypi.org/project/pip/)
- Version Control: [Git](https://git-scm.com/)
- Integrated Development Environment: [Visual Studio Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/)

## Installation

1. Clone Repository
   ```bash
   https://github.com/Arko-Sengupta/Textify.git
   ```
2. Navigate to the Project Directory
   ```bash
   cd/<Project-Directory>
   ```

3. Create `.env.local` inside `<Project-Directory>`.

4. Add below to `.env.local` file
   ```bash
   API_KEY=<Your-OpenAI-API-Key>
   ```

5. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

6. Start Backend Server
   ```bash
   python ImageToFormat_API.py
   ```

7. Confirm Server Start: Open the below URL at Browser: [http://localhost:5000/](http://localhost:5000/)

8. Start the Application
   ```bash
   streamlit run App.py
   ```

## Contribution
If you'd like to contribute, follow the guidelines
- Create a branch using the format `Textify_<YourUsername>` when contributing to the project.
- Add the label `Contributor` to your contributions to distinguish them within the project.