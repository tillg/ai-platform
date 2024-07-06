import { ChatIcon } from "../../components/Icons/ChatIcon";
import styles from "./Chat.module.css";
import { ExampleList } from "../../components/Example";

interface Props {
    onClick: (arg0: string) => void;
}

const EmptyChat = ({onClick}: Props) => {

    return (
        <div className={styles.chatEmptyState}>
            <ChatIcon fontSize={"120px"} />
            <h1 className={styles.chatEmptyStateTitle}>Chat with me</h1>
            <h2 className={styles.chatEmptyStateSubtitle}>Ask anything or try an example</h2>
            <ExampleList onExampleClicked={onClick} />
        </div>
    )

};

export default EmptyChat;
