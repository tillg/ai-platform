import React from "react";
import { ApplicationHeader } from "@com.mgmtp.a12.widgets/widgets-core/lib/application-header";
import { FlyoutMenu, MenuItem } from "@com.mgmtp.a12.widgets/widgets-core/lib/menu";

export interface HeaderProps {
    items: MenuItem[];
}

export function Header(props: HeaderProps): React.ReactElement<HeaderProps> {
    return (
        <div>
            <ApplicationHeader leftSlots={
                <div>
                    <img src='../logo.jpg' alt="Logo" style={{ marginLeft: '10px', marginRight: '10px', height: '24px' }} />
                    <span>AI Platform</span>
                </div>
            } />
            <FlyoutMenu type="horizontal" items={props.items} />
        </div>
    );
}
