import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";

// Components
import SideBar from "./components/SideBar/Sidebar";

import { makeStyles } from "@material-ui/core/styles";
import Cameras from "./components/Cameras/Cameras";
import Analysis from "./components/Analysis/Analysis";
import Playback from "./components/Playback/Playback";

// Icons
import VideocamIcon from "@material-ui/icons/Videocam";
import TimelineIcon from "@material-ui/icons/Timeline";
import FindInPageIcon from "@material-ui/icons/FindInPage";
import Replay30Icon from "@material-ui/icons/Replay30";
import Statistic from "./components/Statistic/Statistic";

function Home(props: {}) {
  return (
    <div style={{ color: "white" }}>
      <Cameras></Cameras>
    </div>
  );
}

function Stats(props: {}) {
  return (
    <div style={{ color: "white" }}>
      <Statistic></Statistic>
    </div>
  );
}

function AnalysisPage(props: {}) {
  return (
    <div style={{ color: "white" }}>
      <Analysis></Analysis>
    </div>
  );
}

function PlaybackPage(props: {}) {
  return (
    <div style={{ color: "white" }}>
      <Playback></Playback>
    </div>
  );
}

const useStyles = makeStyles(theme => ({
  root: {
    display: "flex"
  },
  content: {
    marginLeft: "10px"
  }
}));

const items = [
  { name: "cameras", label: "Cameras", Icon: VideocamIcon, path: "/cameras" },
  { name: "stats", label: "Live stats", Icon: TimelineIcon, path: "/stats" },
  {
    name: "analysis",
    label: "Analysis",
    Icon: FindInPageIcon,
    items: [
      {
        name: "camera1",
        label: "Camera 1",
        Icon: VideocamIcon,
        path: "/analysis"
      },
      {
        name: "camera2",
        label: "Camera 2",
        Icon: VideocamIcon,
        path: "/analysis"
      },
      {
        name: "camera3",
        label: "Camera 3",
        Icon: VideocamIcon,
        path: "/analysis"
      },
      {
        name: "camera4",
        label: "Camera 4",
        Icon: VideocamIcon,
        path: "/analysis"
      }
    ]
  },
  {
    name: "playback",
    label: "Playback",
    Icon: Replay30Icon,
    items: [
      {
        name: "camera1",
        label: "Camera 1",
        Icon: VideocamIcon,
        path: "/playback"
      },
      {
        name: "camera2",
        label: "Camera 2",
        Icon: VideocamIcon,
        path: "/playback"
      },
      {
        name: "camera3",
        label: "Camera 3",
        Icon: VideocamIcon,
        path: "/playback"
      },
      {
        name: "camera4",
        label: "Camera 4",
        Icon: VideocamIcon,
        path: "/playback"
      }
    ]
  }
];

const App: React.FC = () => {
  const classes = useStyles();
  return (
    <div className="App">
      <Router>
        <div className={classes.root}>
          <SideBar items={items} />
          <Route exact path="/" component={Home} />

          <Route path="/cameras" component={Home} />

          <Route path="/stats" component={Stats} />

          <Route path="/analysis" component={AnalysisPage} />

          <Route path="/playback" component={PlaybackPage} />
        </div>
      </Router>
    </div>
  );
};

export default App;
