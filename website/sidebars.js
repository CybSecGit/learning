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
        'resources/docker-quick-start',
        'concepts/containerization',
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
        'concepts/vibe-coding',
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
            'concepts/postgres-sqlalchemy-alembic-trinity',
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
            'concepts/python-project-setup',
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
            {
              type: 'category',
              label: 'Plan 4: CDK TypeScript',
              collapsed: true,
              link: {
                type: 'doc',
                id: 'learning-plans/plan-4-aws-cdk-typescript',
              },
              items: [
                'learning-plans/cdk-typescript/setup',
                'learning-plans/cdk-typescript/module-1',
                'learning-plans/cdk-typescript/module-2',
                'learning-plans/cdk-typescript/module-3',
                'learning-plans/cdk-typescript/module-4',
                'learning-plans/cdk-typescript/module-5',
                'learning-plans/cdk-typescript/module-6',
                'learning-plans/cdk-typescript/module-7',
                'learning-plans/cdk-typescript/debugging-guide',
                'learning-plans/cdk-typescript/troubleshooting',
              ],
            },
            {
              type: 'category',
              label: 'Plan 5: Makefile & Next.js',
              collapsed: true,
              link: {
                type: 'doc',
                id: 'learning-plans/plan-5-makefile-nextjs',
              },
              items: [
                'learning-plans/makefile-nextjs/setup',
                'learning-plans/makefile-nextjs/module-1',
                'learning-plans/makefile-nextjs/module-2',
                'learning-plans/makefile-nextjs/module-3',
                'learning-plans/makefile-nextjs/module-4',
                'learning-plans/makefile-nextjs/module-5',
                'learning-plans/makefile-nextjs/module-6',
                'learning-plans/makefile-nextjs/module-7',
                'learning-plans/makefile-nextjs/debugging-guide',
                'learning-plans/makefile-nextjs/troubleshooting',
              ],
            },
            {
              type: 'category',
              label: 'Plan 6: Go TUI with Charm',
              collapsed: true,
              link: {
                type: 'doc',
                id: 'learning-plans/plan-6-go-tui-charm',
              },
              items: [
                'learning-plans/go-tui-charm/setup',
                'learning-plans/go-tui-charm/installation',
                'learning-plans/go-tui-charm/module-1',
                'learning-plans/go-tui-charm/module-2',
                'learning-plans/go-tui-charm/module-3',
                'learning-plans/go-tui-charm/module-4',
                'learning-plans/go-tui-charm/module-5',
                'learning-plans/go-tui-charm/module-6',
                'learning-plans/go-tui-charm/module-7',
                'learning-plans/go-tui-charm/debugging-guide',
              ],
            },
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