import { Outlet, Link } from "react-router-dom";
import { SubHeader } from "./SubHeader";
import styles from "./Layout.module.css";
import { BrainCircuitFilled, SparkleFilled } from "@fluentui/react-icons";
import { COLORS } from "../../constants";


const Layout = () => {
    return (
        <div>
            <div className={styles.layout}>
                <header className={styles.header} role={"banner"}>
                    <div className={styles.headerContainer}>
                        <Link to="/" className={styles.headerTitleContainer}>
                            <h3 className={styles.headerTitle}>
                                <BrainCircuitFilled primaryFill={COLORS.brandColor} aria-hidden="true" aria-label="AI logo" />
                                AI Platform
                                </h3>
                        </Link>
                        <h4 className={styles.headerRightText}>Modular AI</h4>
                    </div>
                </header>
                <SubHeader>
                    <Link to="/search" >
                        Search
                    </Link>
                    <Link to="/prompts" >
                        Prompts
                    </Link>
                    <Link to="/chat" >
                        Chat
                    </Link>
                </SubHeader>

                <Outlet />
            </div>
        </div>
    );
};

export default Layout;
