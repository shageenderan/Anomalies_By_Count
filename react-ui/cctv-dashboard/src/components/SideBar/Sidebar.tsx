import React from 'react';
import './Sidebar.css'
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ExpandLessIcon from "@material-ui/icons/ExpandLess";
import Collapse from "@material-ui/core/Collapse";
import Divider from "@material-ui/core/Divider";

// Router
import { Link } from "react-router-dom";


function SidebarItem({ depthStep = 10, depth = 0, item, ...rest }) {
  const [collapsed, setCollapsed] = React.useState(true);
  const { label, items, Icon, path, onClick: onClickProp } = item;

  function toggleCollapse() {
    setCollapsed(prevValue => !prevValue);
  }

  function onClick(e) {
    if (Array.isArray(items)) {
      toggleCollapse();
    }
    if (onClickProp) {
      onClickProp(e, item);
    }
  }

  let expandIcon;

  if (Array.isArray(items) && items.length) {
    expandIcon = !collapsed ? (
      <ExpandLessIcon
        className={
          "sidebar-item-expand-arrow" + " sidebar-item-expand-arrow-expanded"
        }
      />
    ) : (
      <ExpandMoreIcon className="sidebar-item-expand-arrow" />
    );
  }
  
  return (
    <>
      <ListItem
        button
        component={Link}
        to={path}
        className="sidebar-item"
        onClick={onClick}
        dense
        {...rest}
      >
        <div
          style={{ paddingLeft: depth * depthStep }}
          className="sidebar-item-content"
        >
          {Icon && <Icon className="sidebar-item-icon" fontSize="large" />}
          <div className="sidebar-item-text">{label}</div>
        </div>
        {expandIcon}
      </ListItem>
      <Collapse in={!collapsed} timeout="auto" unmountOnExit>
        {Array.isArray(items) ? (
          <List disablePadding dense>
            {items.map((subItem, index) => (
              <React.Fragment key={`${subItem.name}${index}`}>
                {subItem === "divider" ? (
                  <Divider style={{ margin: "6px 0" }} />
                ) : (
                  <SidebarItem
                    depth={depth + 1}
                    depthStep={depthStep}
                    item={subItem}
                  />
                )}
              </React.Fragment>
            ))}
          </List>
        ) : null}
      </Collapse>
    </>
  );
}

function SideBar({ items }) {
  return (
    <div className="sidebar">
      <List disablePadding dense>
        {items.map((sidebarItem) => (
          <SidebarItem
          depthStep={10}
          depth= {0}
          item={sidebarItem}
          />
        ))}
      </List>
    </div>
  )
}

export default SideBar