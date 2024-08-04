import Markdown from 'react-markdown'
import aboutPageMd from '../content/aboutPage/aboutPage.md'
import React, { useState, useEffect } from 'react';
import rehypeRaw from "rehype-raw";

export const AboutPageContent = () => {
    const [markdown, setMarkdown] = useState('');
    useEffect(() => {
        fetch(aboutPageMd)
            .then(r => r.text())
            .then(text => {
                setMarkdown(text);
            });
    }, []);
    return (
        <div>
            <Markdown rehypePlugins={[rehypeRaw]}>
                {markdown}
            </Markdown>
        </div>
    )
}