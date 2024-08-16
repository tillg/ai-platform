import React, { useState, useEffect } from 'react';
import Markdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from "remark-gfm";

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
                setMarkdown(updatedText);
            });
    }, [markdownFile, replacements]);

    return (
        <>
            <style>{`
            table{
            border:1px solid black;
            border-collapse: collapse;
            }
            th, td{
            border:1px solid black;
            text-align:left;
            padding: 5px;
            }
            code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 15px;
            font-weight: bold;
            color: black;
            padding: 2px 4px;
            border-radius: 4px;
        }
        `}</style>
            <div>
                <Markdown
                    rehypePlugins={[rehypeRaw]}
                    remarkPlugins={[remarkGfm]}
                >
                    {markdown}
                </Markdown>
            </div>
        </>
    );
};

export default MarkdownRenderer;