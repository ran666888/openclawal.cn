import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'OpenClaw 中文社区',
  tagline: '开源 AI Agent 框架中文社区',
  favicon: 'img/favicon.ico',

  url: 'https://openclaw.cn',
  baseUrl: '/',

  organizationName: 'ran666888',
  projectName: 'openclawal.cn',

  onBrokenLinks: 'warn',

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['en', 'zh-Hans', 'zh-Hant'],
    localeConfigs: {
      en: {
        label: 'English',
      },
      'zh-Hans': {
        label: '简体中文',
        htmlLang: 'zh-Hans',
      },
      'zh-Hant': {
        label: '繁體中文',
        htmlLang: 'zh-Hant',
      },
    },
  },

  themes: [
    '@docusaurus/theme-mermaid',
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        hashed: true,
        language: ['en', 'zh'],
        indexBlog: false,
        docsRouteBasePath: '/',
        highlightSearchTermsOnTargetPage: false,
        ignoreFiles: [
          /^user-guide\/skills\/bundled\//,
          /^user-guide\/skills\/optional\//,
        ],
      }),
    ],
  ],

  plugins: [],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/openclaw-og.svg',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
    navbar: {
      title: 'OpenClaw 中文社区',
      logo: {
        alt: 'OpenClaw',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docs',
          position: 'left',
          label: '文档',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '文档',
          items: [
            { label: '快速入门', to: '/getting-started/quickstart' },
            { label: '用户指南', to: '/user-guide/cli' },
            { label: '开发者指南', to: '/developer-guide/architecture' },
            { label: '参考', to: '/reference/cli-commands' },
          ],
        },
        {
          title: '社区',
          items: [
            { label: 'GitHub', href: 'https://github.com/openclaw/openclaw' },
            { label: 'OpenClaw 官网', href: 'https://openclaw.ai' },
            { label: 'ClawHub', href: 'https://clawhub.openclaw.ai' },
          ],
        },
        {
          title: '更多',
          items: [
            { label: 'OpenClaw 官方文档', href: 'https://docs.openclaw.ai' },
            { label: 'GitHub', href: 'https://github.com/ran666888/openclawal.cn' },
          ],
        },
      ],
      copyright: `Built by <a href="https://github.com/ran666888">Wahhra</a> · OpenClaw 中文社区 · ${new Date().getFullYear()}`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'yaml', 'json', 'python', 'toml'],
    },
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
