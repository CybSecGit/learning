/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  courseSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '🏠 Course Overview',
    },
    {
      type: 'category',
      label: '📚 Chapters',
      items: [
        'chapters/chapter-00-containerization',
        'chapters/chapter-01-setup',
        'chapters/chapter-02-web-scraping',
        'chapters/chapter-03-failure-driven-development',
        'chapters/chapter-04-testing-like-you-mean-it',
        'chapters/chapter-05-user-agents-and-stealth',
        'chapters/chapter-06-mastering-claude-code',
        'chapters/chapter-06.5-claude-code-workshop',
        'chapters/chapter-07-database-architecture',
        'chapters/chapter-08-gui-implementation-patterns',
        'chapters/chapter-08.5-simple-vs-modern-web',
        'chapters/chapter-09-privacy-first-llm-architecture',
        'chapters/chapter-10-modern-dependency-management',
        // 'chapters/chapter-11-pattern-based-ai-automation',
        // 'chapters/chapter-12-model-context-protocol-mcp-architecture',
        'chapters/chapter-13-docker-first-production-security',
      ],
    },
    {
      type: 'category',
      label: '🧪 Exercises',
      items: [
        {
          type: 'doc',
          id: 'exercises/claude-code-exercises',
          label: 'Claude Code Exercises',
        },
        {
          type: 'doc',
          id: 'exercises/language-exercises',
          label: 'Language-Specific Exercises',
        },
        {
          type: 'doc',
          id: 'exercises/debugging-exercise',
          label: 'Debugging Challenge',
        },
      ],
    },
    {
      type: 'category',
      label: '📖 Learning Concepts',
      items: [
        {
          type: 'doc',
          id: 'concepts/python-concepts',
          label: '🐍 Python Concepts',
        },
        {
          type: 'doc',
          id: 'concepts/golang-concepts',
          label: '🐹 Go Concepts',
        },
        {
          type: 'doc',
          id: 'concepts/typescript-deno-concepts',
          label: '🦕 TypeScript/Deno Concepts',
        },
      ],
    },
    {
      type: 'category',
      label: '🔧 Resources',
      items: [
        'debugging-journey',
        {
          type: 'doc',
          id: 'resources/docker-quick-start',
          label: '🐳 Docker Quick Start',
        },
        {
          type: 'doc',
          id: 'resources/security-note',
          label: '🔒 Security Guidelines',
        },
        {
          type: 'doc',
          id: 'resources/contributing',
          label: '🤝 Contributing Guide',
        },
      ],
    },
  ],
};

module.exports = sidebars;