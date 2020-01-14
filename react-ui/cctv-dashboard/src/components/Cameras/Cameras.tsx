import React, { Component } from "react";
import ReactPlayer from "react-player";
import "./Cameras.css";
import { JSXElement } from "@babel/types";
import Button from "react-bootstrap/Button";

interface CamerasProps {
  players: { [id: number]: { show: boolean, label: string, url: string, maximise: boolean, showCam: "hidden" | "show", showUrl: "hidden" | "show" } };
  loadVideo: (e: any) => void;
  showCamera: (e:any) => void;
  toggleCameraSize: (id: string) => void;
}

function Cameras(props: CamerasProps) {
  // const { players, showNav } = this.state;
  const players  = props.players;
  const currentPlayers = Object.keys(players).map(key =>
    {
      if (players[key].show) {
        let cName = players[key].maximise ? "maximise-box-part" : "camera-box-part";
        let playerHeight = players[key].maximise ? "800px" : " 350px";
        return (
          <div className="col-xl-6">
            <a href="#" />
            <div className={cName + " text-center"}>
              <Button className="text" variant="dark" size="lg" onClick={() => props.toggleCameraSize(key)}>
                {players[key].label}
              </Button>
              <form onSubmit={props.showCamera} id={key} className={players[key].showUrl}>
                <label>
                  URL:
                  <input type="text" id={key} onChange={props.loadVideo} />
                </label>
              </form>
              <div className={players[key].showCam} >
                <ReactPlayer
                  width="100"
                  height={playerHeight}
                  url={players[key].url}
                  controls={players[key].controls}
                  playing={true}
                />
              </div>
            </div>
          </div>
        );
      } 
      else {
        return null
      }
    }
  )

  return (
    <div className="container-true">
      <div className="row">{currentPlayers}</div>
    </div>
  );
}

export default Cameras;
