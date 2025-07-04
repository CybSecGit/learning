# Development Skills Laboratory

A comprehensive Development Skills Laboratory on software development, testing, and modern engineering practices covering Python, Go, TypeScript, and practical skills like web scraping. This wiki serves as a living documentation of concepts, learning plans, and exercises.

## Repository Structure

- **`website/`** - The Docusaurus documentation site, containing all learning content, concepts, and exercises.
- **`Makefile`** - Centralized script for all development tasks (setup, testing, linting, Docker, documentation).
- **`docker-compose.yml`** - Defines the multi-service Docker environment for development.

## Getting Started

To get started with the Development Skills Laboratory:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cybsecgit/learning.git
    cd learning
    ```

2.  **Set up the development environment (using Docker):**
    ```bash
    make docker-up
    make docker-shell
    ```
    This will build and start the Docker containers and give you a shell inside the main development environment, with all tools pre-installed.

3.  **Serve the documentation site locally:**
    ```bash
    make docs-serve
    ```
    This will start the Docusaurus site, usually accessible at `http://localhost:3000`.

4.  **Explore the content:** Start with the [Wiki Overview](http://localhost:3000/intro) on the documentation site.

## Content Overview

This laboratory covers a wide range of topics, including:
-   **Frontend Development:** WebAssembly, WebSockets, Modern GUI patterns.
-   **Backend Development:** Web Scraping, Database Architecture, Privacy-First LLM Architectures.
-   **Security:** User Agents & Stealth, Docker-First Production Security.
-   **Core Concepts:** Containerization, Python Project Setup, Failure-Driven Development, Testing, Claude Code Mastery, Dependency Management.
-   **Learning Plans:** Structured paths for Threat Intelligence, Static Analysis, and API Security.
-   **Programming Concepts:** Deep dives into Python, Go, and TypeScript/Deno.

## Origin

This wiki was originally developed as educational content within the [Changelogger project](https://github.com/YOUR_USERNAME/changelogger) and has been split into its own repository for better organization and reusability.
