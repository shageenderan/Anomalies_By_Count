import React, { Component } from "react";
import ReactPlayer from "react-player";
import "./Cameras.css";
import { JSXElement } from "@babel/types";
import Button from "react-bootstrap/Button";

class Cameras extends Component {
  state = {
    players: {
      1: {
        show: true,
        label: "Camera 1",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false
      },
      2: {
        show: true,
        label: "Camera 2",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false
      },
      3: {
        show: true,
        label: "Camera 3",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false
      },
      4: {
        show: true,
        label: "Camera 4",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk",
        maximise: false
      }
    },
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
    const { players, showNav } = this.state;
    let currentPlayers: any = [];
    for (let key in players) {
      currentPlayers.push(
        createCameras(
          players[key].url,
          key,
          players[key].show,
          players[key].label,
          this.click,
          players[key].maximise
        )
      );
    }

    return (
      <div className="container-true">
        <div className="row">{currentPlayers}</div>
      </div>
    );
  }
}

function createCameras(url, id, show, label, click, maximise) {
  if (!show) return null;
  let cName: string = maximise ? "maximise-box-part" : "camera-box-part";
  let playerHeight: string = maximise ? "800px" : " 350px";
  return (
    <div className="col-xl-6">
      <a href="#" />
      <div className={cName + " text-center"} onClick={() => click(id)}>
        <Button className="text" variant="dark" size="lg">
          {label}
        </Button>
        <ReactPlayer
          width="100"
          height={playerHeight}
          url={url}
          playing={true}
        />
      </div>
    </div>
  );
}

export default Cameras;
