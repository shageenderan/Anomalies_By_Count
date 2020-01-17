import React, { Component } from "react";
import Chart from "./Charts/StatisticChart";
import axios from "axios";
import { apiUrl } from "../../App"

interface StatisticProps{
  players: { [id: number]: {
                show: boolean,
                label: string,
                url: string,
                maximise: boolean,
                showCam: "hidden" | "show",
                showUrl: "hidden" | "show",
                videoId: number,
                peopleCount: number[],
                timeData: number[]
                }
           }
}

interface StatisticState{
    charts: { [id: number]: {
                show:boolean,
                text:string,
                maximise:boolean
                }
    }, showNav:boolean
    ;
}

class Statistic extends Component<StatisticProps, StatisticState> {
  constructor(props: StatisticProps) {
    super(props);
    this.state = {
        charts: {
          // Hard code the statistic data for now
          1: {
            show: true,
            text: "Camera 1",
            maximise: false
          },
          2: {
            show: true,
            text: "Camera 2",
            maximise: false
          },
          3: {
            show: true,
            text: "Camera 3",
            maximise: false
          },
          4: {
            show: true,
            text: "Camera 4",
            maximise: false
          }
        },
        showNav: false
      }
  }
  click = id => {
    const charts = Object.create(this.state.charts);
    let showNav = false;
    for (let key in this.state.charts) {
      if (key !== id) {
        charts[key].show = !charts[key].show;
        showNav = !charts[key].show;
      } else {
        charts[key].maximise = !charts[key].maximise;
      }
    }
    this.setState({ charts, showNav });
  };

  render() {
    const { charts, showNav } = this.state;
    const players = this.props.players
    let currentCharts: any = [];
    for (let key in charts) {
      let valMax:number = players[key].timeData.length>0 ? (players[key].timeData[players[key].timeData.length-1]):10
      currentCharts.push(
        <Chart
          timeData={players[key].timeData}
          peopleCount={players[key].peopleCount}
          key={key}
          id={key}
          text={charts[key].text}
          show={charts[key].show}
          click={this.click}
          maximise={charts[key].maximise}
          valMax={valMax}
        />
      );
    }

    return (
      <div className="container-truex">
        <div className="row">{currentCharts}</div>
      </div>
    );
  }
}

export default Statistic;
