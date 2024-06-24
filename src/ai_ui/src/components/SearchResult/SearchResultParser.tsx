import { renderToStaticMarkup } from "react-dom/server";

type HtmlParsedAnswer = {
    answerHtml: string;
    citations: string[];
};

export function parseSearchResultToHtml(answer: string,  onCitationClicked: (citationFilePath: string) => void): HtmlParsedAnswer {
    const citations: string[] = [];

    // trim any whitespace from the end of the answer after removing follow-up questions
    let parsedAnswer = answer.trim();

    const parts = parsedAnswer.split(/\[([^\]]+)\]/g);

    const fragments: string[] = parts.map((part, index) => {
        if (index % 2 === 0) {
            return part;
        } else {
            let citationIndex: number;
            if (citations.indexOf(part) !== -1) {
                citationIndex = citations.indexOf(part) + 1;
            } else {
                citations.push(part);
                citationIndex = citations.length;
            }

            return renderToStaticMarkup(
                <a className="supContainer" title={part}>
                    <sup>{citationIndex}</sup>
                </a>
            );
        }
    });

    return {
        answerHtml: fragments.join(""),
        citations
    };
}
