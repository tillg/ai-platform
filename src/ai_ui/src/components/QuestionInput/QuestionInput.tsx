import { useEffect, useState } from "react";
import { Button, Tooltip } from "@fluentui/react-components";
import { Send28Filled } from "@fluentui/react-icons";
import { theme } from "../../constants";
import styled from "styled-components";

interface Props {
    onSend: (question: string) => void;
    disabled: boolean;
    initQuestion?: string;
    placeholder?: string;
    clearOnSend?: boolean;
}
const StyledQuestionInputContainer = styled.div`
       position: relative; 

`;

const StyledQuestionInputTextArea = styled.textarea`
    border-radius: 8px;
    width: 100%;
    box-shadow:
        0px 8px 16px rgba(0, 0, 0, 0.14),
        0px 0px 2px rgba(0, 0, 0, 0.12);
    line-height: 40px;
    resize: none; /* Prevent resizing */
    border: none; /* Make textarea borderless */
    outline: none; /* Remove focus outline */
    padding: 15px;
    background: white;
    // font-size: 16px
    // border: 1px solid blue;
`
const StyledSendButton = styled.div`
    position: absolute;
    right: 10px; // Adjust as needed
    bottom: 10px; // Adjust as needed
`;

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend, initQuestion }: Props) => {
    const [question, setQuestion] = useState<string>("");

    useEffect(() => {
        initQuestion && setQuestion(initQuestion);
    }, [initQuestion]);

    const sendQuestion = () => {
        if (disabled || !question.trim()) {
            return;
        }

        onSend(question);

        if (clearOnSend) {
            setQuestion("");
        }
    };

    const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
        if (ev.key === "Enter" && !ev.shiftKey) {
            ev.preventDefault();
            sendQuestion();
        }
    };

    const onQuestionChange = (ev: React.FormEvent<HTMLTextAreaElement>) => {
        const newValue = ev.currentTarget.value;
        if (!newValue) {
            setQuestion("");
        } else if (newValue.length <= 1000) {
            setQuestion(newValue);
        }
    };

    return (
        <StyledQuestionInputContainer>
            <StyledQuestionInputTextArea
                placeholder={placeholder}
                value={question}
                onChange={onQuestionChange}
                onKeyDown={onEnterPress}
            />
            <StyledSendButton>

                <div >
                    <Tooltip content="Ask question button" relationship="label">
                        <Button size="large" icon={<Send28Filled primaryFill={theme.topic.brain} />} onClick={sendQuestion} />
                    </Tooltip>
                </div>
            </StyledSendButton>

        </StyledQuestionInputContainer>
    );
};
