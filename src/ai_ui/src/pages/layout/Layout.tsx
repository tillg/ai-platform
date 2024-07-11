import { Outlet, Link } from "react-router-dom";
import { SubHeader } from "./SubHeader";
import styles from "./Layout.module.css";
import { AiPlatformIcon, BrainIcon, PromptsIcon, ChatIcon } from "../../components/Icons";

const Layout = () => {
    return (
        <div>
            <div className={styles.layout}>
                <header className={styles.header} role={"banner"}>
                    <div className={styles.headerContainer}>
                        <Link to="/" className={styles.headerTitleContainer}>
                            <h3 className={styles.headerTitle}>
                                {/* <AiPlatformIcon fontSize="20px"/> */}
                                AI Platform
                                </h3>
                        </Link>
                    </div>
                </header>
                <SubHeader>
                    <Link to="/search" >
                        <BrainIcon fontSize="20px"/>
                        Search
                    </Link>
                    <Link to="/prompts" >
                        <PromptsIcon fontSize="20px" />
                        Prompts
                    </Link>
                    <Link to="/chat" >
                        <ChatIcon fontSize="20px" />
                        Chat
                    </Link>
                </SubHeader>

                <Outlet />
            </div>
        </div>
    );
};

export default Layout;
