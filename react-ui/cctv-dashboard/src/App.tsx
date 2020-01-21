import React from "react";
import "./App.css";
import { Router, Route } from "react-router-dom";
import history from "./history"

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

// Misc
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from "axios";

const styles = makeStyles(theme => ({
  root: {
    display: "flex"
  },
  content: {
    marginLeft: "10px"
  }
}));

axios.defaults.baseURL = process.env.REACT_APP_API_URL

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
        if (this.state.players[key].videoId !== -1) {
          let players = {...this.state.players};
          let count = players[key].peopleCount
          let timestamp = players[key].timeData
          let lastTime = timestamp[timestamp.length - 1]
          if (timestamp.length === 0){
            lastTime = 0
          }
          let url = "video/"+players[key].videoId.toString()+"/frame/?from="+lastTime
          let that = this
          axios.get(url)
               .then(res => {
                  let first = true
                  res.data.forEach(obj =>{
                    if (first){
                        first = false
                    }
                    else {
                        count.push(obj.count)
                        timestamp.push(obj.timestamp)
                        if (obj.anomaly === true){
                          that.notifyAnomaly(key, obj.timestamp)
                        }
                    }
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

  notifyAnomaly = (id, time) => toast("Anomaly detected in Camera "+id+" at time "+time,
                { autoClose: 8000,
                onClick:() => {
                this.navigatePage();
                this.toggleCameraSize(id);
                }
                });

  navigatePage = () => {
    history.push('/cameras')
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
        <Router history={history}>
          <div className="App">
            <SideBar items={items} />
            <Route exact path="/" render={(props) => <Cameras players={this.state.players} toggleCameraSize={this.toggleCameraSize} showCamera={this.showCamera} loadVideo={this.loadVideo}/>}></Route>
            <Route path="/cameras" render={(props) => <Cameras players={this.state.players} toggleCameraSize={this.toggleCameraSize} showCamera={this.showCamera} loadVideo={this.loadVideo}/>}></Route>
            <Route path="/stats" render={(props) => <Statistic players={this.state.players}/>}></Route>
            <Route path="/analysis/:id" render={(props) => <Analysis {...props} data={this.state.players}/>}></Route>
          </div>
        </Router>
        <ToastContainer />
      </div>
    );
  }

};

export default App;
