import React, { useState, useEffect } from 'react';
import Markdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';

interface Replacement {
    tag: string;
    value: string;
}

interface MarkdownRendererProps {
    markdownFile: string;
    replacements?: Replacement[];
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ markdownFile, replacements = [] }) => {
    const [markdown, setMarkdown] = useState('');

    useEffect(() => {
        fetch(markdownFile)
            .then(r => r.text())
            .then(text => {
                let updatedText = text;
                replacements.forEach(({ tag, value }) => {
                    const regex = new RegExp(tag, 'g');
                    updatedText = updatedText.replace(regex, value);
                });
                console.log(updatedText);
                setMarkdown(updatedText);
            });
    }, [markdownFile, replacements]);

    return (
        <div>
            <Markdown rehypePlugins={[rehypeRaw]}>
                {markdown}
            </Markdown>
        </div>
    );
};

export default MarkdownRenderer;