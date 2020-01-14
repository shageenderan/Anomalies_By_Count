import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";

// Components
import SideBar from "./components/SideBar/Sidebar";

import { makeStyles } from "@material-ui/core/styles";
import Cameras from "./components/Cameras/Cameras";
import Analysis from "./components/Analysis/Analysis";

// Icons
import VideocamIcon from "@material-ui/icons/Videocam";
import TimelineIcon from "@material-ui/icons/Timeline";
import FindInPageIcon from "@material-ui/icons/FindInPage";
import Replay30Icon from "@material-ui/icons/Replay30";
import Statistic from "./components/Statistic/Statistic";

const styles = makeStyles(theme => ({
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
  }
];

interface AppState {
  players: {[id: number]: {show:boolean, label:string, url:string, maximise:boolean, showCam:"hidden"|"show", showUrl:"hidden"|"show" }};
}

class App extends React.Component<{}, AppState> {
  constructor(props: {}) {
    super(props)
    this.state = {
      players: {
        1: {
          show: true,
          label: "Camera 1",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show"
        },
        2: {
          show: true,
          label: "Camera 2",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show"
        },
        3: {
          show: true,
          label: "Camera 3",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show"
        },
        4: {
          show: true,
          label: "Camera 4",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show"
        }
      },
    }
  }

  loadVideo = (e) => {
    let players = this.state.players
    players[e.target.id].url = e.target.value
    this.setState({ players });
  }

  showCamera = (e) => {
    //alert('A name was submitted: ' + this.state.players[event.target.id].url);
    e.preventDefault();
    let players = this.state.players
    players[e.target.id].showCam = "show"
    players[e.target.id].showUrl = "hidden"
    this.setState({ players });
  }

  toggleCameraSize = (id:string) => {
    const players = Object.create(this.state.players);
    // let showNav = false; 
    for (let key in this.state.players) {
      if (key !== id) {
        players[key].show = !players[key].show;
        // showNav = !players[key].show;
      } else {
        players[key].maximise = !players[key].maximise;
      }
    }
    // this.setState({ players, showNav });
    this.setState({ players });
  };

  render() {
    return (
      <div className="App">
        <Router>
          <div className="App">
            <SideBar items={items} />
            <Route exact path="/" component={Cameras} />
            <Route path="/cameras" render={() => <Cameras players={this.state.players} toggleCameraSize={this.toggleCameraSize} showCamera={this.showCamera} loadVideo={this.loadVideo}/>}></Route>
            <Route path="/stats" component={Statistic} />
            <Route path="/analysis" component={Analysis} />
          </div>
        </Router>
      </div>
    );
  }

};

export default App;
