import { Stack } from "@fluentui/react";
import styles from "./Start.module.css";
import { BrainCircuitFilled, SparkleFilled } from "@fluentui/react-icons";
import { theme } from "../../constants";
import { Outlet, Link } from "react-router-dom";

export const StartPage = () => {

    return (
        <div>
            <div className={styles.chatEmptyState}>
                <BrainCircuitFilled fontSize={"120px"} primaryFill={theme.topic.brain} aria-hidden="true" aria-label="AI logo" />
                <h1 className={styles.chatEmptyStateTitle}>AI Platform</h1>
                <p>Play around with <Link to="/search" >
                    Vector Databases
                </Link>, <Link to="/prompts" >
                        Prompts
                    </Link> and <Link to="/chat" >
                        chats
                    </Link>.</p>
            </div>

        </div>)
}

