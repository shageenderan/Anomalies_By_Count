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
                personCount: number[],
                timeVal: number[]
                }
           }
}

interface StatisticState{
    charts: { [id: number]: {
                show:boolean,
                text:string,
                timeData:number[],
                peopleCount:number[],
                videoId:number,
                maximise:boolean
                }
    }, showNav:boolean
    ;
}

class Statistic extends Component<StatisticProps, StatisticState> {
  interval
  constructor(props: StatisticProps) {
    super(props);
    this.state = {
        charts: {
          // Hard code the statistic data for now
          1: {
            show: true,
            text: "Camera 1",
            timeData: [],
            peopleCount: [],
            videoId: -1,
            maximise: false
          },
          2: {
            show: true,
            text: "Camera 2",
            timeData: [],
            peopleCount: [],
            videoId: -1,
            maximise: false
          },
          3: {
            show: true,
            text: "Camera 3",
            timeData: [],
            peopleCount: [],
            videoId: -1,
            maximise: false
          },
          4: {
            show: true,
            text: "Camera 4",
            timeData: [],
            peopleCount: [],
            videoId: -1,
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
      charts[key].videoId = this.props.players[key].videoId
    }
    this.setState({ charts, showNav });
  };

  componentDidMount() {
    this.interval = setInterval(() =>
    {
      for (let key in this.state.charts){
        if (this.state.charts[key].videoId != -1){
          let count:number[] = []
          let timestamp:number[] = []
          let charts = Object.create(this.state.charts);
          axios.get(`video/${charts[key].videoId.toString()}/frame/`)
               .then(res => {
                  res.data.forEach(obj =>{
                    count.push(obj.count)
                    timestamp.push(obj.timestamp)
                  })
                  charts[key].timeData = timestamp
                  charts[key].peopleCount = count
                  this.setState({charts})
               })
            }
        }
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    const { charts, showNav } = this.state;
    let currentCharts: any = [];
    for (let key in charts) {
      let valMax:number = charts[key].timeData.length>0 ? (charts[key].timeData[charts[key].timeData.length-1]):10
      currentCharts.push(
        <Chart
          timeData={charts[key].timeData}
          peopleCount={charts[key].peopleCount}
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
