// @ts-check
const { themes } = require("prism-react-renderer");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Bybit MCP Server",
  tagline: "A Model Context Protocol server for Bybit V5 API",
  favicon: "img/favicon.ico",

  url: "https://workspace.github.io",
  baseUrl: "/bybit-mcp/",

  organizationName: "workspace",
  projectName: "bybit-mcp",
  deploymentBranch: "gh-pages",

  onBrokenLinks: "throw",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: "./sidebars.js",
          editUrl:
            "https://github.com/workspace/bybit-mcp/tree/main/docs",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: "Bybit MCP",
        items: [
          {
            type: "docSidebar",
            sidebarId: "docsSidebar",
            position: "left",
            label: "Docs",
          },
          {
            href: "https://github.com/workspace/bybit-mcp",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Docs",
            items: [
              { label: "Getting Started", to: "/getting-started" },
              { label: "Tools Reference", to: "/tools/market" },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "GitHub",
                href: "https://github.com/workspace/bybit-mcp",
              },
              {
                label: "PyPI",
                href: "https://pypi.org/project/bybit-mcp/",
              },
            ],
          },
        ],
        copyright: `Copyright \u00a9 ${new Date().getFullYear()} bybit-mcp contributors. Built with Docusaurus.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
        additionalLanguages: ["python", "bash", "json"],
      },
    }),
};

module.exports = config;
