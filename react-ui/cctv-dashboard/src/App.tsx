import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";
import axios from "axios";

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

export const apiUrl = "http://localhost:8000/"

axios.defaults.baseURL = apiUrl


const items = [
  { name: "cameras", label: "Cameras", Icon: VideocamIcon, path: "/cameras" },
  { name: "stats", label: "Stats", Icon: TimelineIcon, path: "/stats" },
  {
    name: "analysis",
    label: "Analysis",
    Icon: FindInPageIcon,
    items: [
      {
        name: "camera1",
        label: "Camera 1",
        Icon: VideocamIcon,
        path: "/analysis/1"
      },
      {
        name: "camera2",
        label: "Camera 2",
        Icon: VideocamIcon,
        path: "/analysis/2"
      },
      {
        name: "camera3",
        label: "Camera 3",
        Icon: VideocamIcon,
        path: "/analysis/3"
      },
      {
        name: "camera4",
        label: "Camera 4",
        Icon: VideocamIcon,
        path: "/analysis/4"
      }
    ]
  }
];

interface AppState {
  players: {[id: number]: {show:boolean, label:string, url:string, maximise:boolean,
   showCam:"hidden"|"show", showUrl:"hidden"|"show", videoId: number, peopleCount: number[], timeData: number[]}};
}

class App extends React.Component<{}, AppState> {
  interval
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
          showUrl: "show",
          videoId: -1,
          peopleCount: [],
          timeData: []
        },
        2: {
          show: true,
          label: "Camera 2",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show",
          videoId: -1,
          peopleCount: [],
          timeData: []
        },
        3: {
          show: true,
          label: "Camera 3",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show",
          videoId: -1,
          peopleCount: [],
          timeData: []
        },
        4: {
          show: true,
          label: "Camera 4",
          url: "",
          maximise: false,
          showCam: "hidden",
          showUrl: "show",
          videoId: -1,
          peopleCount: [],
          timeData: []
        }
      }
    }
  }

  componentDidMount() {
    this.interval = setInterval(() =>
    {
      for (let key in this.state.players){
        if (this.state.players[key].videoId != -1) {
          let count:number[] = []
          let timestamp:number[] = []
          let players = {...this.state.players};
          let url = "video/"+players[key].videoId.toString()+"/frame/"
          let that = this
          axios.get(url)
               .then(res => {
                  res.data.forEach(obj =>{
                    count.push(obj.count)
                    timestamp.push(obj.timestamp)
                  })
                  players[key].timeData = timestamp
                  players[key].peopleCount = count
                  that.setState({ players })
               });
        }
      }
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }


  loadVideo = (e) => {
    let players = {...this.state.players}
    players[e.target.id].url = e.target.value
    this.setState({ players });
  }

  showCamera = (e) => {
    e.preventDefault();
    let players = {...this.state.players}
    let playerId = e.target.id
    players[playerId].showCam = "show"
    players[playerId].showUrl = "hidden"
    this.setState({ players });
    let that = this
    axios.post('/video/submit/',{ isUrl: 'True', url: this.state.players[playerId].url })
         .then(res => {
            that.state.players[playerId].videoId = res.data.id
            that.setState({players})
            })
  }


  toggleCameraSize = (id:string) => {
    const players = {...this.state.players};
    for (let key in this.state.players) {
      if (key !== id) {
        players[key].show = !players[key].show;
      } else {
        players[key].maximise = !players[key].maximise;
      }
    }
    this.setState({ players });
  };


  render() {
    return (
      <div className="App">
        <Router>
          <div className="App">
            <SideBar items={items} />
            <Route exact path="/" render={(props) => <Cameras players={this.state.players} toggleCameraSize={this.toggleCameraSize} showCamera={this.showCamera} loadVideo={this.loadVideo}/>}></Route>
            <Route path="/cameras" render={(props) => <Cameras players={this.state.players} toggleCameraSize={this.toggleCameraSize} showCamera={this.showCamera} loadVideo={this.loadVideo}/>}></Route>
            <Route path="/stats" render={(props) => <Statistic players={this.state.players}/>}></Route>
            <Route path="/analysis/:id" render={(props) => <Analysis {...props} data={this.state.players}/>}></Route>
          </div>
        </Router>
      </div>
    );
  }

};

export default App;
