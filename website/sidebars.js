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
    // Quick Start Section (always visible)
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      className: 'sidebar-category-primary',
      items: [
        'intro',
        'getting-started/setup',
        'getting-started/preview',
      ],
    },

    // Core Learning Foundation
    {
      type: 'category', 
      label: 'Core Concepts',
      collapsed: false,
      className: 'sidebar-category-primary',
      items: [
        // Fundamental Development Practices
        {
          type: 'category',
          label: 'Development Fundamentals',
          className: 'sidebar-subcategory',
          items: [
            'core-concepts/failure-driven-development',
            'core-concepts/testing-like-you-mean-it', 
            'core-concepts/containerization',
            'concepts/modern-dependency-management',
          ]
        },
        // Programming Languages
        {
          type: 'category',
          label: 'Programming Languages',
          className: 'sidebar-subcategory',
          items: [
            'concepts/python-concepts',
            'concepts/python-project-setup',
            'concepts/golang-concepts',
            'concepts/typescript-deno-concepts',
          ]
        }
      ]
    },

    // Development Tools & Workflow
    {
      type: 'category',
      label: 'Development Tools',
      collapsed: true,
      className: 'sidebar-category-secondary',
      items: [
        // AI-Assisted Development
        {
          type: 'category',
          label: 'AI Development Tools',
          className: 'development-tools-section',
          items: [
            'development-tools/mastering-claude-code',
            'development-tools/claude-code-workshop',
            'development-tools/claude-code-orchestration',
            'concepts/vibe-coding',
            'development-tools/mastering-gemini-cli',
          ]
        },
        // Testing & Quality Tools
        {
          type: 'category',
          label: 'Testing & Quality',
          className: 'development-tools-section',
          items: [
            'development-tools/playwright-mcp-mastery',
            'concepts/pre-commit-hooks-claude-code',
          ]
        }
      ]
    },

    // Technical Domain Knowledge
    {
      type: 'category',
      label: 'Technical Domains', 
      collapsed: true,
      className: 'sidebar-category-secondary',
      items: [
        // Backend Development
        {
          type: 'category',
          label: 'Backend Development',
          className: 'technical-domain-section',
          items: [
            'backend/database-architecture',
            'concepts/postgres-sqlalchemy-alembic-trinity',
            'backend/privacy-first-llm-architecture',
            'backend/pattern-based-ai-automation',
            'backend/model-context-protocol-mcp-architecture',
          ],
        },
        // Frontend Development
        {
          type: 'category', 
          label: 'Frontend Development',
          className: 'technical-domain-section',
          items: [
            'frontend/gui-implementation-patterns',
            'frontend/webassembly-the-fast-lane',
            'frontend/websockets-realtime-communication',
            'frontend/simple-vs-modern-web',
          ],
        },
        // Security
        {
          type: 'category',
          label: 'Security & Production',
          className: 'technical-domain-section',
          items: [
            'security/modern-web-scraping',
            'security/docker-first-production-security',
            'security/github-graphql-security',
            'security/user-agents-and-stealth',
            'reference/security-note',
          ],
        }
      ]
    },

    // Structured Learning Paths
    {
      type: 'category',
      label: 'Learning Paths',
      collapsed: true,
      className: 'sidebar-category-secondary',
      items: [
        'learning-plans/index',
        {
          type: 'category',
          label: 'Security Learning Paths',
          items: [
            'learning-plans/plan-1-threat-intelligence',
            'learning-plans/plan-2-static-analysis',
            'learning-plans/plan-3-api-security',
            'learning-plans/plan-7-cve-database',
          ]
        },
        {
          type: 'category',
          label: 'Development Learning Paths',
          items: [
            {
              type: 'category',
              label: 'AWS CDK with TypeScript',
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
              label: 'Makefile & Next.js Mastery',
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
              label: 'Go TUI with Charm Libraries',
              collapsed: true,
              link: {
                type: 'doc',
                id: 'learning-plans/plan-6-go-tui-charm',
              },
              items: [
                'learning-plans/go-tui-charm/setup',
                'learning-plans/go-tui-charm/installation',
                'learning-plans/go-tui-charm/module-1',
                'learning-plans/go-tui-charm/debugging-guide',
              ],
            },
          ]
        },
        {
          type: 'category',
          label: 'AI/ML Learning Paths',
          items: [
            'learning-plans/plan-8-gpt2-anomaly-detection',
          ]
        }
      ]
    },

    // Hands-on Practice & Tutorials
    {
      type: 'category',
      label: 'Hands-on Practice',
      collapsed: true,
      className: 'sidebar-category-secondary',
      items: [
        // Tutorial-style Content
        {
          type: 'category',
          label: 'Step-by-Step Tutorials',
          items: [
            'hands-on-practice/user-agents-stealth-tutorial',
            'hands-on-practice/database-architecture-tutorial',
            'hands-on-practice/gui-patterns-tutorial',
            'hands-on-practice/github-graphql-security-tutorial',
          ]
        },
        // Exercises & Challenges
        {
          type: 'category',
          label: 'Exercises & Challenges',
          items: [
            'exercises/claude-code-exercises',
            'exercises/github-graphql-security-exercises',
            'exercises/language-exercises',
            'exercises/debugging-exercise',
          ]
        },
        // Debugging & Troubleshooting
        {
          type: 'category',
          label: 'Debugging & Troubleshooting',
          items: [
            'hands-on-practice/debugging-journey',
          ]
        }
      ]
    },

    // Quick Reference & Resources
    {
      type: 'category',
      label: 'Reference',
      collapsed: true,
      className: 'sidebar-category-secondary',
      items: [
        'design-showcase',
      ],
    },
  ],
};

module.exports = sidebars;