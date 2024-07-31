import { Chat } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";

export const ChatHistory = () => {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <Chat.Container
                style={{
                    background: 'white',
                    maxWidth: 700
                }}
            >
                <Chat.MessageGroup
                    userInfo={<Chat.UserInfo userAvatar={<Chat.Avatar alt="Peter Avatar" imageUrl="images/user-avatar.png" />} userName="Peter" />}
                >
                    <Chat.Message status="11:11 am">
                        Hello, my name is Peter. How can I help you?
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup position="right">
                    <Chat.Message status="11:13 am">
                        Hello! I have a question about a tax form
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup
                    userInfo={<Chat.UserInfo userAvatar={<Chat.Avatar alt="Peter Avatar" imageUrl="images/user-avatar.png" />} userName="Peter" />}
                >
                    <Chat.Message status="11:13 am">
                        Regarding tax forms, Susan is our specialist. Hi{' '}
                        <b>
                            @Susan
                        </b>
                        , could you give us a hand, please?
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup userInfo={<Chat.UserInfo userName="Susan" />}>
                    <Chat.Message status="11:11 am">
                        Hello, I'm Susan. Could you please tell me which form is it about?
                        <Chat.SecondaryContent>
                            For example: ESt 1 B, ESt 2 D.
                        </Chat.SecondaryContent>
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup position="right">
                    <Chat.Message status="11:14 am">
                        It's about ESt 1 B
                    </Chat.Message>
                    <Chat.Message status="11:15 am">
                        Do I have to submit any annexes with this?
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup userInfo={<Chat.UserInfo userName="Susan" />}>
                    <Chat.Message status="11:16 am">
                        Yes, you have to attach the following:
                        <Chat.SecondaryContent>
                            Notice: Please double check the files!
                        </Chat.SecondaryContent>
                    </Chat.Message>
                    <Chat.Message status="11:16 am">
                        Annex FB{' '}
                        <Icon>
                            attachment
                        </Icon>
                    </Chat.Message>
                    <Chat.Message status="11:16 am">
                        Income/Annex FE1{' '}
                        <Icon>
                            attachment
                        </Icon>
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup position="right">
                    <Chat.Message status="11:17 am">
                        Ok, thank you.
                    </Chat.Message>
                </Chat.MessageGroup>                <Chat.MessageGroup
                    userInfo={<Chat.UserInfo userAvatar={<Chat.Avatar alt="Peter Avatar" imageUrl="images/user-avatar.png" />} userName="Peter" />}
                >
                    <Chat.Message status="11:11 am">
                        Hello, my name is Peter. How can I help you?
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup position="right">
                    <Chat.Message status="11:13 am">
                        Hello! I have a question about a tax form
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup
                    userInfo={<Chat.UserInfo userAvatar={<Chat.Avatar alt="Peter Avatar" imageUrl="images/user-avatar.png" />} userName="Peter" />}
                >
                    <Chat.Message status="11:13 am">
                        Regarding tax forms, Susan is our specialist. Hi{' '}
                        <b>
                            @Susan
                        </b>
                        , could you give us a hand, please?
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup userInfo={<Chat.UserInfo userName="Susan" />}>
                    <Chat.Message status="11:11 am">
                        Hello, I'm Susan. Could you please tell me which form is it about?
                        <Chat.SecondaryContent>
                            For example: ESt 1 B, ESt 2 D.
                        </Chat.SecondaryContent>
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup position="right">
                    <Chat.Message status="11:14 am">
                        It's about ESt 1 B
                    </Chat.Message>
                    <Chat.Message status="11:15 am">
                        Do I have to submit any annexes with this?
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup userInfo={<Chat.UserInfo userName="Susan" />}>
                    <Chat.Message status="11:16 am">
                        Yes, you have to attach the following:
                        <Chat.SecondaryContent>
                            Notice: Please double check the files!
                        </Chat.SecondaryContent>
                    </Chat.Message>
                    <Chat.Message status="11:16 am">
                        Annex FB{' '}
                        <Icon>
                            attachment
                        </Icon>
                    </Chat.Message>
                    <Chat.Message status="11:16 am">
                        Income/Annex FE1{' '}
                        <Icon>
                            attachment
                        </Icon>
                    </Chat.Message>
                </Chat.MessageGroup>
                <Chat.MessageGroup position="right">
                    <Chat.Message status="11:17 am">
                        Ok, thank you.
                    </Chat.Message>
                </Chat.MessageGroup>
            </Chat.Container>
        </div>
    )
}