import { BrainCircuitFilled } from "@fluentui/react-icons";
import { theme } from "../../constants";

interface BrainIconProps {
    fontSize?: string; // Optional prop to allow flexibility
}

export const BrainIcon = ({ fontSize = "120px" }: BrainIconProps) => (
    <BrainCircuitFilled fontSize={fontSize} primaryFill={theme.topic.brain} aria-hidden="true" aria-label="Brain Icon" />
);