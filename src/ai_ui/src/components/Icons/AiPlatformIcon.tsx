import { BrainIcon } from "./BrainIcon";
import { PromptsIcon } from "./PromptsIcon";
import { ChatIcon } from "./ChatIcon";

interface AiPlatformIconProps {
    fontSize?: string; // Optional prop to allow flexibility
}

export const AiPlatformIcon = ({ fontSize = "120px" }: AiPlatformIconProps) => (
    <><BrainIcon fontSize={fontSize} />
        {/* <PromptsIcon fontSize={fontSize} />
    <ChatIcon fontSize={fontSize} /> */}
    </>
);