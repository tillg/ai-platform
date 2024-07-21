import React from "react";
import { FlyoutMenu, MenuItem } from "@com.mgmtp.a12.widgets/widgets-core/lib/menu";

export interface SidebarProps {
    items: MenuItem[];
}

export function Sidebar(props: SidebarProps): React.ReactElement<SidebarProps> {
    return <FlyoutMenu type="vertical" items={props.items} />;
}
