import * as React from "react";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";


export const SearchPage = () => {
    const [openConfigArea, setOpenConfigArea] = React.useState(true);
    const toggleContentArea = React.useCallback(() => {
        setOpenConfigArea((prevState) => !prevState);

    }, []);
    return (
        <>
            <h2><Icon>manage_search</Icon> Search  </h2>
            <SplitView>
                <SplitView.Area>
                    
                    <p>Here goes the search</p>
                </SplitView.Area>
                {openConfigArea && (
                    <SplitView.Area>
                        <ActionContentbox
                            headingElements={<ContentBoxElements.Title ariaLevel={2} text="Config" />}
                            headingButtons={
                                <ContentBoxElements.HeadingActionButton
                                    icon={<Icon>menu</Icon>}
                                    onClick={toggleContentArea}
                                    title="Toggle Area"
                                />
                            }>
                        </ActionContentbox>
                        <p>Config goes here</p>
                        Select Brain, no of results..
                    </SplitView.Area>
                )}
            </SplitView>
        </>)
}


