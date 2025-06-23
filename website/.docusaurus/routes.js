import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/changelogger/__docusaurus/debug',
    component: ComponentCreator('/changelogger/__docusaurus/debug', 'cba'),
    exact: true
  },
  {
    path: '/changelogger/__docusaurus/debug/config',
    component: ComponentCreator('/changelogger/__docusaurus/debug/config', '92b'),
    exact: true
  },
  {
    path: '/changelogger/__docusaurus/debug/content',
    component: ComponentCreator('/changelogger/__docusaurus/debug/content', '1a9'),
    exact: true
  },
  {
    path: '/changelogger/__docusaurus/debug/globalData',
    component: ComponentCreator('/changelogger/__docusaurus/debug/globalData', '557'),
    exact: true
  },
  {
    path: '/changelogger/__docusaurus/debug/metadata',
    component: ComponentCreator('/changelogger/__docusaurus/debug/metadata', 'afb'),
    exact: true
  },
  {
    path: '/changelogger/__docusaurus/debug/registry',
    component: ComponentCreator('/changelogger/__docusaurus/debug/registry', 'fa7'),
    exact: true
  },
  {
    path: '/changelogger/__docusaurus/debug/routes',
    component: ComponentCreator('/changelogger/__docusaurus/debug/routes', '0b5'),
    exact: true
  },
  {
    path: '/changelogger/',
    component: ComponentCreator('/changelogger/', 'f62'),
    routes: [
      {
        path: '/changelogger/',
        component: ComponentCreator('/changelogger/', '6a4'),
        routes: [
          {
            path: '/changelogger/',
            component: ComponentCreator('/changelogger/', 'a36'),
            routes: [
              {
                path: '/changelogger/chapters/chapter-00-containerization',
                component: ComponentCreator('/changelogger/chapters/chapter-00-containerization', '898'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/changelogger/debugging-journey',
                component: ComponentCreator('/changelogger/debugging-journey', '286'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/changelogger/',
                component: ComponentCreator('/changelogger/', '58b'),
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
