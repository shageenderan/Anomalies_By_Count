import React from 'react';
import './Sidebar.css'
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

// Icons
import VideocamIcon from '@material-ui/icons/Videocam';
import TimelineIcon from '@material-ui/icons/Timeline';
import FindInPageIcon from '@material-ui/icons/FindInPage';
import Replay30Icon from '@material-ui/icons/Replay30';

// Router
import { Link } from "react-router-dom";

function iconStyles() {
  return {
    defaultIcon: {
      color: 'white',
    },
    errorIcon: {
      color: 'red',
    },
  }
}

function SideBar(props: {}) {
  const icons = makeStyles(iconStyles)();
  const [selectedIndex, setSelectedIndex] = React.useState(1);

  const handleListItemClick = (event: any, index: number) => {
    setSelectedIndex(index);
  };

  return (
    <div className="sidebar">
      <List component="nav" aria-label="main mailbox folders">
        <ListItem
          button
          component={Link}
          to={"/cameras"}
          selected={selectedIndex === 0}
          onClick={(event: any) => handleListItemClick(event, 0)}
        >
          <ListItemIcon>
            <VideocamIcon className={icons.defaultIcon} />
          </ListItemIcon>
          <ListItemText primary="Cameras" className="fontColor" />
        </ListItem>

        <ListItem
          button
          component={Link}
          to={"/stats"}
          selected={selectedIndex === 1}
          onClick={(event: any) => handleListItemClick(event, 1)}
        >
          <ListItemIcon>
            <TimelineIcon className={icons.defaultIcon} />
          </ListItemIcon>
          <ListItemText primary="Live stats" className="fontColor" />
        </ListItem>

        <ListItem
          button
          component={Link}
          to={"/analysis"}
          selected={selectedIndex === 2}
          onClick={(event: any) => handleListItemClick(event, 2)}
        >
          <ListItemIcon>
            <FindInPageIcon className={icons.defaultIcon} />
          </ListItemIcon>
          <ListItemText primary="Analysis" className="fontColor" />
        </ListItem>

        <ListItem
          button
          component={Link}
          to={"/playback"}
          selected={selectedIndex === 3}
          onClick={(event: any) => handleListItemClick(event, 3)}
        >
          <ListItemIcon>
            <Replay30Icon className={icons.defaultIcon} />
          </ListItemIcon>
          <ListItemText primary="Playback" className="fontColor" />
        </ListItem>
      </List>
    </div>
  )
}

export default SideBar