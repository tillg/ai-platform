import Markdown from 'markdown-to-jsx'


const markdown = `
# AI Platform
A platform to tinker around with Vector Databases, Prompts and Chats.

Inj order to play with it we have stuff:
* Vector DBs packaged in _Brains_
* LLMs wrapped so we can use them in _Chats_
 
`

export const AboutPage = () => {

    return (
        <div>
            {/* <BrainCircuitFilled fontSize={"120px"} primaryFill={theme.topic.brain} aria-hidden="true" aria-label="AI logo" /> */}
            <Markdown>{markdown}</Markdown>
        </div>)
}

