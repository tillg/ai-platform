
import { InnerWorkingElement } from "./InnerWorkingElement";
import { sortEntriesByType } from "./InnerWorkingSubPane";

interface Props {
    innerWorking: { [key: string]: any };
}


export const InnerWorkingPane = ({ innerWorking }: Props) => {
    return (
        <div>
            {sortEntriesByType(Object.entries(innerWorking)).map(([key, value]) => (
                <InnerWorkingElement key={key} keyName={key} value={value} />
            ))}
        </div>
    );
};