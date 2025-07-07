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
    // Getting Started
    {
      type: 'category',
      label: '🚀 Getting Started',
      collapsed: false,
      items: [
        'intro',
        'resources/docker-quick-start',
        'concepts/python-project-setup',
        'concepts/containerization',
      ],
    },
    
    // Core Development Concepts
    {
      type: 'category',
      label: '📚 Core Concepts',
      collapsed: true,
      items: [
        'concepts/failure-driven-development',
        'concepts/testing-like-you-mean-it',
        'concepts/modern-dependency-management',
        'debugging-journey',
      ],
    },
    
    // Development Tools & AI
    {
      type: 'category',
      label: '🤖 Development Tools',
      collapsed: true,
      items: [
        'concepts/mastering-claude-code',
        'concepts/claude-code-workshop',
        'concepts/mastering-gemini-cli',
        'concepts/playwright-mcp-mastery',
      ],
    },
    
    // Technical Topics (with subcategories)
    {
      type: 'category',
      label: '💻 Technical Topics',
      collapsed: true,
      items: [
        // Frontend
        {
          type: 'category',
          label: '🎨 Frontend Development',
          collapsed: true,
          items: [
            'frontend/gui-implementation-patterns',
            'frontend/webassembly-the-fast-lane',
            'frontend/websockets-realtime-communication',
            'frontend/simple-vs-modern-web',
          ],
        },
        // Backend
        {
          type: 'category',
          label: '⚙️ Backend Development',
          collapsed: true,
          items: [
            'backend/modern-web-scraping',
            'backend/database-architecture',
            'backend/privacy-first-llm-architecture',
            'backend/pattern-based-ai-automation',
            'backend/model-context-protocol-mcp-architecture',
          ],
        },
        // Security
        {
          type: 'category',
          label: '🔒 Security',
          collapsed: true,
          items: [
            'security/docker-first-production-security',
            'security/github-graphql-security',
            'security/user-agents-and-stealth',
            'resources/security-note',
          ],
        },
        // Languages
        {
          type: 'category',
          label: '📝 Programming Languages',
          collapsed: true,
          items: [
            'concepts/python-concepts',
            'concepts/golang-concepts',
            'concepts/typescript-deno-concepts',
          ],
        },
      ],
    },
    
    // Learning & Practice
    {
      type: 'category',
      label: '🎯 Learning & Practice',
      collapsed: true,
      items: [
        // Learning Plans
        {
          type: 'category',
          label: '📋 Learning Plans',
          collapsed: true,
          items: [
            'learning-plans/index',
            'learning-plans/plan-1-threat-intelligence',
            'learning-plans/plan-2-static-analysis',
            'learning-plans/plan-3-api-security',
            'learning-plans/plan-4-aws-cdk-typescript',
          ],
        },
        // Exercises
        {
          type: 'category',
          label: '🏋️ Hands-on Exercises',
          collapsed: true,
          items: [
            'exercises/claude-code-exercises',
            'exercises/github-graphql-security-exercises',
            'exercises/language-exercises',
            'exercises/debugging-exercise',
          ],
        },
      ],
    },
    
    // Resources
    {
      type: 'category',
      label: '📖 Resources',
      collapsed: true,
      items: [
        'resources/contributing',
      ],
    },
  ],
};

module.exports = sidebars;