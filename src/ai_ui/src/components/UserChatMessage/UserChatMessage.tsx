import styled from "styled-components";
import { theme } from "../../constants"
// Extending div props to accept any standard div attributes
interface Props extends React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode; // Optional children prop to accept any child elements
}

const StyledUserChatMessageContainer = styled.div`
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
    max-width: 80%;
    margin-left: auto;
`

const Message = styled.div`
    font-size: 16px;
    font-family: system-ui;
    padding: 20px;
    background:  ${props => props.theme.userMessageBackgroundColor};;
    border-radius: 8px;
    box-shadow:
        0px 2px 4px rgba(0, 0, 0, 0.14),
        0px 0px 2px rgba(0, 0, 0, 0.12);
    outline: transparent solid 1px;
`;



// Adjusting the component to accept any div attributes and children
const UserChatMessage: React.FC<Props> = ({ children, ...divProps }) => {
    return (
        <StyledUserChatMessageContainer {...divProps}>
            <Message>{children}</Message>
        </StyledUserChatMessageContainer>
    );
};

export { UserChatMessage };
