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
      label: '🏠 Wiki Overview',
    },
    {
      type: 'category',
      label: '🎨 Frontend Development',
      items: [
        'frontend/chapter-14-webassembly-the-fast-lane',
        'frontend/chapter-15-websockets-realtime-communication',
        'frontend/chapter-08.5-simple-vs-modern-web',
        'frontend/chapter-08-gui-implementation-patterns',
      ],
    },
    {
      type: 'category',
      label: '⚙️ Backend Development',
      items: [
        'backend/chapter-02-web-scraping',
        'backend/chapter-07-database-architecture',
        'backend/chapter-09-privacy-first-llm-architecture',
        'backend/chapter-11-pattern-based-ai-automation',
        'backend/chapter-12-model-context-protocol-mcp-architecture',
      ],
    },
    {
      type: 'category',
      label: '🔒 Security',
      items: [
        'security/chapter-05-user-agents-and-stealth',
        'security/chapter-13-docker-first-production-security',
      ],
    },
    {
      type: 'category',
      label: '💡 Core Concepts',
      items: [
        'concepts/chapter-00-containerization',
        'concepts/chapter-01-setup',
        'concepts/chapter-03-failure-driven-development',
        'concepts/chapter-04-testing-like-you-mean-it',
        'concepts/chapter-06-mastering-claude-code',
        'concepts/chapter-06.5-claude-code-workshop',
        'concepts/chapter-10-modern-dependency-management',
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