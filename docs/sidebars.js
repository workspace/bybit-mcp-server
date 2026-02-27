/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    "intro",
    "getting-started",
    {
      type: "category",
      label: "Tools Reference",
      items: ["tools/market", "tools/trade", "tools/account"],
    },
  ],
};

module.exports = sidebars;
