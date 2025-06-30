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
        'frontend/webassembly-the-fast-lane',
        'frontend/websockets-realtime-communication',
        'frontend/simple-vs-modern-web',
        'frontend/gui-implementation-patterns',
      ],
    },
    {
      type: 'category',
      label: '⚙️ Backend Development',
      items: [
        'backend/modern-web-scraping',
        'backend/database-architecture',
        'backend/privacy-first-llm-architecture',
        'backend/pattern-based-ai-automation',
        'backend/model-context-protocol-mcp-architecture',
      ],
    },
    {
      type: 'category',
      label: '🔒 Security',
      items: [
        'security/user-agents-and-stealth',
        'security/docker-first-production-security',
      ],
    },
    {
      type: 'category',
      label: '💡 Core Concepts',
      items: [
        'concepts/containerization',
        'concepts/python-project-setup',
        'concepts/failure-driven-development',
        'concepts/testing-like-you-mean-it',
        'concepts/mastering-claude-code',
        'concepts/claude-code-workshop',
        'concepts/modern-dependency-management',
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
      label: '🎯 Learning Plans',
      items: [
        {
          type: 'doc',
          id: 'learning-plans/learning-plans-overview',
          label: '📚 Overview',
        },
        {
          type: 'doc',
          id: 'learning-plans/plan-1-threat-intelligence',
          label: '🕵️ Plan 1: Threat Intelligence',
        },
        {
          type: 'doc',
          id: 'learning-plans/plan-2-static-analysis',
          label: '🔍 Plan 2: Static Analysis',
        },
        {
          type: 'doc',
          id: 'learning-plans/plan-3-api-security',
          label: '🛡️ Plan 3: API Security',
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