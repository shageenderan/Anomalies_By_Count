import React from "react";
import ReactPlayer from "react-player";
import "./Playback.css";

function Playback(props: {}) {
  return (
    <div className="box">
      <div style={{ display: "flex" }}>
        <div
          style={{ width: "48%", height: "50vh", padding: "5px 0px 0px 0px" }}
        >
          <ReactPlayer
            url="https://www.youtube.com/watch?v=1EiC9bvVGnk"
            playing={true}
          />
        </div>
        <div
          style={{ width: "50%", height: "50vh", padding: "5px 0px 0px 15px" }}
        >
          <ReactPlayer
            url="https://www.youtube.com/watch?v=1EiC9bvVGnk"
            playing={true}
          />
        </div>
      </div>
      <div style={{ display: "flex" }}>
        <div
          style={{ width: "48%", height: "50vh", padding: "5px 0px 0px 0px" }}
        >
          <ReactPlayer
            url="https://www.youtube.com/watch?v=1EiC9bvVGnk"
            playing={true}
          />
        </div>
        <div
          style={{ width: "50%", height: "50vh", padding: "5px 0px 0px 15px" }}
        >
          <ReactPlayer
            url="https://www.youtube.com/watch?v=1EiC9bvVGnk"
            playing={true}
          />
        </div>
      </div>
    </div>
  );
}

export default Playback;
