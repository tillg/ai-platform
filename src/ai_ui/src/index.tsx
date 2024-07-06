import React from "react";
import ReactDOM from "react-dom/client";
import { createHashRouter, RouterProvider } from "react-router-dom";
//import { initializeIcons } from "@fluentui/react";
import { initializeIcons } from '@fluentui/font-icons-mdl2';
import { ThemeProvider } from "styled-components";
import "./index.css";
import { theme } from "./constants"
import Layout from "./pages/layout/Layout";
import Chat from "./pages/chat/Chat";
import Search from "./pages/search/Search";
import {StartPage} from "./pages/start/StartPage";
import Prompts from "./pages/prompts/Prompts";

var layout = <Layout />;

initializeIcons();


const router = createHashRouter([
    {
        path: "/",
        element: layout,
        children: [
            {
                index: true,
                element: <StartPage />
            },
            {
                path: "/search",
                element: <Search />
            },
            {
                path: "/chat",
                element: <Chat />
            },
            {
                path: "/prompts",
                element: <Prompts />
            }
        ]
    }
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <RouterProvider router={router} />
        </ThemeProvider>
    </React.StrictMode>
);
