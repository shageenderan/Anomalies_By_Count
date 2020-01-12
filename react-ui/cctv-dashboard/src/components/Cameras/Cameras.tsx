import React, { Component } from "react";
import ReactPlayer from "react-player";
import "./Cameras.css";
import { JSXElement } from "@babel/types";
import Button from "react-bootstrap/Button";

class Cameras extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  state = {
    players: {
      1: {
        show: true,
        label: "Camera 1",
        url: "https://drive.google.com/uc?export=download&id=1WLm1va6XreJAFh0u4lY5Ntza-Aj05j8W",
        maximise: false,
        showCam: "hidden",
        showUrl: "show"
      },
      2: {
        show: true,
        label: "Camera 2",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false,
        showCam: "hidden",
        showUrl: "show"
      },
      3: {
        show: true,
        label: "Camera 3",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false,
        showCam: "hidden",
        showUrl: "show"
      },
      4: {
        show: true,
        label: "Camera 4",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false,
        showCam: "hidden",
        showUrl: "show"
      }
    },
    url: "",
    showNav: false
  };

  click = id => {
    const players = Object.create(this.state.players);
    let showNav = false;
    for (let key in this.state.players) {
      if (key !== id) {
        players[key].show = !players[key].show;
        showNav = !players[key].show;
      } else {
        players[key].maximise = !players[key].maximise;
      }
    }
    this.setState({ players, showNav });
  };

  render() {
    const { players, showNav, url } = this.state;
    let currentPlayers: any = [];
    for (let key in players) {
      currentPlayers.push(
        createCameras(
          players[key].url,
          key,
          players[key].show,
          players[key].label,
          this.click,
          players[key].controls,
          players[key].maximise,
          this
        )
      );
    }

    return (
      <div className="container-true">
        <div className="row">{currentPlayers}</div>
      </div>
    );
  }

   handleChange(event) {
    var players = this.state.players
    players[event.target.id].url = event.target.value
    this.setState({players});
  }

  handleSubmit(event){
    //alert('A name was submitted: ' + this.state.players[event.target.id].url);
    var players = this.state.players
    players[event.target.id].showCam = "show"
    players[event.target.id].showUrl = "hidden"
    this.setState({players});


    event.preventDefault();
  }
}

function createCameras(url, id, show, label, click, controls, maximise, context) {
  if (!show) return null;
  let cName: string = maximise ? "maximise-box-part" : "camera-box-part";
  let playerHeight: string = maximise ? "800px" : " 350px";
  return (
    <div className="col-xl-6">
      <a href="#" />
      <div className={cName + " text-center"}>
        <Button className="text" variant="dark" size="lg" onClick={() => click(id)}>
          {label}
        </Button>
        <form onSubmit={context.handleSubmit}  id={id} className={context.state.players[id].showUrl}>
          <label>
            URL:
            <input type="text" id={id} onChange={context.handleChange}/>
          </label>
        </form>
        <div className={context.state.players[id].showCam} >
            <ReactPlayer
              width="100"
              height={playerHeight}
              url={url}
              controls={controls}
              playing={true}
            />
        </div>
      </div>
    </div>
  );
}


export default Cameras;
