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
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk"
      },
      2: {
        show: true,
        label: "Camera 2",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk"
      },
      3: {
        show: true,
        label: "Camera 3",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk"
      },
      4: {
        show: true,
        label: "Camera 4",
        url: "https://www.youtube.com/watch?v=1EiC9bvVGnk"
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
          this.click
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

function createCameras(url, id, show, label, click) {
  if (!show) return null;

  return (
    <div className="col-xl-6">
      <a href="#" />
      <div className="camera-box-part text-center " onClick={() => click(id)}>
        <div className="title"></div>
        <Button className="text" variant="dark" size="lg">
          {label}
        </Button>
        <ReactPlayer url={url} playing={true} />
      </div>
    </div>
  );
}

export default Cameras;
