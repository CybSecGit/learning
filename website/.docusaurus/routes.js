import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/learning/',
    component: ComponentCreator('/learning/', '229'),
    routes: [
      {
        path: '/learning/',
        component: ComponentCreator('/learning/', 'd59'),
        routes: [
          {
            path: '/learning/',
            component: ComponentCreator('/learning/', 'b8b'),
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
