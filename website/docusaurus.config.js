const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Web Scraping Course: From Zero to Hero',
  tagline: 'Learn modern web scraping through epic failures and systematic debugging',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/changelogger/',

  // GitHub pages deployment config
  organizationName: 'your-username',
  projectName: 'changelogger',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/changelogger/tree/main/',
          routeBasePath: '/', // Serve docs at site root
        },
        blog: false, // Disable blog
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card
      image: 'img/social-card.jpg',
      navbar: {
        title: 'Web Scraping Course',
        logo: {
          alt: 'Web Scraping Course Logo',
          src: 'img/logo.svg',
          width: 32,
          height: 32,
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'courseSidebar',
            position: 'left',
            label: '📚 Course',
          },
          // TODO: Add reference sidebar when content is ready
          // {
          //   type: 'docSidebar',
          //   sidebarId: 'referenceSidebar',
          //   position: 'left',
          //   label: '📖 Reference',
          // },
          {
            href: 'https://github.com/your-username/changelogger',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Course',
            items: [
              {
                label: '🚀 Getting Started',
                to: '/intro',
              },
              {
                label: '🐛 Debugging Journey',
                to: '/debugging-journey',
              },
              // TODO: Add when content exists
              // {
              //   label: '🧪 Exercises',
              //   to: '/exercises',
              // },
            ],
          },
          {
            title: 'Resources',
            items: [
              // TODO: Add when content exists
              // {
              //   label: '⚙️ Setup Guide',
              //   to: '/setup',
              // },
              // {
              //   label: '🧪 Testing Guide',
              //   to: '/testing',
              // },
              // {
              //   label: '🏗️ Project Structure',
              //   to: '/project-structure',
              // },
              {
                label: '🐳 Containerization',
                to: '/chapters/chapter-00-containerization',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/your-username/changelogger',
              },
              {
                label: 'Issues & Questions',
                href: 'https://github.com/your-username/changelogger/issues',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Changelogger Project. Built with Docusaurus.<br/>
        <em>"The expert has failed more times than the beginner has even tried. Let's fail faster so we can succeed sooner."</em>`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['python', 'bash', 'json', 'yaml'],
      },
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),
};

module.exports = config;
