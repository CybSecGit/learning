const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Personal Wiki',
  tagline: 'Development knowledge base with hands-on practice and systematic debugging',
  favicon: 'img/favicon.svg',

  // Set the production url of your site here
  url: 'https://cybsecgit.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/learning/',

  // GitHub pages deployment config
  organizationName: 'cybsecgit',
  projectName: 'learning',

  onBrokenLinks: 'warn',
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
          editUrl: 'https://github.com/cybsecgit/learning/tree/main/',
          routeBasePath: '/', // Serve docs at site root
        },
        blog: false, // Disable blog
        theme: {
          customCss: require.resolve('./src/css/enhanced-custom.css'),
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
        title: 'Personal Wiki',
        logo: {
          alt: 'Personal Development Wiki Logo',
          src: 'img/logo.svg',
          width: 32,
          height: 32,
        },
        items: [
          {
            type: 'search',
            position: 'left',
          },
          {
            href: 'https://github.com/cybsecgit/learning',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Quick Start',
            items: [
              {
                label: '🚀 Getting Started',
                to: '/getting-started',
              },
              {
                label: '📚 Core Concepts',
                to: '/core-concepts',
              },
              {
                label: '🛠️ Hands-on Practice',
                to: '/hands-on-practice',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: '🔧 Development Tools',
                to: '/development-tools',
              },
              {
                label: '🎯 Learning Paths',
                to: '/learning-paths',
              },
              {
                label: '📖 Reference',
                to: '/reference',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/cybsecgit/learning',
              },
              {
                label: 'Issues & Questions',
                href: 'https://github.com/cybsecgit/learning/issues',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Built with Docusaurus.<br/>
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
      docs: {
        sidebar: {
          hideable: true,
          autoCollapseCategories: true,
        },
      },
      algolia: false, // Disable for now, can be added later
      announcementBar: {
        id: 'development_lab',
        content: '🚀 Development Skills Laboratory - Learn through hands-on practice and systematic debugging',
        backgroundColor: '#7c3aed',
        textColor: '#ffffff',
        isCloseable: true,
      },
    }),
};

module.exports = config;
