import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/learning/',
    component: ComponentCreator('/learning/', '3e3'),
    routes: [
      {
        path: '/learning/',
        component: ComponentCreator('/learning/', 'e79'),
        routes: [
          {
            path: '/learning/',
            component: ComponentCreator('/learning/', 'f36'),
            routes: [
              {
                path: '/learning/backend/database-architecture',
                component: ComponentCreator('/learning/backend/database-architecture', 'e3d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/backend/model-context-protocol-mcp-architecture',
                component: ComponentCreator('/learning/backend/model-context-protocol-mcp-architecture', 'c33'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/backend/modern-web-scraping',
                component: ComponentCreator('/learning/backend/modern-web-scraping', '265'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/backend/pattern-based-ai-automation',
                component: ComponentCreator('/learning/backend/pattern-based-ai-automation', '818'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/backend/privacy-first-llm-architecture',
                component: ComponentCreator('/learning/backend/privacy-first-llm-architecture', 'a82'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/claude-code-examples/go/CLAUDE',
                component: ComponentCreator('/learning/concepts/claude-code-examples/go/CLAUDE', '839'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/development-config',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/development-config', 'bab'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/error-handling',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/error-handling', 'c66'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/git-workflow',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/git-workflow', '751'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/production-config',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/production-config', '76f'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/security-guidelines',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/security-guidelines', '00b'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/style-guide',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/style-guide', '9a5'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/imports/testing-conventions',
                component: ComponentCreator('/learning/concepts/claude-code-examples/imports/testing-conventions', 'd89'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/python/CLAUDE',
                component: ComponentCreator('/learning/concepts/claude-code-examples/python/CLAUDE', '157'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-examples/typescript/CLAUDE',
                component: ComponentCreator('/learning/concepts/claude-code-examples/typescript/CLAUDE', '890'),
                exact: true
              },
              {
                path: '/learning/concepts/claude-code-workshop',
                component: ComponentCreator('/learning/concepts/claude-code-workshop', 'e21'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/containerization',
                component: ComponentCreator('/learning/concepts/containerization', '218'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/failure-driven-development',
                component: ComponentCreator('/learning/concepts/failure-driven-development', 'd16'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/golang-concepts',
                component: ComponentCreator('/learning/concepts/golang-concepts', 'b7c'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/mastering-claude-code',
                component: ComponentCreator('/learning/concepts/mastering-claude-code', '498'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/mastering-gemini-cli',
                component: ComponentCreator('/learning/concepts/mastering-gemini-cli', 'f78'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/modern-dependency-management',
                component: ComponentCreator('/learning/concepts/modern-dependency-management', 'abb'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/playwright-mcp-mastery',
                component: ComponentCreator('/learning/concepts/playwright-mcp-mastery', 'c17'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/postgres-sqlalchemy-alembic-trinity',
                component: ComponentCreator('/learning/concepts/postgres-sqlalchemy-alembic-trinity', 'a3d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/pre-commit-hooks-claude-code',
                component: ComponentCreator('/learning/concepts/pre-commit-hooks-claude-code', '72d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/python-concepts',
                component: ComponentCreator('/learning/concepts/python-concepts', '6ee'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/python-project-setup',
                component: ComponentCreator('/learning/concepts/python-project-setup', '3f7'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/testing-like-you-mean-it',
                component: ComponentCreator('/learning/concepts/testing-like-you-mean-it', 'b16'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/typescript-deno-concepts',
                component: ComponentCreator('/learning/concepts/typescript-deno-concepts', '256'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/concepts/vibe-coding',
                component: ComponentCreator('/learning/concepts/vibe-coding', 'da1'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/debugging-journey',
                component: ComponentCreator('/learning/debugging-journey', '94d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/design-showcase',
                component: ComponentCreator('/learning/design-showcase', '7de'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/exercises/claude-code-exercises',
                component: ComponentCreator('/learning/exercises/claude-code-exercises', 'dd2'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/exercises/debugging-exercise',
                component: ComponentCreator('/learning/exercises/debugging-exercise', '9c7'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/exercises/github-graphql-security-exercises',
                component: ComponentCreator('/learning/exercises/github-graphql-security-exercises', 'a2e'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/exercises/language-exercises',
                component: ComponentCreator('/learning/exercises/language-exercises', '939'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/frontend/gui-implementation-patterns',
                component: ComponentCreator('/learning/frontend/gui-implementation-patterns', 'fed'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/frontend/simple-vs-modern-web',
                component: ComponentCreator('/learning/frontend/simple-vs-modern-web', '138'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/frontend/webassembly-the-fast-lane',
                component: ComponentCreator('/learning/frontend/webassembly-the-fast-lane', '060'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/frontend/websockets-realtime-communication',
                component: ComponentCreator('/learning/frontend/websockets-realtime-communication', 'f8f'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/',
                component: ComponentCreator('/learning/learning-plans/', 'cff'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/debugging-guide',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/debugging-guide', '5d0'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-1',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-1', '538'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-2',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-2', '754'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-3',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-3', 'c8d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-4',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-4', '4fa'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-5',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-5', 'ba9'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-6',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-6', '7ec'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/module-7',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/module-7', '5a4'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/setup',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/setup', '1d0'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/cdk-typescript/troubleshooting',
                component: ComponentCreator('/learning/learning-plans/cdk-typescript/troubleshooting', 'e17'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/go-tui-charm/debugging-guide',
                component: ComponentCreator('/learning/learning-plans/go-tui-charm/debugging-guide', 'd7e'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/go-tui-charm/installation',
                component: ComponentCreator('/learning/learning-plans/go-tui-charm/installation', '70b'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/go-tui-charm/module-1',
                component: ComponentCreator('/learning/learning-plans/go-tui-charm/module-1', '6c7'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/go-tui-charm/setup',
                component: ComponentCreator('/learning/learning-plans/go-tui-charm/setup', '7b9'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/debugging-guide',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/debugging-guide', 'da1'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/makefile-cool-tricks',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/makefile-cool-tricks', '345'),
                exact: true
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-1',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-1', '9f3'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-2',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-2', 'e77'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-3',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-3', 'fec'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-4',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-4', '6ef'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-5',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-5', '9bd'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-6',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-6', '978'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/module-7',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/module-7', '4d9'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/nextjs-rendering-strategies',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/nextjs-rendering-strategies', '18d'),
                exact: true
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/setup',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/setup', '5e3'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/makefile-nextjs/troubleshooting',
                component: ComponentCreator('/learning/learning-plans/makefile-nextjs/troubleshooting', '48c'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-1-threat-intelligence',
                component: ComponentCreator('/learning/learning-plans/plan-1-threat-intelligence', '212'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-2-static-analysis',
                component: ComponentCreator('/learning/learning-plans/plan-2-static-analysis', '134'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-3-api-security',
                component: ComponentCreator('/learning/learning-plans/plan-3-api-security', 'cf2'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-4-aws-cdk-typescript',
                component: ComponentCreator('/learning/learning-plans/plan-4-aws-cdk-typescript', '668'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-5-makefile-nextjs',
                component: ComponentCreator('/learning/learning-plans/plan-5-makefile-nextjs', '0d9'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-6-go-tui-charm',
                component: ComponentCreator('/learning/learning-plans/plan-6-go-tui-charm', 'cef'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-7-cve-database',
                component: ComponentCreator('/learning/learning-plans/plan-7-cve-database', '0fc'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/learning-plans/plan-8-gpt2-anomaly-detection',
                component: ComponentCreator('/learning/learning-plans/plan-8-gpt2-anomaly-detection', 'f35'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/resources/contributing',
                component: ComponentCreator('/learning/resources/contributing', 'df5'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/resources/docker-quick-start',
                component: ComponentCreator('/learning/resources/docker-quick-start', '8b1'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/resources/security-note',
                component: ComponentCreator('/learning/resources/security-note', '7b8'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/security/docker-first-production-security',
                component: ComponentCreator('/learning/security/docker-first-production-security', '961'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/security/github-graphql-security',
                component: ComponentCreator('/learning/security/github-graphql-security', 'de3'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/security/user-agents-and-stealth',
                component: ComponentCreator('/learning/security/user-agents-and-stealth', '528'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/',
                component: ComponentCreator('/learning/', 'b2d'),
                exact: true,
                sidebar: "courseSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
