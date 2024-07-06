import { BranchCompareFilled } from "@fluentui/react-icons";
import { theme } from "../../constants";

interface PromptsIconProps {
    fontSize?: string; // Optional prop to allow flexibility
}

export const PromptsIcon = ({ fontSize = "120px" }: PromptsIconProps) => (
    <BranchCompareFilled fontSize={fontSize} primaryFill={theme.topic.prompts} aria-hidden="true" aria-label="Prompts Icon" />
);