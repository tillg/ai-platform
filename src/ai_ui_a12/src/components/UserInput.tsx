import { useEffect, useState , useCallback} from "react";
import { TextAreaStateless } from "@com.mgmtp.a12.widgets/widgets-core/lib/input/text-area";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon"
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";

interface Props {
    onSend: (question: string) => void;
    disabled: boolean;
    initQuestion?: string;
    placeholder?: string;
    clearOnSend?: boolean;
}

export const UserInput = ({ onSend, disabled, placeholder, clearOnSend, initQuestion }: Props) => {
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

    const handleQuestionChange = useCallback((event: React.ChangeEvent<HTMLTextAreaElement>): void => {
        		setQuestion(event.target.value);
    }, []);

    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <TextAreaStateless
                placeholder={placeholder}
                value={question}
                onChange={handleQuestionChange}
                onKeyDown={onEnterPress}
            />
            <Button 
                icon={<Icon>send</Icon>} 
                onClick={sendQuestion} 
                id={generateUid()}
                style={{ alignSelf: 'flex-end' }}

            />
        </div>
    );
};
