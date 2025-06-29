import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/learning/',
    component: ComponentCreator('/learning/', '7c6'),
    routes: [
      {
        path: '/learning/',
        component: ComponentCreator('/learning/', '4c9'),
        routes: [
          {
            path: '/learning/',
            component: ComponentCreator('/learning/', '56c'),
            routes: [
              {
                path: '/learning/chapters/chapter-00-containerization',
                component: ComponentCreator('/learning/chapters/chapter-00-containerization', 'ec6'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-01-setup',
                component: ComponentCreator('/learning/chapters/chapter-01-setup', 'ea5'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-02-preview',
                component: ComponentCreator('/learning/chapters/chapter-02-preview', '2cd'),
                exact: true
              },
              {
                path: '/learning/chapters/chapter-02-web-scraping',
                component: ComponentCreator('/learning/chapters/chapter-02-web-scraping', 'fb8'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-03-failure-driven-development',
                component: ComponentCreator('/learning/chapters/chapter-03-failure-driven-development', 'a25'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-04-testing-like-you-mean-it',
                component: ComponentCreator('/learning/chapters/chapter-04-testing-like-you-mean-it', 'e61'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-05-user-agents-and-stealth',
                component: ComponentCreator('/learning/chapters/chapter-05-user-agents-and-stealth', '709'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-06-mastering-claude-code',
                component: ComponentCreator('/learning/chapters/chapter-06-mastering-claude-code', '99d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-06.5-claude-code-workshop',
                component: ComponentCreator('/learning/chapters/chapter-06.5-claude-code-workshop', '532'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-07-database-architecture',
                component: ComponentCreator('/learning/chapters/chapter-07-database-architecture', 'faf'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-08-gui-implementation-patterns',
                component: ComponentCreator('/learning/chapters/chapter-08-gui-implementation-patterns', 'ba8'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-08.5-simple-vs-modern-web',
                component: ComponentCreator('/learning/chapters/chapter-08.5-simple-vs-modern-web', '4af'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-09-privacy-first-llm-architecture',
                component: ComponentCreator('/learning/chapters/chapter-09-privacy-first-llm-architecture', '3a9'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-10-modern-dependency-management',
                component: ComponentCreator('/learning/chapters/chapter-10-modern-dependency-management', 'da7'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-11-pattern-based-ai-automation',
                component: ComponentCreator('/learning/chapters/chapter-11-pattern-based-ai-automation', '625'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-12-model-context-protocol-mcp-architecture',
                component: ComponentCreator('/learning/chapters/chapter-12-model-context-protocol-mcp-architecture', '488'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/chapter-13-docker-first-production-security',
                component: ComponentCreator('/learning/chapters/chapter-13-docker-first-production-security', '549'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/learning/chapters/claude-code-examples/go/CLAUDE',
                component: ComponentCreator('/learning/chapters/claude-code-examples/go/CLAUDE', '32d'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/development-config',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/development-config', '53a'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/error-handling',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/error-handling', 'eb9'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/git-workflow',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/git-workflow', '22b'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/production-config',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/production-config', '86c'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/security-guidelines',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/security-guidelines', '3dc'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/style-guide',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/style-guide', 'eb6'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/imports/testing-conventions',
                component: ComponentCreator('/learning/chapters/claude-code-examples/imports/testing-conventions', '1a7'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/python/CLAUDE',
                component: ComponentCreator('/learning/chapters/claude-code-examples/python/CLAUDE', 'c34'),
                exact: true
              },
              {
                path: '/learning/chapters/claude-code-examples/typescript/CLAUDE',
                component: ComponentCreator('/learning/chapters/claude-code-examples/typescript/CLAUDE', '73f'),
                exact: true
              },
              {
                path: '/learning/concepts/golang-concepts',
                component: ComponentCreator('/learning/concepts/golang-concepts', 'b7c'),
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
                path: '/learning/concepts/typescript-deno-concepts',
                component: ComponentCreator('/learning/concepts/typescript-deno-concepts', '256'),
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
                path: '/learning/exercises/language-exercises',
                component: ComponentCreator('/learning/exercises/language-exercises', '939'),
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
