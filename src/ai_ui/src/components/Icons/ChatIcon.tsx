import { ChatFilled } from "@fluentui/react-icons";
import { theme } from "../../constants";

interface ChatIconProps {
    fontSize?: string; // Optional prop to allow flexibility
}

export const ChatIcon = ({ fontSize = "120px" }: ChatIconProps) => (
    <ChatFilled fontSize={fontSize} primaryFill={theme.topic.chat} aria-hidden="true" aria-label="Chat Icon" />
);