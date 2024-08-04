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
import { AboutPage } from "./pages/AboutPage";
import { SearchPage } from "./pages/SearchPage";
import { ChatLlmPage } from "./pages/ChatLlmPage";

const theme = createTheme({
  baseTheme: "flat-compact"
});

const menuItems = [{ label: "About", content: <AboutPage /> }, { label: "Search Brains", content: <SearchPage /> }, { label: "Chat LLM", content: <ChatLlmPage/> }];


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


  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <ApplicationFrame
        main={<Header items={getMenuItems()} />}
        content={menuItems[menuIndex].content}
        subExpanded={true}
      />
    </ThemeProvider>
  );
}