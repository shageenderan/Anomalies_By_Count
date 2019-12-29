import React from "react";
import "./Statistic.css";
import LineChart from "./Charts/LineChart";

function Statistic(props: {}) {
  return (
    <div className="box">
      <div style={{ display: "flex" }}>
        <div
          style={{ width: "60%", height: "50vh", padding: "0px 0px 0px 0px" }}
        >
          <LineChart />
        </div>
        <div
          style={{ width: "60%", height: "50vh", padding: "0px 0px 0px 15px" }}
        >
          <LineChart />
        </div>
      </div>
      <div style={{ display: "flex" }}>
        <div
          style={{ width: "60%", height: "50vh", padding: "0px 0px 0px 0px" }}
        >
          <LineChart />
        </div>
        <div
          style={{ width: "60%", height: "50vh", padding: "5px 0px 0px 15px" }}
        >
          <LineChart />
        </div>
      </div>
    </div>
  );
}

export default Statistic;
