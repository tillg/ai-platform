import React from "react";
import { ThemeProvider } from "styled-components";

import { GlobalStyles } from "@com.mgmtp.a12.widgets/widgets-core/lib/theme/base";
// import { flatTheme } from "@com.mgmtp.a12.widgets/widgets-core/lib/theme/flat/flat-theme";
import { createTheme } from "@com.mgmtp.a12.widgets/widgets-core/lib/theme/create-theme";
import "@com.mgmtp.a12.widgets/widgets-core/lib/theme/basic.css";

import { ApplicationFrame } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/application-frame";
import { MenuItem } from "@com.mgmtp.a12.widgets/widgets-core/lib/menu";

// import your components
import { Header } from "./Header";
import { Sidebar } from "./Sidebar";
// import { Content } from "./Content";
import { StartPage } from "./pages/StartPage";

const theme = createTheme({
  baseTheme: "flat-compact"
});

const menuItems = [{ label: "About" }, { label: "Quote" }];

const sidebarItems = [
  {
    name: "Quote 1",
    quote: "Life is short, smile while you still have teeth."
  },
  {
    name: "Quote 2",
    quote: "If two wrongs don't make a right, try three."
  },
  {
    name: "Quote 3",
    quote: "I am not lazy, I am on energy saving mode."
  }
];

export default function App() {
  const [menuIndex, setMenuIndex] = React.useState(0);
  const [sidebarIndex, setSidebarIndex] = React.useState(0);

  const getMenuItems = React.useCallback((): MenuItem[] => {
    return menuItems.map((item, index) => ({
      ...item,
      selected: menuIndex === index,
      onClick: () => setMenuIndex(index)
    }));
  }, [menuIndex])

  const getSidebarItems = React.useCallback((): MenuItem[] => {
    return sidebarItems.map((item, index) => ({
      label: item.name,
      selected: sidebarIndex === index,
      onClick: () => setSidebarIndex(index)
    }));
  }, [sidebarIndex])

  // const selectedSidebarItem = sidebarItems[sidebarIndex];
  // const content = menuIndex === 0 ? selectedSidebarItem.quote : "About page without sidebar";

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <ApplicationFrame
        main={<Header items={getMenuItems()} />}
        sub={menuIndex === 1 ? <Sidebar items={getSidebarItems()} /> : undefined}
        // content={<Content title={menuIndex === 0 ? selectedSidebarItem.name : "About"} text={content} />}
        content={<StartPage/>}
        subExpanded={true}
      />
    </ThemeProvider>
  );
}